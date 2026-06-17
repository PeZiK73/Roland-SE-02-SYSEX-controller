import re

with open('Source/PluginProcessor.cpp', 'r') as f:
    processor_content = f.read()

with open('Source/PluginEditor.cpp', 'r') as f:
    editor_content = f.read()

processor_ids = set(re.findall(r'addCcParam\(\"([^\"]+)\"', processor_content))

editor_ids = []
for line in editor_content.split('\n'):
    if 'addKnob(' in line or 'addSwitch(' in line:
        match = re.search(r'add(?:Knob|Switch)\(\"([^\"]+)\"', line)
        if match:
            editor_ids.append(match.group(1))

for eid in editor_ids:
    if eid not in processor_ids:
        print("MISSING IN APVTS:", eid)
