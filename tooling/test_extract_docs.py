import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import extract_docs


SOURCE = r'''
namespace Sample;

/// <summary>Surface with multiline declarations.</summary>
public class Surface
{
    /// <summary>Four values.</summary>
    /// <param name="first">First value.</param>
    /// <param name="second">Second value.</param>
    /// <param name="third">Third value.</param>
    /// <param name="fourth">Fourth value.</param>
    public void Apply(
        int first,
        string second = "right)",
        int third = Math.Max(1, 2),
        bool fourth = true)
    {
    }

    /// <summary>Three values.</summary>
    public void SetCombatantPortrait(
        int id,
        int sprite,
        int source,
        int desired)
    {
    }

    /// <summary>Two values.</summary>
    public void SetCombatantArt(
        int id,
        int art)
    {
    }

    /// <summary>URL default must not start a comment.</summary>
    public void WithUrl(
        string url = "https://example.com")
    {
    }

    /// <summary>This declaration follows the URL method.</summary>
    public void AfterUrl()
    {
    }

    /// <summary>Constructs the surface.</summary>
    public Surface(
        int width,
        int height = Math.Max(1, 2))
    {
    }

    /// <summary>A property must remain a property.</summary>
    public int Width
    {
        get;
    }

    private sealed class PrivateChip
    {
        public int CombatantId;
    }

    internal enum InternalKind
    {
        Hidden
    }

    /// <summary>Still a public member of the outer type.</summary>
    public int Height { get; }
}

/// <summary>Interface declarations are implicitly public.</summary>
public interface IContract
{
    /// <summary>Interface method.</summary>
    void Execute(
        int count,
        int stride = Math.Max(1, 2));
}
'''


class ExtractDocsTests(unittest.TestCase):
    def test_multiline_methods_constructors_and_interface_members(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / 'Surface.cs'
            source.write_text(SOURCE, encoding='utf-8')
            api = extract_docs.collect(directory)

        surface = api['Sample.Surface']
        members = {member['name']: member for member in surface['members']}
        self.assertEqual(
            members['Apply']['signature'],
            'public void Apply(int first, string second = "right)", int third = Math.Max(1, 2), bool fourth = true)')
        self.assertEqual(
            members['SetCombatantPortrait']['signature'],
            'public void SetCombatantPortrait(int id, int sprite, int source, int desired)')
        self.assertEqual(
            members['SetCombatantArt']['signature'],
            'public void SetCombatantArt(int id, int art)')
        self.assertEqual(
            members['WithUrl']['signature'],
            'public void WithUrl(string url = "https://example.com")')
        self.assertEqual(members['AfterUrl']['signature'], 'public void AfterUrl()')
        self.assertEqual(
            members['Surface']['signature'],
            'public Surface(int width, int height = Math.Max(1, 2))')
        self.assertEqual(members['Width']['kind'], 'property')
        self.assertNotIn('CombatantId', members)
        self.assertNotIn('PrivateChip', members)
        self.assertNotIn('InternalKind', members)
        self.assertIn('Height', members)

        contract = api['Sample.IContract']
        self.assertEqual(
            contract['members'][0]['signature'],
            'public void Execute(int count, int stride = Math.Max(1, 2))')

    def test_parameter_text_handles_nested_parentheses_and_quotes(self):
        code = 'public void Apply(string value = "right)", int count = Math.Max(1, 2))'
        self.assertEqual(
            extract_docs.parameter_text(code),
            'string value = "right)", int count = Math.Max(1, 2)')


if __name__ == '__main__':
    unittest.main()
