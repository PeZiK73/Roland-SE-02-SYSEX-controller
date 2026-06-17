import re

with open("../Source/PluginEditor.cpp", "r") as f:
    editor_content = f.read()

with open("../Source/PluginProcessor.cpp", "r") as f:
    processor_content = f.read()

editor_ids = set(re.findall(r'add(?:Knob|Switch)\("([^"]+)"', editor_content))
processor_ids = set(re.findall(r'addCcParam\("([^"]+)"', processor_content))

missing_in_processor = editor_ids - processor_ids
missing_in_editor = processor_ids - editor_ids

print("IDs in Editor but not in APVTS (WILL CAUSE CRASH!):")
for id in missing_in_processor:
    print(" - " + id)

print("\nIDs in APVTS but not in Editor:")
for id in missing_in_editor:
    print(" - " + id)
