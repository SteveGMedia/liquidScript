# liquidScript
A lightweight plugin system for python.

Note: Code is kind of jank and probably should be re-written at some point.

Sample Output:

```
Available Scripts:  ['Test']
Found Module:  Test
Test: <module 'Scripts' from 'd:\\Python\\liquidScript\\Scripts\\__init__.py'>
Plugin Loaded!
Injected: mystring = This is a test string to be injected. on <Scripts.Test.MyFirstPlugin object at 0x000001C90CB67430>
This is a test string to be injected.
Called !help function.
Parameter Keys:  ['data', 'testString', 'scriptObject']
Parameter Values:  [{'Hello': 'World'}, 'This is a test string.', <ScriptObject.ScriptObject object at 0x000001C90CB8A9D0>]
Plugin Unloaded!
```
