import re

with open('Source/PluginProcessor.h', 'r') as f:
    content = f.read()

content = content.replace("void openMidiOutput(const juce::String& identifier);", "void openMidiOutput(const juce::String& identifier);\n    void saveGlobalSettings();\n    void loadGlobalSettings();")

with open('Source/PluginProcessor.h', 'w') as f:
    f.write(content)
