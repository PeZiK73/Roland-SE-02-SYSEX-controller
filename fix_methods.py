with open('Source/PluginEditor.cpp', 'r') as f:
    content = f.read()

methods = '''
SE02_ControllerAudioProcessorEditor::~SE02_ControllerAudioProcessorEditor()
{
}

void SE02_ControllerAudioProcessorEditor::paint (juce::Graphics& g)
{
    g.fillAll (juce::Colours::black);
    if (bgImage.isValid()) {
        g.drawImageAt(bgImage, 0, 0);
    }
}

void SE02_ControllerAudioProcessorEditor::resized()
{
    mainPanel->setBounds(0, 0, 1024, 330);
    // resizer.setBounds(getWidth() - 16, getHeight() - 16, 16, 16);
}

void SE02_ControllerAudioProcessorEditor::addKnob(const juce::String& id, const juce::String& name, int cx, int cy, int size)
{
    auto comp = std::make_unique<AttachedSlider>();
    comp->slider.setSliderStyle(juce::Slider::RotaryHorizontalVerticalDrag);
    comp->slider.setTextBoxStyle(juce::Slider::NoTextBox, false, 0, 0);
    int x = cx - size / 2;
    int y = cy - size / 2;
    comp->slider.setBounds(x, y, size, size);
    comp->slider.setLookAndFeel(&customLookAndFeel);
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
}
'''

# We will remove the garbage appended from the wrong backup, which starts after the closing brace of the constructor
import re
match = re.search(r'// resizer.setBounds\(getWidth\(\) - 16, getHeight\(\) - 16, 16, 16\);\n\}', content, re.DOTALL)
if match:
    content = content[:match.end()] + '\n' + methods
    with open('Source/PluginEditor.cpp', 'w') as f:
        f.write(content)
    print("Methods safely appended!")
else:
    print("Could not find the end of the constructor to append methods!")
