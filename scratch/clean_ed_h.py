import re

def clean_editor_h():
    with open('Source/PluginEditor.h', 'r') as f:
        content = f.read()

    to_remove = [
        r'    juce::ComboBox midiInBox;\n',
        r'    juce::ComboBox midiOutBox;\n',
        r'    juce::TextButton refreshMidiBtn;\n',
        r'    juce::TextButton readPresetBtn;\n',
        r'    juce::ToggleButton showValuesBtn;\n'
    ]
    
    for pat in to_remove:
        content = re.sub(pat, '', content)

    with open('Source/PluginEditor.h', 'w') as f:
        f.write(content)

clean_editor_h()
print("Editor.h cleaned!")
