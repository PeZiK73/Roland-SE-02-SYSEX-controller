with open('Source/PluginEditor.cpp', 'r') as f:
    lines = f.readlines()
ids = []
for line in lines:
    if 'addKnob(' in line or 'addSwitch(' in line:
        import re
        match = re.search(r'add(?:Knob|Switch)\(\"([^\"]+)\"', line)
        if match:
            ids.append(match.group(1))
from collections import Counter
c = Counter(ids)
for k, v in c.items():
    if v > 1:
        print('Duplicate:', k)
