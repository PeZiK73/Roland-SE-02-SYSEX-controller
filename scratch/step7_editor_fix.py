import re

with open('Source/PluginEditor.cpp', 'r') as f:
    content = f.read()

# 1. Update loadPresetFromFile math
content = content.replace("float vals[6] = {0.0f, 26.0f, 51.0f, 77.0f, 102.0f, 127.0f};", "float vals[6] = {10.0f, 32.0f, 53.0f, 74.0f, 95.0f, 116.0f};")

# 2. Fix setSize ordering in constructor
constructor_old = '''SE02_ControllerAudioProcessorEditor::SE02_ControllerAudioProcessorEditor (SE02_ControllerAudioProcessor& p)
    : AudioProcessorEditor (&p), audioProcessor (p)
{
    setSize (2048, 660);
    mainPanel = std::make_unique<MainPanel>();
    mainPanel->setBounds(0, 0, 1024, 330);
    addAndMakeVisible(mainPanel.get());'''

constructor_new = '''SE02_ControllerAudioProcessorEditor::SE02_ControllerAudioProcessorEditor (SE02_ControllerAudioProcessor& p)
    : AudioProcessorEditor (&p), audioProcessor (p)
{
    mainPanel = std::make_unique<MainPanel>();
    mainPanel->setBounds(0, 0, 1024, 330);
    addAndMakeVisible(mainPanel.get());'''

content = content.replace(constructor_old, constructor_new)

# Add setSize (2048, 660); to the end of constructor
# Find where the constructor ends. It ends at     startTimer(50);\n}
constructor_end_old = '''    constrainer.setFixedAspectRatio(1024.0 / 330.0);
    constrainer.setSizeLimits(1024, 330, 2048, 660);

    startTimer(50);
}'''

constructor_end_new = '''    constrainer.setFixedAspectRatio(1024.0 / 330.0);
    constrainer.setSizeLimits(1024, 330, 2048, 660);

    startTimer(50);
    
    setSize (2048, 660); // Call this AFTER mainPanel is created so resized() scales it!
}'''

content = content.replace(constructor_end_old, constructor_end_new)

with open('Source/PluginEditor.cpp', 'w') as f:
    f.write(content)
