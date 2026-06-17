import re

def clean_editor_cpp():
    with open('Source/PluginEditor.cpp', 'r') as f:
        content = f.read()

    # We need to remove the initialization and layout logic for these buttons.
    # Searching for bounds calls
    content = re.sub(r'    readPresetBtn.*?\n', '', content)
    content = re.sub(r'    midiInBox.*?\n', '', content)
    content = re.sub(r'    midiOutBox.*?\n', '', content)
    content = re.sub(r'    refreshMidiBtn.*?\n', '', content)
    content = re.sub(r'    showValuesBtn.*?\n', '', content)
    
    # Also remove addAndMakeVisible calls that were missed or on next line
    content = re.sub(r'    mainPanel->addAndMakeVisible\(readPresetBtn\);\n', '', content)
    content = re.sub(r'    mainPanel->addAndMakeVisible\(midiInBox\);\n', '', content)
    content = re.sub(r'    mainPanel->addAndMakeVisible\(midiOutBox\);\n', '', content)
    content = re.sub(r'    mainPanel->addAndMakeVisible\(refreshMidiBtn\);\n', '', content)
    content = re.sub(r'    mainPanel->addAndMakeVisible\(showValuesBtn\);\n', '', content)

    # Also remove lambda blocks
    content = re.sub(r'        audioProcessor\.requestSysExPreset\(\);\n    \};\n', '', content)
    
    # The refreshMidiBtn block is large
    refresh_block = r'''    refreshMidiBtn\.onClick = \[this\]\(\) \{
        midiInBox\.clear\(\);
        auto inDevices = juce::MidiInput::getAvailableDevices\(\);
        for \(auto& dev : inDevices\) midiInBox\.addItem\(dev\.name, midiInBox\.getNumItems\(\) \+ 1\);

        midiOutBox\.clear\(\);
        auto outDevices = juce::MidiOutput::getAvailableDevices\(\);
        for \(auto& dev : outDevices\) midiOutBox\.addItem\(dev\.name, midiOutBox\.getNumItems\(\) \+ 1\);
    \};\n'''
    content = re.sub(refresh_block, '', content)

    # The midiInBox / midiOutBox onChange blocks
    midi_on_change = r'''    midiInBox\.onChange = \[this\]\(\) \{
        auto devs = juce::MidiInput::getAvailableDevices\(\);
        int idx = midiInBox\.getSelectedItemIndex\(\);
        if \(idx >= 0 && idx < devs\.size\(\)\) \{
            audioProcessor\.openMidiInput\(devs\[idx\]\.identifier\);
        \}
    \};
    
    midiOutBox\.onChange = \[this\]\(\) \{
        auto devs = juce::MidiOutput::getAvailableDevices\(\);
        int idx = midiOutBox\.getSelectedItemIndex\(\);
        if \(idx >= 0 && idx < devs\.size\(\)\) \{
            audioProcessor\.openMidiOutput\(devs\[idx\]\.identifier\);
        \}
    \};\n'''
    content = re.sub(midi_on_change, '', content)
    
    # showValuesBtn onClick
    show_values = r'''    showValuesBtn\.onClick = \[this\]\(\) \{
        customLookAndFeel\.showValues = showValuesBtn\.getToggleState\(\);
        repaint\(\);
    \};\n'''
    content = re.sub(show_values, '', content)

    with open('Source/PluginEditor.cpp', 'w') as f:
        f.write(content)

clean_editor_cpp()
print("Editor.cpp cleaned!")
