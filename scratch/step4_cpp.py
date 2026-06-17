import re

with open('Source/PluginEditor.cpp', 'r') as f:
    content = f.read()

setup_code = '''
    auto updateLabels = [this] {
        bankLabel.setText("BANK: " + audioProcessor.getBankName(audioProcessor.currentBankIndex), juce::dontSendNotification);
        juce::String pstr = juce::String(audioProcessor.currentPreset);
        if (pstr.length() == 1) pstr = "0" + pstr;
        presetLabel.setText("PRESET: " + pstr, juce::dontSendNotification);
    };

    addAndMakeVisible(presetPrevBtn);
    presetPrevBtn.onClick = [this, updateLabels] {
        if (audioProcessor.currentPreset > 1) audioProcessor.currentPreset--;
        else audioProcessor.currentPreset = 128;
        audioProcessor.sendProgramChange();
        updateLabels();
    };

    addAndMakeVisible(presetNextBtn);
    presetNextBtn.onClick = [this, updateLabels] {
        if (audioProcessor.currentPreset < 128) audioProcessor.currentPreset++;
        else audioProcessor.currentPreset = 1;
        audioProcessor.sendProgramChange();
        updateLabels();
    };

    addAndMakeVisible(presetLabel);
    presetLabel.setJustificationType(juce::Justification::centred);
    presetLabel.setColour(juce::Label::textColourId, juce::Colours::yellow);

    addAndMakeVisible(bankPrevBtn);
    bankPrevBtn.onClick = [this, updateLabels] {
        if (audioProcessor.currentBankIndex > 0) audioProcessor.currentBankIndex--;
        else audioProcessor.currentBankIndex = 4;
        audioProcessor.sendProgramChange();
        updateLabels();
    };

    addAndMakeVisible(bankNextBtn);
    bankNextBtn.onClick = [this, updateLabels] {
        if (audioProcessor.currentBankIndex < 4) audioProcessor.currentBankIndex++;
        else audioProcessor.currentBankIndex = 0;
        audioProcessor.sendProgramChange();
        updateLabels();
    };

    addAndMakeVisible(bankLabel);
    bankLabel.setJustificationType(juce::Justification::centred);
    bankLabel.setColour(juce::Label::textColourId, juce::Colours::yellow);

    addAndMakeVisible(browseBtn);
    addAndMakeVisible(savePresetBtn);

    updateLabels();
'''

content = content.replace("    addAndMakeVisible(resizer);", "    addAndMakeVisible(resizer);\n" + setup_code)

resize_code = '''
    presetPrevBtn.setBounds(10 * scaleX, h - (25 * scaleY), 20 * scaleX, 20 * scaleY);
    presetLabel.setBounds(30 * scaleX, h - (25 * scaleY), 70 * scaleX, 20 * scaleY);
    presetNextBtn.setBounds(100 * scaleX, h - (25 * scaleY), 20 * scaleX, 20 * scaleY);

    bankPrevBtn.setBounds(130 * scaleX, h - (25 * scaleY), 20 * scaleX, 20 * scaleY);
    bankLabel.setBounds(150 * scaleX, h - (25 * scaleY), 60 * scaleX, 20 * scaleY);
    bankNextBtn.setBounds(210 * scaleX, h - (25 * scaleY), 20 * scaleX, 20 * scaleY);

    browseBtn.setBounds(240 * scaleX, h - (25 * scaleY), 70 * scaleX, 20 * scaleY);
    
    // Move savePresetBtn over to the right side, next to SHOW PARAMETERS
    savePresetBtn.setBounds(w - (210 * scaleX), h - (25 * scaleY), 70 * scaleX, 20 * scaleY);

    midiInSelector.setBounds(w - (610 * scaleX), h - (25 * scaleY), 150 * scaleX, 20 * scaleY);
    midiOutSelector.setBounds(w - (450 * scaleX), h - (25 * scaleY), 150 * scaleX, 20 * scaleY);
    showValuesBtn.setBounds(w - (290 * scaleX), h - (25 * scaleY), 70 * scaleX, 20 * scaleY);
    readPresetBtn.setBounds(w - (130 * scaleX), h - (25 * scaleY), 100 * scaleX, 20 * scaleY);
'''

# Replace the previous resize code (midiInSelector... to readPresetBtn...)
old_resize = r'    midiInSelector\.setBounds.*?readPresetBtn\.setBounds[^;]*;'
content = re.sub(old_resize, resize_code, content, flags=re.DOTALL)


with open('Source/PluginEditor.cpp', 'w') as f:
    f.write(content)
