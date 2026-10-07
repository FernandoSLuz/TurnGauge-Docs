"""Resolve explicit, unambiguous member inheritdoc within the extracted package.

This is a source reader, not a C# compiler. It handles non-generic base/interface
names in the same namespace or written in full, and exact member contracts,
including parameter names/defaults. Aliases, generic substitution, renamed
parameters, external types and cref/path selectors remain unresolved instead
of borrowing a plausible but unproven description.
"""
import copy
import re


def _contract(member):
    signature = member['signature']
    parameters = signature[signature.find('('):] if member['kind'] == 'method' else ''
    return (member['kind'], member['name'], member['type'], parameters)


def resolve_inheritdoc(api):
    """Fill absent sections only where an explicit marker has one source.

    Original declarations remain in place; inherited methods are not added to
    derived types. Resolution provenance and unresolved reasons stay in the JSON.
    """
    active = set()
    done = set()

    def bases(key):
        entry = api[key]
        for name in entry.get('bases', '').split(','):
            name = name.strip()
            if not name:
                continue
            if not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_.]*', name):
                yield None
                continue
            if '.' in name:
                if name in api:
                    yield name
                else:
                    yield None
                continue
            container = entry.get('containing_type') or entry['namespace']
            candidate = container + '.' + name
            if candidate in api:
                yield candidate
            elif container != entry['namespace']:
                candidate = entry['namespace'] + '.' + name
                if candidate in api:
                    yield candidate
                else:
                    yield None
            else:
                yield None

    def nearest(key, member, seen):
        candidates = set()
        incomplete = False
        for base in bases(key):
            if base is None:
                incomplete = True
                continue
            if base in seen:
                incomplete = True
                continue
            matches = [(base, index) for index, candidate in enumerate(api[base]['members'])
                       if _contract(candidate) == _contract(member)]
            # A nearest declaration without prose must not be silently skipped.
            if matches:
                candidates.update(matches)
            else:
                inherited, missing = nearest(base, member, seen | {base})
                candidates.update(inherited)
                incomplete |= missing
        return candidates, incomplete

    def resolve(identity):
        key, index = identity
        member = api[key]['members'][index]
        doc = member['doc']
        marker = doc.get('inheritdoc')
        if not marker or identity in done:
            return
        if identity in active:
            doc['inheritance_status'] = 'unresolved-cycle'
            return
        if marker != 'implicit' or member['kind'] not in ('method', 'property', 'event'):
            doc['inheritance_status'] = 'unsupported'
            done.add(identity)
            return

        active.add(identity)
        candidates, unresolved = nearest(key, member, {key})
        sources = {}
        for candidate_id in sorted(candidates):
            source_key, source_index = candidate_id
            source_member = api[source_key]['members'][source_index]
            # Conditional alternatives cannot donate to an unconditional member.
            if (source_member.get('conditions', []) != member.get('conditions', [])
                    or api[source_key].get('conditions', []) != api[key].get('conditions', [])):
                unresolved = True
                continue
            resolve(candidate_id)
            source_doc = source_member['doc']
            if (not source_doc.get('summary') or (source_doc.get('inheritdoc') and
                    source_doc.get('inheritance_status') != 'resolved')):
                unresolved = True
                continue
            origin = source_doc.get('inherited_from') or (source_key + '.' + source_member['signature'])
            sources[candidate_id] = (origin, source_doc)

        if len(sources) == 1 and not unresolved:
            origin, inherited = next(iter(sources.values()))
            for field in ('summary', 'remarks', 'returns', 'value'):
                if not doc.get(field):
                    doc[field] = inherited.get(field, '')
            for field in ('params', 'exceptions'):
                present = {item['name'] for item in doc.get(field, [])}
                doc.setdefault(field, []).extend(copy.deepcopy(item) for item in inherited.get(field, [])
                                                 if item['name'] not in present)
            doc['inherited_from'] = origin
            doc['inheritance_status'] = 'resolved'
        else:
            doc['inheritance_status'] = 'ambiguous' if len(sources) > 1 else 'unresolved'
        active.remove(identity)
        done.add(identity)

    for key in sorted(api):
        for index in range(len(api[key]['members'])):
            resolve((key, index))
