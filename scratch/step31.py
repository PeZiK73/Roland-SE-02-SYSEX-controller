import sys

with open('Source/PluginProcessor.h', 'r') as f:
    content = f.read()

if "void pushOutgoingMidiMessage" not in content:
    content = content.replace("void requestSysExPreset();", "void requestSysExPreset();\n    void pushOutgoingMidiMessage(const juce::MidiMessage& msg);")
    with open('Source/PluginProcessor.h', 'w') as f:
        f.write(content)
        print("Updated PluginProcessor.h")
else:
    print("Already updated PluginProcessor.h")
