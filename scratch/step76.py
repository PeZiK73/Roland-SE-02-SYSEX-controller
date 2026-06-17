import re

with open('Source/PluginEditor.cpp', 'r') as f:
    e_content = f.read()

with open('Source/PluginProcessor.cpp', 'r') as f:
    p_content = f.read()

editor_ids = set(re.findall(r'add(?:Knob|Switch)\("([^"]+)"', e_content))
processor_ids = set(re.findall(r'addCcParam\("([^"]+)"', p_content))

print("In Editor but not Processor:", editor_ids - processor_ids)
print("In Processor but not Editor:", processor_ids - editor_ids)
