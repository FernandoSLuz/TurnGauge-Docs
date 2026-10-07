"""Extract the public API surface of a Unity package, with its XML doc comments.

Reads `///` comments straight from source, so the generated reference cannot drift
into describing members that do not exist or summaries that were never written.

Output is a JSON document consumed by generate_api.py.
"""
import io
import json
import os
import re
import sys

# --- declaration matching -------------------------------------------------

NAMESPACE = re.compile(r'^\s*namespace\s+([A-Za-z0-9_.]+)')

TYPE = re.compile(
    r'^\s*public\s+((?:sealed\s+|abstract\s+|static\s+|readonly\s+|partial\s+)*)'
    r'(class|struct|interface|enum)\s+([A-Za-z0-9_]+)([^{]*)')

# Recognize nested non-public types so their public-looking fields do not leak
# into the public outer type's generated entry.
TYPE_ANY = re.compile(
    r'^\s*((?:(?:public|private|protected|internal|static|sealed|abstract|partial|readonly)\s+)*)'
    r'(class|struct|interface|enum)\s+([A-Za-z0-9_]+)([^{]*)')

# The terminator alternatives are tried left to right, so `=>` has to precede the
# bare `=` or every expression-bodied property would read as a field. `=` is in the
# list because a field with an initializer -- `public const float X = 30f;`, and the
# id tables' `public static readonly StableId Y = ...` -- never reaches its `;` on
# the declaration line the parser sees, so without it those members are silently
# dropped. That previously hid a large part of the documented member surface.
MEMBER = re.compile(
    r'^\s*public\s+(?!class\b|struct\b|interface\b|enum\b)'
    r'((?:static\s+|virtual\s+|override\s+|readonly\s+|const\s+|abstract\s+|sealed\s+|'
    r'event\s+|async\s+|extern\s+|unsafe\s+|new\s+)*)'
    r'([A-Za-z0-9_<>\[\],.?:\s]+?)\s+([A-Za-z0-9_]+)\s*(\(|\{|=>|;|=|$)')

OPERATOR = re.compile(
    r'^\s*public\s+((?:static\s+|virtual\s+|override\s+|readonly\s+|abstract\s+|new\s+)*)'
    r'([A-Za-z0-9_<>,.?:\s]+?)\s+operator\s+(==|!=)\s*\(')

# Interface members are implicitly public and therefore have no `public` token.
INTERFACE_MEMBER = re.compile(
    r'^\s*(?!class\b|struct\b|interface\b|enum\b)'
    r'((?:static\s+|virtual\s+|override\s+|readonly\s+|const\s+|abstract\s+|sealed\s+|'
    r'event\s+|async\s+|extern\s+|unsafe\s+|new\s+)*)'
    r'([A-Za-z0-9_<>\[\],.?:\s]+?)\s+([A-Za-z0-9_]+)\s*(\(|\{|=>|;|=|$)')

# A constructor looks like `public TypeName(` with no return type.
CTOR = re.compile(r'^\s*public\s+([A-Za-z0-9_]+)\s*\(')

ATTRIBUTE = re.compile(r'^\s*\[')
DOC_LINE = re.compile(r'^\s*///\s?(.*)$')
# A conditionally compiled declaration puts `#if SYMBOL` between the doc comment
# and the type, so directives have to be transparent the same way attributes are.
# Otherwise a documented type reads as undocumented -- which is worse than a plain
# gap, because the reference then prints a "not documented" warning over real prose.
DIRECTIVE = re.compile(r'^\s*#\s*(if|else|elif|endif|region|endregion|pragma|nullable|define|undef|line|warning|error)\b')

EXCLUDE_DIR_PARTS = ('Tests', 'InternalTools', 'Internal', 'OptionalDemos', 'Library', 'obj', 'Temp')


def parameter_text(code):
    """Return the balanced parameter text after the first opening parenthesis.

    Signatures in the package are sometimes formatted over several lines and may
    contain nested calls in defaults.  Splitting at the first ``)`` silently
    truncated those signatures, so scan the balanced expression instead.
    """
    start = code.find('(')
    if start < 0:
        return ''
    depth = 0
    quote = None
    escaped = False
    for index in range(start, len(code)):
        char = code[index]
        if quote:
            if escaped:
                escaped = False
            elif char == '\\':
                escaped = True
            elif char == quote:
                quote = None
            continue
        if char in ('"', "'"):
            quote = char
        elif char == '(':
            depth += 1
        elif char == ')':
            depth -= 1
            if depth == 0:
                return code[start + 1:index].strip()
    return code[start + 1:].strip()


def parenthesis_delta(code):
    """Count structural parentheses while ignoring quoted defaults."""
    depth = 0
    quote = None
    escaped = False
    for char in code:
        if quote:
            if escaped:
                escaped = False
            elif char == '\\':
                escaped = True
            elif char == quote:
                quote = None
            continue
        if char in ('"', "'"):
            quote = char
        elif char == '(':
            depth += 1
        elif char == ')':
            depth -= 1
    return depth


def strip_line_comment(code):
    """Remove ``//`` comments without treating URL/string contents as comments."""
    quote = None
    verbatim = False
    escaped = False
    index = 0
    while index < len(code):
        char = code[index]
        if quote:
            if verbatim and char == '"':
                if index + 1 < len(code) and code[index + 1] == '"':
                    index += 2
                    continue
                quote = None
            elif not verbatim and escaped:
                escaped = False
            elif not verbatim and char == '\\':
                escaped = True
            elif not verbatim and char == quote:
                quote = None
            index += 1
            continue
        if char == '@' and index + 1 < len(code) and code[index + 1] == '"':
            quote, verbatim = '"', True
            index += 2
            continue
        if char in ('"', "'"):
            quote, verbatim = char, False
            index += 1
            continue
        if char == '/' and index + 1 < len(code) and code[index + 1] == '/':
            return code[:index]
        index += 1
    return code


def strip_leading_attributes(code):
    """Remove inline attribute blocks before matching a declaration.

    Unity-facing fields commonly use ``[SerializeField] public ...`` on one
    line.  The attribute is source syntax, not part of the declaration regex;
    leaving it in place makes an otherwise public field disappear.
    """
    index = 0
    length = len(code)
    while True:
        while index < length and code[index].isspace():
            index += 1
        if index >= length or code[index] != '[':
            return code[index:]
        depth = 0
        quote = None
        escaped = False
        end = index
        while end < length:
            char = code[end]
            if quote:
                if escaped:
                    escaped = False
                elif char == '\\':
                    escaped = True
                elif char == quote:
                    quote = None
            elif char in ('"', "'"):
                quote = char
            elif char == '[':
                depth += 1
            elif char == ']':
                depth -= 1
                if depth == 0:
                    index = end + 1
                    break
            end += 1
        else:
            return code


def declaration_line(lines, index, code):
    """Coalesce a declaration's multiline parameter list without consuming its body."""
    if parenthesis_delta(code) <= 0:
        return lines, index, code
    if not (CTOR.match(code) or OPERATOR.match(code) or MEMBER.match(code) or INTERFACE_MEMBER.match(code)):
        return lines, index, code

    parts = [code]
    depth = parenthesis_delta(code)
    while depth > 0 and index + 1 < len(lines):
        index += 1
        continuation = strip_line_comment(lines[index])
        parts.append(continuation)
        depth += parenthesis_delta(continuation)
    return lines, index, ' '.join(part.strip() for part in parts)


# --- XML doc comment parsing ---------------------------------------------

def clean_inline(text):
    """Turn XML doc inline tags into Markdown."""
    if not text:
        return ''
    # A cref may carry a documentation-ID prefix ("T:Foo.Bar", "M:Foo.Bar"), which is
    # stripped. The colon has to be required: with it optional, `cref="BattleSnapshot"`
    # matched B as the prefix and the reference rendered as `attleSnapshot`.
    text = re.sub(r'<see\s+cref="(?:[A-Za-z]:)?([^"]+)"\s*/>', r'`\1`', text)
    text = re.sub(r'<see\s+cref="(?:[A-Za-z]:)?([^"]+)"\s*>(.*?)</see>', r'`\2`', text, flags=re.S)
    text = re.sub(r'<see\s+href="([^"]+)"\s*/>', r'\1', text)
    text = re.sub(r'<see\s+langword="([^"]+)"\s*/>', r'`\1`', text)
    text = re.sub(r'<seealso\s+cref="(?:[A-Za-z]:)?([^"]+)"\s*/>', r'`\1`', text)
    text = re.sub(r'<paramref\s+name="([^"]+)"\s*/>', r'`\1`', text)
    text = re.sub(r'<typeparamref\s+name="([^"]+)"\s*/>', r'`\1`', text)
    text = re.sub(r'<c>(.*?)</c>', r'`\1`', text, flags=re.S)
    text = re.sub(r'</?para>', '\n\n', text)
    text = re.sub(r'<code>(.*?)</code>', r'`\1`', text, flags=re.S)
    text = re.sub(r'<b>(.*?)</b>', r'**\1**', text, flags=re.S)
    text = re.sub(r'<i>(.*?)</i>', r'*\1*', text, flags=re.S)
    text = text.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
    text = re.sub(r'<[^>]+>', '', text)          # drop any stray tags
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def section(buffer, tag):
    m = re.search(r'<%s>(.*?)</%s>' % (tag, tag), buffer, flags=re.S)
    return clean_inline(m.group(1)) if m else ''


def named_sections(buffer, tag):
    out = []
    for m in re.finditer(r'<%s\s+name="([^"]+)"\s*>(.*?)</%s>' % (tag, tag), buffer, flags=re.S):
        out.append({'name': m.group(1), 'text': clean_inline(m.group(2))})
    return out


def parse_doc(lines):
    """Turn a list of raw /// lines into structured doc fields."""
    buffer = '\n'.join(lines)
    summary = section(buffer, 'summary')
    if not summary and buffer.strip() and '<' not in buffer:
        # A bare /// comment with no tags is still a summary.
        summary = clean_inline(buffer)
    return {
        'summary': summary,
        'remarks': section(buffer, 'remarks'),
        'returns': section(buffer, 'returns'),
        'value': section(buffer, 'value'),
        'params': named_sections(buffer, 'param'),
        'exceptions': [
            {'name': m.group(1), 'text': clean_inline(m.group(2))}
            for m in re.finditer(
                r'<exception\s+cref="(?:[A-Za-z]:)?([^"]+)"\s*>(.*?)</exception>', buffer, flags=re.S)
        ],
    }


# --- file walking --------------------------------------------------------

def parse_file(path, display, out):
    try:
        with io.open(path, encoding='utf-8') as source:
            lines = source.read().split('\n')
    except Exception:
        return

    namespace = ''
    doc_buffer = []
    conditional_stack = []
    current = None
    depth_of_type = None
    entered_body = False
    # Enclosing types, innermost last. Without a stack a nested type ends its
    # parent rather than interrupting it, and every member declared after the
    # nested type is dropped. `BattleRuntimeController` declares two small
    # [Serializable] binding classes near the top of its body, so all forty of
    # its own members -- the entire scene-facing API -- extracted as nothing.
    enclosing = []
    brace = 0
    # Attributes such as [CreateAssetMenu(...)] often span several lines. While
    # one is open, intervening lines must not clear the pending doc comment.
    attribute_depth = 0
    ignored_nested_depths = []
    pending_nested_bases = []

    index = 0
    while index < len(lines):
        raw = lines[index]
        doc = DOC_LINE.match(raw)
        if doc:
            doc_buffer.append(doc.group(1))
            index += 1
            continue

        code = strip_line_comment(raw)
        # Attributes are source syntax, not part of declaration matching. Unity
        # authoring fields commonly use `[SerializeField] public ...` inline;
        # strip them before matching while the existing visibility checks still
        # decide whether the declaration belongs to the public surface.
        code = strip_leading_attributes(code)
        stripped = raw.strip()

        directive = DIRECTIVE.match(code)
        if directive:
            directive_name = directive.group(1)
            directive_text = code.strip()[1:].strip()
            if directive_name == 'if':
                conditional_stack.append('#if ' + directive_text[2:].strip())
            elif directive_name == 'else' and conditional_stack:
                conditional_stack[-1] = '#else (matching ' + conditional_stack[-1] + ')'
            elif directive_name == 'elif' and conditional_stack:
                conditional_stack[-1] = '#elif ' + directive_text[4:].strip()
            elif directive_name == 'endif' and conditional_stack:
                conditional_stack.pop()

        # A declaration may put each parameter on its own line.  Coalesce only
        # lines already recognised as declarations, so a method body call cannot
        # swallow the following source into a phantom signature.
        lines, index, code = declaration_line(lines, index, code)

        ns = NAMESPACE.match(code)
        if ns:
            namespace = ns.group(1)
            doc_buffer = []

        matched_declaration = False
        suppressed = bool(ignored_nested_depths)

        # A private/internal nested type remains lexically inside the public
        # outer type. Keep tracking braces, but suppress declarations within it.
        nested_type = TYPE_ANY.match(code) if current is not None and entered_body else None
        nested_nonpublic = nested_type and not TYPE.match(code)
        nested_nonpublic_base = brace if nested_nonpublic else None
        if nested_nonpublic:
            suppressed = True
            doc_buffer = []
            if '(' not in code and '{' not in code:
                pending_nested_bases.append(brace)

        conditions = list(conditional_stack)
        t = TYPE.match(code) if not suppressed else None
        if t:
            modifiers, kind, name, tail = (
                t.group(1).strip(), t.group(2), t.group(3), t.group(4).strip())
            # A public nested type belongs to the public outer type's qualified
            # namespace. Keeping only `namespace + name` makes a nested type
            # look top-level and can also collide with an unrelated type of the
            # same short name. The short `name` is retained for headings and
            # anchors; the qualified key preserves the source relationship.
            key = (current + '.' + name) if current is not None else (namespace + '.' + name)
            bases = ''
            if tail.startswith(':'):
                bases = tail.lstrip(':').strip().rstrip('{').strip()
            entry = out.setdefault(key, {
                'kind': kind,
                'modifiers': modifiers,
                'namespace': namespace,
                'name': name,
                'containing_type': current or '',
                'conditions': conditions,
                'bases': bases,
                'file': display,
                'doc': parse_doc(doc_buffer),
                'members': [],
                'enum_values': [],
            })
            # A partial type declared twice keeps the first non-empty doc.
            if not entry['doc']['summary'] and doc_buffer:
                entry['doc'] = parse_doc(doc_buffer)
            if current is not None:
                enclosing.append((current, depth_of_type, entered_body))
            current = key
            depth_of_type = brace
            entered_body = False
            matched_declaration = True
            doc_buffer = []

        elif current is not None and entered_body and not suppressed:
            entry = out[current]

            if entry['kind'] == 'enum':
                # Enum members are bare identifiers, optionally assigned.
                em = re.match(r'^\s*([A-Za-z_][A-Za-z0-9_]*)\s*(=\s*[^,]+)?,?\s*$', code)
                if em and em.group(1) not in ('get', 'set'):
                    entry['enum_values'].append({
                        'name': em.group(1),
                        'doc': parse_doc(doc_buffer),
                    })
                    matched_declaration = True
                    doc_buffer = []
            else:
                ctor = CTOR.match(code)
                operator = OPERATOR.match(code)
                mm = MEMBER.match(code)
                if not mm and entry['kind'] == 'interface':
                    mm = INTERFACE_MEMBER.match(code)
                if operator:
                    modifiers = operator.group(1).strip()
                    rtype = ' '.join(operator.group(2).split())
                    token = operator.group(3)
                    entry['members'].append({
                        'kind': 'method',
                        'modifiers': modifiers,
                        'type': rtype,
                        'name': 'operator ' + token,
                        'signature': 'public ' + (modifiers + ' ' if modifiers else '') +
                            rtype + ' operator ' + token + '(' + parameter_text(code) + ')',
                        'conditions': conditions,
                        'doc': parse_doc(doc_buffer),
                    })
                    matched_declaration = True
                    doc_buffer = []
                elif ctor and ctor.group(1) == entry['name']:
                    params = parameter_text(code)
                    entry['members'].append({
                        'kind': 'constructor',
                        'modifiers': '',
                        'type': '',
                        'name': entry['name'],
                        'signature': 'public ' + entry['name'] + '(' + params + ')',
                        'conditions': conditions,
                        'doc': parse_doc(doc_buffer),
                    })
                    matched_declaration = True
                    doc_buffer = []
                elif mm:
                    modifiers = mm.group(1).strip()
                    rtype = ' '.join(mm.group(2).split())
                    name = mm.group(3)
                    tail = mm.group(4)
                    # Classify by what terminates the declaration:
                    #   '('  a method
                    #   ';'  a field (possibly with an initializer)
                    #   '{'  a property whose accessors open on this line
                    #   ''   a property whose brace is on the next line
                    #   '=>' an expression-bodied property
                    if 'event' in modifiers:
                        kind = 'event'
                    elif tail == '(':
                        kind = 'method'
                    elif tail == ';' or tail == '=':
                        kind = 'field'
                    else:
                        kind = 'property'
                    signature = 'public ' + (modifiers + ' ' if modifiers else '') + rtype + ' ' + name
                    if tail == '(':
                        signature += '(' + parameter_text(code) + ')'
                    entry['members'].append({
                        'kind': kind,
                        'modifiers': modifiers,
                        'type': rtype,
                        'name': name,
                        'signature': signature,
                        'conditions': conditions,
                        'doc': parse_doc(doc_buffer),
                    })
                    matched_declaration = True
                    doc_buffer = []

        # Attributes sit between a doc comment and its declaration, so they must
        # not clear the buffer -- including multi-line ones, which is why the
        # bracket depth is tracked rather than just matching a leading '['.
        opens_attribute = ATTRIBUTE.match(raw) is not None
        inside_attribute = attribute_depth > 0 or opens_attribute
        if opens_attribute or attribute_depth > 0:
            attribute_depth += code.count('[') - code.count(']')
            if attribute_depth < 0:
                attribute_depth = 0

        is_directive = DIRECTIVE.match(raw) is not None

        if not matched_declaration and not inside_attribute and not is_directive and stripped != '':
            doc_buffer = []

        brace += code.count('{') - code.count('}')

        if pending_nested_bases and brace > pending_nested_bases[-1]:
            ignored_nested_depths.append(pending_nested_bases.pop())

        if nested_nonpublic and brace > nested_nonpublic_base:
            ignored_nested_depths.append(nested_nonpublic_base)
        while ignored_nested_depths and brace <= ignored_nested_depths[-1]:
            ignored_nested_depths.pop()

        if current is not None and depth_of_type is not None:
            if not entered_body:
                if brace > depth_of_type:
                    entered_body = True
            elif brace <= depth_of_type:
                if enclosing:
                    current, depth_of_type, entered_body = enclosing.pop()
                else:
                    current = None
                    depth_of_type = None
                    entered_body = False

        index += 1


def collect(root):
    out = {}
    for base, dirs, files in os.walk(root):
        rel = os.path.relpath(base, root).replace('\\', '/')
        parts = rel.split('/')
        if any(part in EXCLUDE_DIR_PARTS for part in parts):
            continue
        for name in sorted(files):
            if name.endswith('.cs'):
                parse_file(os.path.join(base, name), rel + '/' + name, out)
    return out


if __name__ == '__main__':
    root, dest = sys.argv[1], sys.argv[2]
    api = collect(root)
    io.open(dest, 'w', encoding='utf-8', newline='\n').write(
        json.dumps(api, indent=1, sort_keys=True))

    types = len(api)
    members = sum(len(v['members']) + len(v['enum_values']) for v in api.values())
    documented = sum(1 for v in api.values() if v['doc']['summary'])
    doc_members = sum(
        1 for v in api.values() for m in v['members'] if m['doc']['summary'])
    print('types: %d (%d with summaries)' % (types, documented))
    print('members: %d (%d with summaries)' % (members, doc_members))
