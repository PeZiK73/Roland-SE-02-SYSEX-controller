import sys

with open('Source/PluginEditor.cpp', 'r') as f:
    content = f.read()

content = content.replace("juce::LookAndFeel::setDefaultLookAndFeel(&customLookAndFeel);", "setLookAndFeel(&customLookAndFeel);")
content = content.replace("juce::LookAndFeel::setDefaultLookAndFeel(nullptr);", "setLookAndFeel(nullptr);")

with open('Source/PluginEditor.cpp', 'w') as f:
    f.write(content)
