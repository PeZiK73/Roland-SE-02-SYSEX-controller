import re

with open('Source/PluginEditor.h', 'r') as f:
    content = f.read()

buttons = '''    juce::TextButton bankPrevBtn{"<"};
    juce::TextButton bankNextBtn{">"};
    juce::Label bankLabel;

    juce::TextButton presetPrevBtn{"<"};
    juce::TextButton presetNextBtn{">"};
    juce::Label presetLabel;

    juce::TextButton browseBtn{"BROWSE"};
    juce::TextButton savePresetBtn{"SAVE PR"};
'''

content = content.replace("    juce::TextButton readPresetBtn{\"READ PRESET\"};", "    juce::TextButton readPresetBtn{\"READ PRESET\"};\n" + buttons)

with open('Source/PluginEditor.h', 'w') as f:
    f.write(content)
