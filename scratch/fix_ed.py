import re

with open('Source/PluginEditor.h', 'r') as f:
    content = f.read()

content = content.replace("juce::TextButton readPresetBtn{\"READ PRESET\"};", "juce::TextButton readPresetBtn{\"READ PRESET\"};\n    juce::ToggleButton showValuesBtn{\"SHOW PARAMETERS\"};")

with open('Source/PluginEditor.h', 'w') as f:
    f.write(content)

with open('Source/PluginEditor.cpp', 'r') as f:
    cpp_content = f.read()

# Add to constructor
setup_code = '''
    addAndMakeVisible(showValuesBtn);
    showValuesBtn.setToggleState(false, juce::dontSendNotification);
    showValuesBtn.onClick = [this] {
        bool show = showValuesBtn.getToggleState();
        for (auto* k : knobs) k->setVisible(show);
        for (auto* s : switches) s->setVisible(show);
    };

    if (audioProcessor.hardwareMidiIn) midiInSelector.setText(audioProcessor.hardwareMidiIn->getDeviceInfo().name, juce::dontSendNotification);
    if (audioProcessor.hardwareMidiOut) midiOutSelector.setText(audioProcessor.hardwareMidiOut->getDeviceInfo().name, juce::dontSendNotification);

    // Initial hide
    for (auto* k : knobs) k->setVisible(false);
    for (auto* s : switches) s->setVisible(false);
'''

cpp_content = cpp_content.replace("    addAndMakeVisible(resizer);", "    addAndMakeVisible(resizer);\n" + setup_code)

# Add to resized()
resize_code = '''
    midiInSelector.setBounds(w - (610 * scaleX), h - (25 * scaleY), 150 * scaleX, 20 * scaleY);
    midiOutSelector.setBounds(w - (450 * scaleX), h - (25 * scaleY), 150 * scaleX, 20 * scaleY);
    showValuesBtn.setBounds(w - (290 * scaleX), h - (25 * scaleY), 150 * scaleX, 20 * scaleY);
    readPresetBtn.setBounds(w - (130 * scaleX), h - (25 * scaleY), 100 * scaleX, 20 * scaleY);
'''

cpp_content = re.sub(r'    midiInSelector\.setBounds.*readPresetBtn\.setBounds[^;]*;\n', resize_code + '\n', cpp_content, flags=re.DOTALL)

with open('Source/PluginEditor.cpp', 'w') as f:
    f.write(cpp_content)

