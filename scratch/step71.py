import re

with open('scratch/generate.py', 'r') as f:
    content = f.read()

bad_state = """void SE02_ControllerAudioProcessor::getStateInformation (juce::MemoryBlock& destData)
{
    std::unique_ptr<juce::Viewport> viewport;
    std::unique_ptr<juce::Component> mainPanel;

    std::vector<std::unique_ptr<AttachedSlider>> sliders;
    std::vector<std::unique_ptr<juce::Label>> labels;

    juce::ComboBox midiInBox;
    juce::ComboBox midiOutBox;
    juce::TextButton readPresetBtn;
    juce::TextButton showValuesBtn;
};"""

good_state = """void SE02_ControllerAudioProcessor::getStateInformation (juce::MemoryBlock& destData)
{
    auto state = apvts.copyState();
    std::unique_ptr<juce::XmlElement> xml (state.createXml());
    copyXmlToBinary (*xml, destData);
}"""

content = content.replace(bad_state, good_state)

# Now fix the PluginEditor.h template
bad_h = """    std::unique_ptr<juce::Viewport> viewport;
    std::unique_ptr<juce::Component> mainPanel;

    std::vector<std::unique_ptr<AttachedSlider>> sliders;
    std::vector<std::unique_ptr<juce::Label>> labels;
};
"""

good_h = """    std::unique_ptr<juce::Viewport> viewport;
    std::unique_ptr<juce::Component> mainPanel;

    std::vector<std::unique_ptr<AttachedSlider>> sliders;
    std::vector<std::unique_ptr<juce::Label>> labels;

    juce::ComboBox midiInBox;
    juce::ComboBox midiOutBox;
    juce::TextButton readPresetBtn;
    juce::TextButton showValuesBtn;
};
"""

# There might be multiple occurrences of the ad_h text if it matched getStateInformation earlier! Wait, getStateInformation didn't have };
# Let's just do a direct replacement
content = content.replace(bad_h, good_h)

with open('scratch/generate.py', 'w') as f:
    f.write(content)
