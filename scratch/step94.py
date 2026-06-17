import re

with open('Source/PluginEditor.h', 'r') as f:
    h_content = f.read()

# Remove the getAvailableDevices lines
h_content = re.sub(r'for \(auto info : juce::MidiInput::getAvailableDevices\(\)\).*?\n', '', h_content)
h_content = re.sub(r'for \(auto info : juce::MidiOutput::getAvailableDevices\(\)\).*?\n', '', h_content)

with open('Source/PluginEditor.h', 'w') as f:
    f.write(h_content)

with open('Source/PluginProcessor.cpp', 'r') as f:
    p_content = f.read()

# Remove openMidiInput
p_content = re.sub(r'void SE02_ControllerAudioProcessor::openMidiInput.*?^\}\n', '', p_content, flags=re.DOTALL|re.MULTILINE)
# Remove openMidiOutput
p_content = re.sub(r'void SE02_ControllerAudioProcessor::openMidiOutput.*?^\}\n', '', p_content, flags=re.DOTALL|re.MULTILINE)

with open('Source/PluginProcessor.cpp', 'w') as f:
    f.write(p_content)

with open('Source/PluginProcessor.h', 'r') as f:
    ph_content = f.read()
    
ph_content = ph_content.replace('void openMidiInput(const juce::String& identifier);\n', '')
ph_content = ph_content.replace('    void openMidiOutput(const juce::String& identifier);\n', '')

with open('Source/PluginProcessor.h', 'w') as f:
    f.write(ph_content)

print("Purged all getAvailableDevices from all files.")
