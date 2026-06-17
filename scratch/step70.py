import re

with open('scratch/generate.py', 'r') as f:
    content = f.read()

# Fix addSwitch
content = re.sub(r'void SE02_ControllerAudioProcessorEditor::addSwitch\(const juce::String& id, const juce::String& name, int cx, int cy, int width, int height\)\s*\{\s*auto comp = std::make_unique<AttachedSlider>\(\);\s*comp->slider\.setBounds\(x, y, width, height\);', 'void SE02_ControllerAudioProcessorEditor::addSwitch(const juce::String& id, const juce::String& name, int cx, int cy, int width, int height)\n{\n    auto comp = std::make_unique<AttachedSlider>();\n    comp->slider.setSliderStyle(juce::Slider::LinearVertical);\n    comp->slider.setTextBoxStyle(juce::Slider::NoTextBox, false, 0, 0);\n    mainPanel->addAndMakeVisible(comp->slider);\n\n    int x = cx - width/2;\n    int y = cy - height/2;\n    comp->slider.setBounds(x, y, width, height);', content)

with open('scratch/generate.py', 'w') as f:
    f.write(content)
