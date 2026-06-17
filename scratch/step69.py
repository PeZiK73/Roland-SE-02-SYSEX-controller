import re

with open('scratch/generate.py', 'r') as f:
    content = f.read()

content = re.sub(r'juce::ComboBox midiOutBox;', 'juce::ComboBox midiOutBox;\n    juce::TextButton readPresetBtn;', content)

with open('scratch/generate.py', 'w') as f:
    f.write(content)
