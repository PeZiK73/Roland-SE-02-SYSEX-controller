import re

with open('scratch/generate.py', 'r') as f:
    content = f.read()

bad_h = """    std::unique_ptr<juce::Viewport> viewport;
    std::unique_ptr<juce::Component> mainPanel;

    std::vector<std::unique_ptr<AttachedSlider>> sliders;
    std::vector<std::unique_ptr<juce::Label>> labels;
};"""

good_h = """    std::unique_ptr<juce::Viewport> viewport;
    std::unique_ptr<juce::Component> mainPanel;

    std::vector<std::unique_ptr<AttachedSlider>> sliders;
    std::vector<std::unique_ptr<juce::Label>> labels;

    juce::ComboBox midiInBox;
    juce::ComboBox midiOutBox;
    juce::TextButton readPresetBtn;
    juce::TextButton showValuesBtn;
};"""

content = content.replace(bad_h, good_h)

with open('scratch/generate.py', 'w') as f:
    f.write(content)
