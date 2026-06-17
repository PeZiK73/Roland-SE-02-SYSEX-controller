import re

# Fix PluginEditor.h
with open('Source/PluginEditor.h', 'r') as f:
    h_content = f.read()

# We need to add the UI elements if they are missing
if "juce::ComboBox midiInBox;" not in h_content:
    # find where to inject it
    h_content = re.sub(r'std::vector<std::unique_ptr<AttachedSlider>> sliders;\s*std::vector<std::unique_ptr<juce::Label>> labels;\s*};', 'std::vector<std::unique_ptr<AttachedSlider>> sliders;\n    std::vector<std::unique_ptr<juce::Label>> labels;\n\n    juce::ComboBox midiInBox;\n    juce::ComboBox midiOutBox;\n    juce::TextButton readPresetBtn;\n    juce::TextButton showValuesBtn;\n};', h_content)
    # Wait, earlier I saw that sliders is actually std::map<juce::String, std::unique_ptr<AttachedSlider>> sliders;!
    # Let me just check the class end
    h_content = re.sub(r'std::map<juce::String, std::unique_ptr<AttachedSlider>> sliders;\s*};', 'std::map<juce::String, std::unique_ptr<AttachedSlider>> sliders;\n\n    juce::ComboBox midiInBox;\n    juce::ComboBox midiOutBox;\n    juce::TextButton readPresetBtn;\n    juce::TextButton showValuesBtn;\n};', h_content)
    with open('Source/PluginEditor.h', 'w') as f:
        f.write(h_content)

# Fix PluginEditor.cpp
with open('Source/PluginEditor.cpp', 'r') as f:
    cpp_content = f.read()

# Replace the broken addKnob and addSwitch
good_knob_and_switch = """void SE02_ControllerAudioProcessorEditor::addKnob(const juce::String& id, const juce::String& name, int cx, int cy, int size)
{
    auto comp = std::make_unique<AttachedSlider>();
    comp->slider.setSliderStyle(juce::Slider::RotaryHorizontalVerticalDrag);
    comp->slider.setTextBoxStyle(juce::Slider::NoTextBox, false, 0, 0);
    comp->slider.setBounds(cx - size/2, cy - size/2, size, size);
    mainPanel->addAndMakeVisible(comp->slider);

    comp->attachment = std::make_unique<juce::AudioProcessorValueTreeState::SliderAttachment>(
        audioProcessor.apvts, id, comp->slider);

    sliders[id] = std::move(comp);
}

void SE02_ControllerAudioProcessorEditor::addSwitch(const juce::String& id, const juce::String& name, int cx, int cy, int width, int height)
{
    auto comp = std::make_unique<AttachedSlider>();
    comp->slider.setSliderStyle(juce::Slider::LinearVertical);
    comp->slider.setTextBoxStyle(juce::Slider::NoTextBox, false, 0, 0);
    comp->slider.setBounds(cx - width/2, cy - height/2, width, height + 16);
    comp->slider.setLookAndFeel(&switchLookAndFeel);
    mainPanel->addAndMakeVisible(comp->slider);

    comp->attachment = std::make_unique<juce::AudioProcessorValueTreeState::SliderAttachment>(
        audioProcessor.apvts, id, comp->slider);

    sliders[id] = std::move(comp);
}"""

# Find everything from "void SE02_ControllerAudioProcessorEditor::addKnob" to "void SE02_ControllerAudioProcessorEditor::paint"
cpp_content = re.sub(r'void SE02_ControllerAudioProcessorEditor::addKnob\(.*?(?=void SE02_ControllerAudioProcessorEditor::paint)', good_knob_and_switch + '\n\n', cpp_content, flags=re.DOTALL)

with open('Source/PluginEditor.cpp', 'w') as f:
    f.write(cpp_content)
