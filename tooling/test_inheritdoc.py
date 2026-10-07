import tempfile
import unittest
from pathlib import Path

import extract_docs


class InheritDocTests(unittest.TestCase):
    def collect(self, source):
        with tempfile.TemporaryDirectory() as directory:
            Path(directory, 'Contract.cs').write_text(source)
            return extract_docs.collect(directory)

    def member(self, api, key, name, index=0):
        return [m for m in api[key]['members'] if m['name'] == name][index]

    def test_explicit_marker_follows_interface_and_override_chain(self):
        api = self.collect('''namespace Sample;
public interface IClock
{
    /// <summary>Advance the visual clock.</summary>
    /// <param name="seconds">Elapsed visual seconds.</param>
    void Tick(float seconds);
}
public abstract class Clock : IClock
{
    /// <inheritdoc />
    public abstract void Tick(float seconds);
}
public class PreciseClock : Clock
{
    /// <inheritdoc />
    public override void Tick(float seconds) { }
}
public class UndocumentedClock : IClock
{
    public void Tick(float seconds) { }
}
''')
        doc = self.member(api, 'Sample.PreciseClock', 'Tick')['doc']
        self.assertEqual(doc['summary'], 'Advance the visual clock.')
        self.assertEqual(doc['params'], [{'name': 'seconds', 'text': 'Elapsed visual seconds.'}])
        self.assertEqual(doc['inherited_from'], 'Sample.IClock.public void Tick(float seconds)')
        self.assertFalse(self.member(api, 'Sample.UndocumentedClock', 'Tick')['doc']['summary'])

    def test_overloads_and_local_descriptions_remain_distinct(self):
        api = self.collect('''namespace Sample;
public interface IClock
{
    /// <summary>Step seconds.</summary>
    /// <param name="value">Seconds to step.</param>
    void Tick(float value);
    /// <summary>Step frames.</summary>
    /// <param name="value">Frames to step.</param>
    void Tick(int value);
}
public class Clock : IClock
{
    /// <inheritdoc />
    /// <summary>Use the custom seconds clock.</summary>
    public void Tick(float value) { }
    /// <inheritdoc />
    /// <param name="value">Custom frame count.</param>
    public void Tick(int value) { }
}
''')
        first = self.member(api, 'Sample.Clock', 'Tick', 0)['doc']
        second = self.member(api, 'Sample.Clock', 'Tick', 1)['doc']
        self.assertEqual(first['summary'], 'Use the custom seconds clock.')
        self.assertEqual(first['params'][0]['text'], 'Seconds to step.')
        self.assertEqual(second['summary'], 'Step frames.')
        self.assertEqual(second['params'][0]['text'], 'Custom frame count.')
        self.assertEqual(self.member(api, 'Sample.IClock', 'Tick', 1)['doc']['params'][0]['text'], 'Frames to step.')

    def test_conflicting_interfaces_and_unknown_base_remain_unresolved(self):
        api = self.collect('''namespace Sample;
public interface IFirst
{
    /// <summary>First contract.</summary>
    void Reset();
}
public interface ISecond
{
    /// <summary>Second contract.</summary>
    void Reset();
}
public class Ambiguous : IFirst, ISecond
{
    /// <inheritdoc />
    public void Reset() { }
}
public class External : UnknownBase, IFirst
{
    /// <inheritdoc />
    public void Reset() { }
}
''')
        for key in ['Sample.Ambiguous', 'Sample.External']:
            self.assertFalse(self.member(api, key, 'Reset')['doc']['summary'])
        self.assertEqual(self.member(api, 'Sample.Ambiguous', 'Reset')['doc']['inheritance_status'], 'ambiguous')

    def test_namespace_collision_and_cycles_do_not_invent_descriptions(self):
        api = self.collect('''namespace Other;
public interface IClock
{
    /// <summary>Wrong namespace.</summary>
    void Tick();
}
namespace Sample;
public interface IClock
{
    /// <summary>Correct namespace.</summary>
    void Tick();
}
public class Clock : IClock
{
    /// <inheritdoc />
    public void Tick() { }
}
public class CycleA : CycleB
{
    /// <inheritdoc />
    public void Tick() { }
}
public class CycleB : CycleA
{
    /// <inheritdoc />
    public void Tick() { }
}
''')
        self.assertEqual(self.member(api, 'Sample.Clock', 'Tick')['doc']['summary'], 'Correct namespace.')
        for key in ['Sample.CycleA', 'Sample.CycleB']:
            self.assertFalse(self.member(api, key, 'Tick')['doc']['summary'])

    def test_conditional_conflict_cref_and_renamed_parameters_stay_unresolved(self):
        api = self.collect('''namespace Sample;
public interface IClock
{
#if FIRST
    /// <summary>First branch.</summary>
    void Tick();
#else
    /// <summary>Second branch.</summary>
    void Tick();
#endif
    /// <summary>Advance seconds.</summary>
    void Advance(float seconds);
}
public class Clock : IClock
{
    /// <inheritdoc />
    public void Tick() { }
    /// <inheritdoc cref="IClock.Advance" />
    public void Advance(float seconds) { }
    /// <inheritdoc />
    public void Advance(float elapsed) { }
}
''')
        for member in api['Sample.Clock']['members']:
            self.assertFalse(member['doc']['summary'])
            self.assertNotEqual(member['doc'].get('inheritance_status'), 'resolved')


if __name__ == '__main__':
    unittest.main()
