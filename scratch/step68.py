import re

with open('scratch/generate.py', 'r') as f:
    content = f.read()

# Fix addKnob
content = re.sub(r'auto comp = std::make_unique<AttachedSlider>\(\);\s*comp->slider\.setSliderStyle.*?mainPanel->addAndMakeVisible\(comp->slider\);\s*auto comp = std::make_unique<AttachedSlider>\(\);', 'auto comp = std::make_unique<AttachedSlider>();', content, flags=re.DOTALL)

# Fix addSwitch
content = re.sub(r'auto comp = std::make_unique<AttachedSlider>\(\);\s*comp->slider\.setSliderStyle.*?mainPanel->addAndMakeVisible\(comp->slider\);\s*int x = cx - width/2;\s*int y = cy - height/2;\s*auto comp = std::make_unique<AttachedSlider>\(\);', 'auto comp = std::make_unique<AttachedSlider>();', content, flags=re.DOTALL)

# Add midiInBox to header
content = re.sub(r'std::vector<std::unique_ptr<juce::Label>> labels;', 'std::vector<std::unique_ptr<juce::Label>> labels;\n    juce::ComboBox midiInBox;\n    juce::ComboBox midiOutBox;', content)

with open('scratch/generate.py', 'w') as f:
    f.write(content)
