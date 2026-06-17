import re

with open('Source/PluginEditor.h', 'r') as f:
    content = f.read()

# Change white to transparent yellow
content = content.replace("g.setColour(juce::Colours::white);\n            g.setFont(12.0f);", "g.setColour(juce::Colours::yellow.withAlpha(0.5f));\n            g.setFont(12.0f);")
# Make sure it catches both instances
# Also remove valLabel from AttachedSlider
content = content.replace("juce::Label valLabel; // Value label\n", "")

with open('Source/PluginEditor.h', 'w') as f:
    f.write(content)


with open('Source/PluginEditor.cpp', 'r') as f:
    cpp_content = f.read()

# Remove valLabel initializations from addKnob
knob_regex = r'      comp->valLabel\.setJustificationType.*?comp->valLabel\.setText.*?;\n'
cpp_content = re.sub(knob_regex, '', cpp_content, flags=re.DOTALL)

with open('Source/PluginEditor.cpp', 'w') as f:
    f.write(cpp_content)

