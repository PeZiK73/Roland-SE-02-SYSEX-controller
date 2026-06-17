import re

with open('Source/PluginEditor.cpp', 'r') as f:
    content = f.read()

resize_code = '''
    presetPrevBtn.setBounds(10 * scaleX, h - (25 * scaleY), 20 * scaleX, 20 * scaleY);
    presetLabel.setBounds(30 * scaleX, h - (25 * scaleY), 75 * scaleX, 20 * scaleY);
    presetNextBtn.setBounds(105 * scaleX, h - (25 * scaleY), 20 * scaleX, 20 * scaleY);

    bankPrevBtn.setBounds(135 * scaleX, h - (25 * scaleY), 20 * scaleX, 20 * scaleY);
    bankLabel.setBounds(155 * scaleX, h - (25 * scaleY), 65 * scaleX, 20 * scaleY);
    bankNextBtn.setBounds(220 * scaleX, h - (25 * scaleY), 20 * scaleX, 20 * scaleY);

    browseBtn.setBounds(250 * scaleX, h - (25 * scaleY), 70 * scaleX, 20 * scaleY);
    
    // Right side
    midiInSelector.setBounds(w - (590 * scaleX), h - (25 * scaleY), 130 * scaleX, 20 * scaleY);
    midiOutSelector.setBounds(w - (450 * scaleX), h - (25 * scaleY), 130 * scaleX, 20 * scaleY);
    showValuesBtn.setBounds(w - (310 * scaleX), h - (25 * scaleY), 130 * scaleX, 20 * scaleY);
    savePresetBtn.setBounds(w - (175 * scaleX), h - (25 * scaleY), 70 * scaleX, 20 * scaleY);
    readPresetBtn.setBounds(w - (100 * scaleX), h - (25 * scaleY), 90 * scaleX, 20 * scaleY);
'''

# Replace the layout
old_resize = r'    presetPrevBtn\.setBounds.*?readPresetBtn\.setBounds[^;]*;'
content = re.sub(old_resize, resize_code, content, flags=re.DOTALL)

with open('Source/PluginEditor.cpp', 'w') as f:
    f.write(content)
