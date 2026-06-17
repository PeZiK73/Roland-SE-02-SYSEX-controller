import re

with open('Source/PluginProcessor.cpp', 'r') as f:
    content = f.read()

content = content.replace(
    'SE02_ControllerAudioProcessor::SE02_ControllerAudioProcessor()',
    '#include <fstream>\nvoid logdbg(const char* m) { std::ofstream f("C:/TEMP/crash_debug.txt", std::ios::app); f << m << std::endl; }\nSE02_ControllerAudioProcessor::SE02_ControllerAudioProcessor()'
)

# Insert logs into the constructor
content = content.replace('    for (int i = 0; i < 128; ++i)', '    logdbg("START CONSTRUCTOR");\n    for (int i = 0; i < 128; ++i)')
content = content.replace('    ccParams.clear();', '    logdbg("CLEARED CCPARAMS");\n    ccParams.clear();')
content = content.replace('    syxParamMap[102] = "DLY_AMOUNT";', '    syxParamMap[102] = "DLY_AMOUNT";\n    logdbg("DONE SYXPARAMMAP");')
content = content.replace('    startTimerHz(30);', '    logdbg("ABOUT TO START TIMER");\n    startTimerHz(30);\n    logdbg("CONSTRUCTOR FINISHED");')
content = content.replace('juce::AudioProcessorEditor* SE02_ControllerAudioProcessor::createEditor() {', 'juce::AudioProcessorEditor* SE02_ControllerAudioProcessor::createEditor() {\n    logdbg("CALLING createEditor");')

with open('Source/PluginProcessor.cpp', 'w') as f:
    f.write(content)

with open('Source/PluginEditor.cpp', 'r') as f:
    ed_content = f.read()

ed_content = '#include <fstream>\nextern void logdbg(const char* m);\n' + ed_content
ed_content = ed_content.replace('SE02_ControllerAudioProcessorEditor::SE02_ControllerAudioProcessorEditor', 'logdbg("EDITOR CONSTRUCTOR START");\nSE02_ControllerAudioProcessorEditor::SE02_ControllerAudioProcessorEditor')
ed_content = ed_content.replace('    addKnob("GLIDE",', '    logdbg("ADDING KNOBS");\n    addKnob("GLIDE",')
ed_content = ed_content.replace('    addSwitch("LFO_MW_OSC",', '    logdbg("ADDING SWITCHES");\n    addSwitch("LFO_MW_OSC",')
ed_content = ed_content.replace('    addKnob("DLY_AMOUNT", "AMOUNT", dx, r3, kSize);\n}', '    addKnob("DLY_AMOUNT", "AMOUNT", dx, r3, kSize);\n    logdbg("EDITOR CONSTRUCTOR FINISHED");\n}')

with open('Source/PluginEditor.cpp', 'w') as f:
    f.write(ed_content)

print("Injected debug statements.")
