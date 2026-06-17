import re

with open('Source/PluginProcessor.h', 'r') as f:
    content = f.read()

members = '''    juce::String getBankName(int index);
    void sendProgramChange();
    
    int currentBankIndex = 0; // 0=A, 1=B, 2=C, 3=USER, 4=D
    int currentPreset = 1; // 1 to 128
    
    // Update MIDI variables so apvts knows they changed
    juce::String lastMidiInName;
    juce::String lastMidiOutName;
'''

content = content.replace("    juce::MidiBuffer midiOutputQueue;", members + "\n    juce::MidiBuffer midiOutputQueue;")

with open('Source/PluginProcessor.h', 'w') as f:
    f.write(content)

