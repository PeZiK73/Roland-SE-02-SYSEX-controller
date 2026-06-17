import re

with open('Source/PluginProcessor.h', 'r') as f:
    content = f.read()

if 'requestSysExPreset' not in content:
    content = content.replace('void sendSysEx(const juce::uint8* data, int size);', 'void sendSysEx(const juce::uint8* data, int size);\n    void requestSysExPreset();')
    
if 'midiOutputQueue' not in content:
    content = content.replace('juce::AudioProcessorValueTreeState apvts;', 'juce::AudioProcessorValueTreeState apvts;\n    juce::MidiBuffer midiOutputQueue;')

with open('Source/PluginProcessor.h', 'w') as f:
    f.write(content)

with open('Source/PluginEditor.h', 'r') as f:
    content = f.read()

if 'midiInBox' not in content:
    content = content.replace('juce::TextButton loadPresetBtn{"LOAD PRESET"};', 'juce::ComboBox midiInBox;\n    juce::ComboBox midiOutBox;\n    juce::TextButton loadPresetBtn{"LOAD PRESET"};')

with open('Source/PluginEditor.h', 'w') as f:
    f.write(content)
