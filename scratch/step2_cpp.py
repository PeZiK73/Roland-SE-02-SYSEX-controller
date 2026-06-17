import re

with open('Source/PluginProcessor.cpp', 'r') as f:
    content = f.read()

impls = '''
juce::String SE02_ControllerAudioProcessor::getBankName(int index)
{
    if (index == 0) return "A";
    if (index == 1) return "B";
    if (index == 2) return "C";
    if (index == 3) return "USER";
    if (index == 4) return "D";
    return "A";
}

void SE02_ControllerAudioProcessor::sendProgramChange()
{
    // MSB Bank A=1, B=2, C=3, USER=4, D=5
    // LSB is always 1
    int msb = currentBankIndex + 1;
    int lsb = 1;
    int pc = currentPreset - 1; // 0-127
    
    if (hardwareMidiOut) {
        hardwareMidiOut->sendMessageNow(juce::MidiMessage::controllerEvent(1, 0, msb));
        hardwareMidiOut->sendMessageNow(juce::MidiMessage::controllerEvent(1, 32, lsb));
        hardwareMidiOut->sendMessageNow(juce::MidiMessage::programChange(1, pc));
    }
}
'''

content = content.replace("void SE02_ControllerAudioProcessor::requestSysExPreset()", impls + "\nvoid SE02_ControllerAudioProcessor::requestSysExPreset()")

# Fix openMidiInput / openMidiOutput to sync with lastMidiInName so APVTS knows
sync_midi_in = '''    for (auto& dev : devs) {
        if (dev.name == identifier) {
            hardwareMidiIn = juce::MidiInput::openDevice(dev.identifier, this);
            if (hardwareMidiIn) {
                hardwareMidiIn->start();
                lastMidiInName = identifier;
            }
            break;
        }
    }'''

content = re.sub(r'    for \(auto& dev : devs\) \{\n        if \(dev\.name == identifier\) \{\n            hardwareMidiIn = juce::MidiInput::openDevice\(dev\.identifier, this\);\n            if \(hardwareMidiIn\) hardwareMidiIn->start\(\);\n            break;\n        \}\n    \}', sync_midi_in, content)


sync_midi_out = '''    for (auto& dev : devs) {
        if (dev.name == identifier) {
            hardwareMidiOut = juce::MidiOutput::openDevice(dev.identifier);
            if (hardwareMidiOut) lastMidiOutName = identifier;
            break;
        }
    }'''
content = re.sub(r'    for \(auto& dev : devs\) \{\n        if \(dev\.name == identifier\) \{\n            hardwareMidiOut = juce::MidiOutput::openDevice\(dev\.identifier\);\n            break;\n        \}\n    \}', sync_midi_out, content)


# Fix state loading/saving
state_get = '''
    auto state = apvts.copyState();
    if (lastMidiInName.isNotEmpty()) state.setProperty("midiIn", lastMidiInName, nullptr);
    if (lastMidiOutName.isNotEmpty()) state.setProperty("midiOut", lastMidiOutName, nullptr);
    state.setProperty("currentBank", currentBankIndex, nullptr);
    state.setProperty("currentPreset", currentPreset, nullptr);

    std::unique_ptr<juce::XmlElement> xml (state.createXml());
    copyXmlToBinary (*xml, destData);
'''

content = re.sub(r'void SE02_ControllerAudioProcessor::getStateInformation \(juce::MemoryBlock& destData\)\n\{\n.*?\n\}', 
    'void SE02_ControllerAudioProcessor::getStateInformation (juce::MemoryBlock& destData)\n{\n' + state_get + '\n}', content, flags=re.DOTALL)


state_set = '''
    std::unique_ptr<juce::XmlElement> xmlState (getXmlFromBinary (data, sizeInBytes));
    if (xmlState.get() != nullptr)
    {
        if (xmlState->hasTagName (apvts.state.getType()))
        {
            auto vt = juce::ValueTree::fromXml (*xmlState);
            apvts.replaceState (vt);
            
            if (vt.hasProperty("midiIn")) openMidiInput(vt.getProperty("midiIn").toString());
            if (vt.hasProperty("midiOut")) openMidiOutput(vt.getProperty("midiOut").toString());
            if (vt.hasProperty("currentBank")) currentBankIndex = vt.getProperty("currentBank");
            if (vt.hasProperty("currentPreset")) currentPreset = vt.getProperty("currentPreset");
        }
    }
'''

content = re.sub(r'void SE02_ControllerAudioProcessor::setStateInformation \(const void\* data, int sizeInBytes\)\n\{\n.*?\n\}', 
    'void SE02_ControllerAudioProcessor::setStateInformation (const void* data, int sizeInBytes)\n{\n' + state_set + '\n}', content, flags=re.DOTALL)


with open('Source/PluginProcessor.cpp', 'w') as f:
    f.write(content)
