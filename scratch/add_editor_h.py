import re

with open('Source/PluginEditor.h', 'r') as f:
    content = f.read()

members = '''    juce::ComboBox midiInSelector;
    juce::ComboBox midiOutSelector;
    juce::TextButton readPresetBtn{"READ PRESET"};
    
    juce::StringArray getMidiInputNames() {
        juce::StringArray names;
        for (auto info : juce::MidiInput::getAvailableDevices()) names.add(info.name);
        return names;
    }
    juce::StringArray getMidiOutputNames() {
        juce::StringArray names;
        for (auto info : juce::MidiOutput::getAvailableDevices()) names.add(info.name);
        return names;
    }

    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR (SE02_ControllerAudioProcessorEditor)
'''

content = re.sub(r'    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR \(SE02_ControllerAudioProcessorEditor\)', members, content)

with open('Source/PluginEditor.h', 'w') as f:
    f.write(content)
