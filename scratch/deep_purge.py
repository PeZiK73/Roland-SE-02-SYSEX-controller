import re

with open('Source/PluginEditor.cpp', 'r') as f:
    content = f.read()

# Remove UI setup for MIDI dropdowns
content = re.sub(r'midiInBox\.setBounds.*?midiInBox\.onChange = \[this\]\(\) \{.*?\n    \};\n', '', content, flags=re.DOTALL)
content = re.sub(r'midiOutBox\.setBounds.*?midiOutBox\.onChange = \[this\]\(\) \{.*?\n    \};\n', '', content, flags=re.DOTALL)
content = re.sub(r'auto inDevices = juce::MidiInput::getAvailableDevices\(\);.*?\n', '', content, flags=re.DOTALL)
content = re.sub(r'auto outDevices = juce::MidiOutput::getAvailableDevices\(\);.*?\n', '', content, flags=re.DOTALL)
content = re.sub(r'for \(auto& dev : inDevices\) midiInBox\.addItem\(dev\.name, midiInBox\.getNumItems\(\) \+ 1\);\n', '', content)
content = re.sub(r'for \(auto& dev : outDevices\) midiOutBox\.addItem\(dev\.name, midiOutBox\.getNumItems\(\) \+ 1\);\n', '', content)
content = re.sub(r'    midiInBox.setBounds\(630, 302, 120, 24\);\n    midiInBox.setTextWhenNothingSelected\("MIDI Input..."\);\n    mainPanel->addAndMakeVisible\(midiInBox\);\n\n    midiOutBox.setBounds\(760, 302, 120, 24\);\n    midiOutBox.setTextWhenNothingSelected\("MIDI Output..."\);\n    mainPanel->addAndMakeVisible\(midiOutBox\);\n\n', '', content)
content = re.sub(r'    auto inDevices = juce::MidiInput::getAvailableDevices\(\);\n    for \(auto& dev : inDevices\) midiInBox.addItem\(dev.name, midiInBox.getNumItems\(\) \+ 1\);\n    \n    auto outDevices = juce::MidiOutput::getAvailableDevices\(\);\n    for \(auto& dev : outDevices\) midiOutBox.addItem\(dev.name, midiOutBox.getNumItems\(\) \+ 1\);\n    \n    midiInBox.onChange = \[this\]\(\) \{\n        auto devs = juce::MidiInput::getAvailableDevices\(\);\n        int idx = midiInBox.getSelectedItemIndex\(\);\n        if \(idx >= 0 && idx < devs.size\(\)\) audioProcessor.openMidiInput\(devs\[idx\].identifier\);\n    \};\n    \n    midiOutBox.onChange = \[this\]\(\) \{\n        auto devs = juce::MidiOutput::getAvailableDevices\(\);\n        int idx = midiOutBox.getSelectedItemIndex\(\);\n        if \(idx >= 0 && idx < devs.size\(\)\) audioProcessor.openMidiOutput\(devs\[idx\].identifier\);\n    \};\n', '', content)


with open('Source/PluginEditor.cpp', 'w') as f:
    f.write(content)

with open('Source/PluginProcessor.cpp', 'r') as f:
    content = f.read()

# Remove openMidiInput and openMidiOutput methods
content = re.sub(r'void SE02_ControllerAudioProcessor::openMidiInput.*?^}\n', '', content, flags=re.DOTALL|re.MULTILINE)
content = re.sub(r'void SE02_ControllerAudioProcessor::openMidiOutput.*?^}\n', '', content, flags=re.DOTALL|re.MULTILINE)
# Remove hardwareMidiOut references
content = re.sub(r'if \(hardwareMidiOut\) hardwareMidiOut->sendMessageNow\(rq1\);\n\s+else midiOutputQueue\.addEvent\(rq1, 0\);', 'midiOutputQueue.addEvent(rq1, 0);', content)

with open('Source/PluginProcessor.cpp', 'w') as f:
    f.write(content)

with open('Source/PluginProcessor.h', 'r') as f:
    content = f.read()
content = re.sub(r'std::unique_ptr<juce::MidiInput> hardwareMidiIn;\n\s+std::unique_ptr<juce::MidiOutput> hardwareMidiOut;', '', content)
content = re.sub(r'void openMidiInput\(const juce::String& identifier\);\n\s+void openMidiOutput\(const juce::String& identifier\);', '', content)
with open('Source/PluginProcessor.h', 'w') as f:
    f.write(content)

with open('Source/PluginEditor.h', 'r') as f:
    content = f.read()
content = re.sub(r'juce::ComboBox midiInBox;\n\s+juce::ComboBox midiOutBox;', '', content)
with open('Source/PluginEditor.h', 'w') as f:
    f.write(content)
