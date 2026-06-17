import sys

with open('Source/PluginEditor.h', 'r') as f:
    content = f.read()

bad_str = """    std::vector<std::unique_ptr<AttachedSlider>> sliders;
    std::vector<std::unique_ptr<juce::Label>> labels;
};"""

good_str = """    std::vector<std::unique_ptr<AttachedSlider>> sliders;
    std::vector<std::unique_ptr<juce::Label>> labels;

    juce::ComboBox midiInBox;
    juce::ComboBox midiOutBox;
    juce::TextButton readPresetBtn;
    juce::TextButton showValuesBtn;
};"""

if bad_str in content:
    content = content.replace(bad_str, good_str)
    with open('Source/PluginEditor.h', 'w') as f:
        f.write(content)
    print("Fixed PluginEditor.h successfully")
else:
    print("Could not find bad_str in PluginEditor.h")
