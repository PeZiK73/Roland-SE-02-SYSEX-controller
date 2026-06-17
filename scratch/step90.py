import re

with open('Source/PluginEditor.h', 'r') as f:
    h_content = f.read()
h_content = re.sub(r'^\s*juce::ComboBox midiInBox;.*?\n', '', h_content, flags=re.MULTILINE)
h_content = re.sub(r'^\s*juce::ComboBox midiOutBox;.*?\n', '', h_content, flags=re.MULTILINE)
with open('Source/PluginEditor.h', 'w') as f:
    f.write(h_content)

with open('Source/PluginEditor.cpp', 'r') as f:
    c_content = f.read()

# Completely remove all references to midiInBox and midiOutBox
c_content = re.sub(r'^.*midiInBox.*?\n', '', c_content, flags=re.MULTILINE)
c_content = re.sub(r'^.*midiOutBox.*?\n', '', c_content, flags=re.MULTILINE)
c_content = re.sub(r'^.*getAvailableDevices.*?\n', '', c_content, flags=re.MULTILINE)

# The lambdas might have leftover lines like:
#         int idx = ...
#         if (idx >= 0 ...
#     };
# Let's clean those up manually
c_content = re.sub(r'^\s*int idx =.*?\n', '', c_content, flags=re.MULTILINE)
c_content = re.sub(r'^\s*if \(idx >= 0.*?\n', '', c_content, flags=re.MULTILINE)
c_content = re.sub(r'^\s*};\s*$', '', c_content, flags=re.MULTILINE) # This might aggressively remove other lambdas!

with open('Source/PluginEditor.cpp', 'w') as f:
    f.write(c_content)
