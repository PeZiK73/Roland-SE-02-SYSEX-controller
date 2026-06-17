with open('Source/PluginEditor.cpp', 'r') as f:
    content = f.read()

bad_addKnob = '''void SE02_ControllerAudioProcessorEditor::addKnob(const juce::String& id, const juce::String& name, int cx, int cy, int size)
{
    auto comp = std::make_unique<AttachedSlider>();
    comp->slider.setSliderStyle(juce::Slider::LinearVertical);
    comp->slider.setTextBoxStyle(juce::Slider::NoTextBox, false, 0, 0);
    int x = cx - 15;
    int y = cy - 20;
    comp->slider.setBounds(x, y, 30, 40 + 16);
    comp->slider.setLookAndFeel(&switchLookAndFeel);'''

good_addKnob = '''void SE02_ControllerAudioProcessorEditor::addKnob(const juce::String& id, const juce::String& name, int cx, int cy, int size)
{
    auto comp = std::make_unique<AttachedSlider>();
    comp->slider.setSliderStyle(juce::Slider::RotaryHorizontalVerticalDrag);
    comp->slider.setTextBoxStyle(juce::Slider::NoTextBox, false, 0, 0);
    int x = cx - size / 2;
    int y = cy - size / 2;
    comp->slider.setBounds(x, y, size, size);
    comp->slider.setLookAndFeel(&customLookAndFeel);'''

if bad_addKnob in content:
    content = content.replace(bad_addKnob, good_addKnob)
    with open('Source/PluginEditor.cpp', 'w') as f:
        f.write(content)
    print('Fixed addKnob in PluginEditor.cpp')
else:
    print('bad_addKnob not found')
