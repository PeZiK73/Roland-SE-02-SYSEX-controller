import re

with open('Source/PluginEditor.cpp', 'r') as f:
    content = f.read()

setup_code = '''
    addAndMakeVisible(midiInSelector);
    midiInSelector.setTextWhenNothingSelected("MIDI In...");
    midiInSelector.addItemList(getMidiInputNames(), 1);
    midiInSelector.onChange = [this] { audioProcessor.openMidiInput(midiInSelector.getText()); };

    addAndMakeVisible(midiOutSelector);
    midiOutSelector.setTextWhenNothingSelected("MIDI Out...");
    midiOutSelector.addItemList(getMidiOutputNames(), 1);
    midiOutSelector.onChange = [this] { audioProcessor.openMidiOutput(midiOutSelector.getText()); };

    addAndMakeVisible(readPresetBtn);
    readPresetBtn.onClick = [this] { audioProcessor.requestSysExPreset(); };

    addAndMakeVisible(resizer);
'''

content = content.replace("    addAndMakeVisible(resizer);", setup_code)

resize_code = '''
    int w = getWidth();
    int h = getHeight();
    
    // Original design was 1024x330. We scale positions.
    float scaleX = w / 1024.0f;
    float scaleY = h / 330.0f;

    resizer.setBounds(w - 16, h - 16, 16, 16);
    
    midiInSelector.setBounds(w - (450 * scaleX), h - (25 * scaleY), 150 * scaleX, 20 * scaleY);
    midiOutSelector.setBounds(w - (290 * scaleX), h - (25 * scaleY), 150 * scaleX, 20 * scaleY);
    readPresetBtn.setBounds(w - (130 * scaleX), h - (25 * scaleY), 100 * scaleX, 20 * scaleY);
}
'''

content = re.sub(r'    resizer\.setBounds\(getWidth\(\) - 16, getHeight\(\) - 16, 16, 16\);\n}', resize_code, content)

with open('Source/PluginEditor.cpp', 'w') as f:
    f.write(content)
