import re

with open('Source/PluginEditor.h', 'r') as f:
    content = f.read()

content = re.sub(r'std::vector<std::unique_ptr<juce::Label>> labels;\s*};', 'std::vector<std::unique_ptr<juce::Label>> labels;\njuce::ComboBox midiInBox;\njuce::ComboBox midiOutBox;\njuce::TextButton readPresetBtn;\njuce::TextButton showValuesBtn;\n};', content)

with open('Source/PluginEditor.h', 'w') as f:
    f.write(content)

with open('Source/PluginEditor.cpp', 'r') as f:
    content2 = f.read()

bad_switch = """void SE02_ControllerAudioProcessorEditor::addSwitch(const juce::String& id, const juce::String& name, int cx, int cy, int width, int height)
{
    auto comp = std::make_unique<AttachedSlider>();
    comp->slider.setSliderStyle(juce::Slider::LinearVertical);
    comp->slider.setTextBoxStyle(juce::Slider::NoTextBox, false, 0, 0);
    mainPanel->addAndMakeVisible(comp->slider);

    comp->slider.setBounds(x, y, width, height);"""

good_switch = """void SE02_ControllerAudioProcessorEditor::addSwitch(const juce::String& id, const juce::String& name, int cx, int cy, int width, int height)
{
    auto comp = std::make_unique<AttachedSlider>();
    comp->slider.setSliderStyle(juce::Slider::LinearVertical);
    comp->slider.setTextBoxStyle(juce::Slider::NoTextBox, false, 0, 0);
    mainPanel->addAndMakeVisible(comp->slider);

    int x = cx - width/2;
    int y = cy - height/2;
    comp->slider.setBounds(x, y, width, height);"""

if bad_switch in content2:
    content2 = content2.replace(bad_switch, good_switch)
    with open('Source/PluginEditor.cpp', 'w') as f:
        f.write(content2)
else:
    print("Could not find bad_switch in PluginEditor.cpp")
