import re

with open('Source/PluginProcessor.cpp', 'r') as f:
    content = f.read()

content = content.replace("dev.identifier == identifier", "dev.name == identifier")

state_get = '''
    auto state = apvts.copyState();
    std::unique_ptr<juce::XmlElement> xml (state.createXml());
    if (hardwareMidiIn) xml->setAttribute("midiIn", hardwareMidiIn->getDeviceInfo().name);
    if (hardwareMidiOut) xml->setAttribute("midiOut", hardwareMidiOut->getDeviceInfo().name);
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
            apvts.replaceState (juce::ValueTree::fromXml (*xmlState));
            if (xmlState->hasAttribute("midiIn")) openMidiInput(xmlState->getStringAttribute("midiIn"));
            if (xmlState->hasAttribute("midiOut")) openMidiOutput(xmlState->getStringAttribute("midiOut"));
        }
    }
'''

content = re.sub(r'void SE02_ControllerAudioProcessor::setStateInformation \(const void\* data, int sizeInBytes\)\n\{\n.*?\n\}', 
    'void SE02_ControllerAudioProcessor::setStateInformation (const void* data, int sizeInBytes)\n{\n' + state_set + '\n}', content, flags=re.DOTALL)

with open('Source/PluginProcessor.cpp', 'w') as f:
    f.write(content)
