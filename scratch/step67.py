import re

with open('scratch/generate.py', 'r') as f:
    content = f.read()

# Fix the duplicate 'comp' inside addKnob by finding the addKnob definition and removing the duplicated auto comp...
# Wait, let's just replace the body of addKnob.
bad_addKnob = """void SE02_ControllerAudioProcessorEditor::addKnob(const juce::String& id, const juce::String& name, int cx, int cy, int size)
{
    auto comp = std::make_unique<AttachedSlider>();
    comp->slider.setSliderStyle(juce::Slider::RotaryHorizontalVerticalDrag);
    comp->slider.setTextBoxStyle(juce::Slider::NoTextBox, false, 0, 0);
    mainPanel->addAndMakeVisible(comp->slider);

    auto comp = std::make_unique<AttachedSlider>();
    comp->slider.setSliderStyle(juce::Slider::LinearVertical);
    comp->slider.setTextBoxStyle(juce::Slider::NoTextBox, false, 0, 0);
    mainPanel->addAndMakeVisible(comp->slider);

    comp->slider.setBounds(cx - size/2, cy - size/2, size, size);
    comp->attachment = std::make_unique<juce::AudioProcessorValueTreeState::SliderAttachment>(audioProcessor.apvts, id, comp->slider);
    
    // Create label
    auto label = std::make_unique<juce::Label>("", name);
    label->setJustificationType(juce::Justification::centred);
    label->setBounds(cx - size/2, cy + size/2 + 2, size, 20);
    mainPanel->addAndMakeVisible(*label);
    
    sliders.push_back(std::move(comp));
    labels.push_back(std::move(label));
}"""

good_addKnob = """void SE02_ControllerAudioProcessorEditor::addKnob(const juce::String& id, const juce::String& name, int cx, int cy, int size)
{
    auto comp = std::make_unique<AttachedSlider>();
    comp->slider.setSliderStyle(juce::Slider::RotaryHorizontalVerticalDrag);
    comp->slider.setTextBoxStyle(juce::Slider::NoTextBox, false, 0, 0);
    mainPanel->addAndMakeVisible(comp->slider);

    comp->slider.setBounds(cx - size/2, cy - size/2, size, size);
    comp->attachment = std::make_unique<juce::AudioProcessorValueTreeState::SliderAttachment>(audioProcessor.apvts, id, comp->slider);
    
    // Create label
    auto label = std::make_unique<juce::Label>("", name);
    label->setJustificationType(juce::Justification::centred);
    label->setBounds(cx - size/2, cy + size/2 + 2, size, 20);
    mainPanel->addAndMakeVisible(*label);
    
    sliders.push_back(std::move(comp));
    labels.push_back(std::move(label));
}"""

if bad_addKnob in content:
    content = content.replace(bad_addKnob, good_addKnob)
else:
    print("Could not find bad addKnob")

# Same for addSwitch
bad_addSwitch = """void SE02_ControllerAudioProcessorEditor::addSwitch(const juce::String& id, const juce::String& name, int cx, int cy, int width, int height)
{
    auto comp = std::make_unique<AttachedSlider>();
    comp->slider.setSliderStyle(juce::Slider::LinearVertical);
    comp->slider.setTextBoxStyle(juce::Slider::NoTextBox, false, 0, 0);
    mainPanel->addAndMakeVisible(comp->slider);

    int x = cx - width/2;
    int y = cy - height/2;
    
    auto comp = std::make_unique<AttachedSlider>();
    comp->slider.setSliderStyle(juce::Slider::LinearVertical);
    comp->slider.setTextBoxStyle(juce::Slider::NoTextBox, false, 0, 0);
    mainPanel->addAndMakeVisible(comp->slider);

    int x = cx - width/2;
    int y = cy - height/2;
    comp->slider.setBounds(x, y, width, height);
    comp->attachment = std::make_unique<juce::AudioProcessorValueTreeState::SliderAttachment>(audioProcessor.apvts, id, comp->slider);
    
    auto label = std::make_unique<juce::Label>("", name);
    label->setJustificationType(juce::Justification::centred);
    label->setBounds(cx - width/2 - 10, cy + height/2 + 2, width + 20, 20);
    mainPanel->addAndMakeVisible(*label);
    
    sliders.push_back(std::move(comp));
    labels.push_back(std::move(label));
}"""

good_addSwitch = """void SE02_ControllerAudioProcessorEditor::addSwitch(const juce::String& id, const juce::String& name, int cx, int cy, int width, int height)
{
    auto comp = std::make_unique<AttachedSlider>();
    comp->slider.setSliderStyle(juce::Slider::LinearVertical);
    comp->slider.setTextBoxStyle(juce::Slider::NoTextBox, false, 0, 0);
    mainPanel->addAndMakeVisible(comp->slider);

    int x = cx - width/2;
    int y = cy - height/2;
    comp->slider.setBounds(x, y, width, height);
    comp->attachment = std::make_unique<juce::AudioProcessorValueTreeState::SliderAttachment>(audioProcessor.apvts, id, comp->slider);
    
    auto label = std::make_unique<juce::Label>("", name);
    label->setJustificationType(juce::Justification::centred);
    label->setBounds(cx - width/2 - 10, cy + height/2 + 2, width + 20, 20);
    mainPanel->addAndMakeVisible(*label);
    
    sliders.push_back(std::move(comp));
    labels.push_back(std::move(label));
}"""

if bad_addSwitch in content:
    content = content.replace(bad_addSwitch, good_addSwitch)
else:
    print("Could not find bad addSwitch")


# And add midiInBox and midiOutBox to PluginEditor.h
bad_h = """    std::unique_ptr<juce::Viewport> viewport;
    std::unique_ptr<juce::Component> mainPanel;

    std::vector<std::unique_ptr<AttachedSlider>> sliders;
    std::vector<std::unique_ptr<juce::Label>> labels;"""

good_h = """    std::unique_ptr<juce::Viewport> viewport;
    std::unique_ptr<juce::Component> mainPanel;

    std::vector<std::unique_ptr<AttachedSlider>> sliders;
    std::vector<std::unique_ptr<juce::Label>> labels;
    
    juce::ComboBox midiInBox;
    juce::ComboBox midiOutBox;"""

if bad_h in content:
    content = content.replace(bad_h, good_h)
else:
    print("Could not find bad h")

with open('scratch/generate.py', 'w') as f:
    f.write(content)

print("Fixed generate.py")
