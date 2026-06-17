import re

with open('Source/PluginProcessor.h', 'r') as f:
    content = f.read()

content = content.replace("juce::MidiInput* hardwareMidiIn = nullptr;", "std::unique_ptr<juce::MidiInput> hardwareMidiIn;")
content = content.replace("juce::MidiOutput* hardwareMidiOut = nullptr;", "std::unique_ptr<juce::MidiOutput> hardwareMidiOut;")

if "midiOutputQueue" not in content:
    content = content.replace("std::atomic<float> incomingSysExValues[120];", "std::atomic<float> incomingSysExValues[120];\n    juce::MidiBuffer midiOutputQueue;\n    int ccBlockTimer = 0;")

with open('Source/PluginProcessor.h', 'w') as f:
    f.write(content)

with open('Source/PluginProcessor.cpp', 'r') as f:
    cpp_content = f.read()

# Remove the duplicated createPluginFilter I added at the bottom
cpp_content = re.sub(r'//==============================================================================\n// This creates new instances of the plugin..\njuce::AudioProcessor\* JUCE_CALLTYPE createPluginFilter\(\)\n\{\n    return new SE02_ControllerAudioProcessor\(\);\n\}\n$', '', cpp_content)

with open('Source/PluginProcessor.cpp', 'w') as f:
    f.write(cpp_content)

