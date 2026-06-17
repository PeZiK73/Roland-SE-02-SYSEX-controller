import re

editor_ids = set()
with open('Source/PluginEditor.cpp', 'r') as f:
    for match in re.finditer(r'add(?:Knob|Switch)\(\"([^\"]+)\"', f.read()):
        editor_ids.add(match.group(1))

processor_ids = set()
with open('Source/PluginProcessor.cpp', 'r') as f:
    for match in re.finditer(r'addCcParam\(\"([^\"]+)\"', f.read()):
        processor_ids.add(match.group(1))

missing = editor_ids - processor_ids
print('In Editor but not Processor:', missing)
if missing:
    print('CRASH REASON FOUND: SliderAttachment will dereference null parameter for', missing)
