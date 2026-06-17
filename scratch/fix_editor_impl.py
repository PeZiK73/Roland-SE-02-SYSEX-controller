import re

with open('Source/PluginEditor.cpp', 'r') as f:
    content = f.read()

# Restore the correct addKnob implementation and append addSwitch
correct_implementations = """void SE02_ControllerAudioProcessorEditor::addKnob(const juce::String& id, const juce::String& name, int cx, int cy, int size)
{
    auto comp = std::make_unique<AttachedSlider>();
    comp->slider.setSliderStyle(juce::Slider::RotaryHorizontalVerticalDrag);
    comp->slider.setTextBoxStyle(juce::Slider::NoTextBox, false, 0, 0);
    int x = cx - size / 2;
    int y = cy - size / 2;
    comp->slider.setBounds(x, y, size, size);
    comp->slider.setLookAndFeel(&switchLookAndFeel);
    mainPanel->addAndMakeVisible(comp->slider);
    comp->attachment = std::make_unique<juce::AudioProcessorValueTreeState::SliderAttachment>(audioProcessor.apvts, id, comp->slider);
    sliders[id] = std::move(comp);
}

void SE02_ControllerAudioProcessorEditor::addSwitch(const juce::String& id, const juce::String& name, int cx, int cy, int width, int height)
{
    auto comp = std::make_unique<AttachedSlider>();
    comp->slider.setSliderStyle(juce::Slider::LinearVertical);
    comp->slider.setTextBoxStyle(juce::Slider::NoTextBox, false, 0, 0);
    int x = cx - width / 2;
    int y = cy - height / 2;
    comp->slider.setBounds(x, y, width, height + 16);
    comp->slider.setLookAndFeel(&switchLookAndFeel);
    mainPanel->addAndMakeVisible(comp->slider);
    comp->attachment = std::make_unique<juce::AudioProcessorValueTreeState::SliderAttachment>(audioProcessor.apvts, id, comp->slider);
    sliders[id] = std::move(comp);
}"""

# Remove the broken addKnob
content = re.sub(r'void SE02_ControllerAudioProcessorEditor::addKnob.*?^\}', correct_implementations, content, flags=re.DOTALL|re.MULTILINE)

with open('Source/PluginEditor.cpp', 'w') as f:
    f.write(content)
