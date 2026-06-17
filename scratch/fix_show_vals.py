import re

with open('Source/PluginEditor.cpp', 'r') as f:
    content = f.read()

# Replace the bad showValuesBtn initialization block
bad_setup = '''    addAndMakeVisible(showValuesBtn);
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
    for (auto* s : switches) s->setVisible(false);'''

good_setup = '''    addAndMakeVisible(showValuesBtn);
    showValuesBtn.setToggleState(false, juce::dontSendNotification);
    showValuesBtn.onClick = [this] {
        bool show = showValuesBtn.getToggleState();
        customLookAndFeel.showValues = show;
        switchLookAndFeel.showValues = show;
        repaint();
    };
    customLookAndFeel.showValues = false;
    switchLookAndFeel.showValues = false;

    if (audioProcessor.hardwareMidiIn) midiInSelector.setText(audioProcessor.hardwareMidiIn->getDeviceInfo().name, juce::dontSendNotification);
    if (audioProcessor.hardwareMidiOut) midiOutSelector.setText(audioProcessor.hardwareMidiOut->getDeviceInfo().name, juce::dontSendNotification);'''

content = content.replace(bad_setup, good_setup)

with open('Source/PluginEditor.cpp', 'w') as f:
    f.write(content)
