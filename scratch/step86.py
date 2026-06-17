import re

with open('Source/PluginProcessor.cpp', 'r') as f:
    content = f.read()

# Fix releaseResources
content = content.replace(
    'void SE02_ControllerAudioProcessor::releaseResources()\n{\n    logdbg("RELEASE RESOURCES"); {}',
    'void SE02_ControllerAudioProcessor::releaseResources()\n{}'
)

# Remove the rest of the debug logs to clean it up
content = content.replace('#include <fstream>\nvoid logdbg(const char* m) { std::ofstream f("C:/TEMP/crash_debug.txt", std::ios::app); f << m << std::endl; }\n', '')
content = content.replace('    logdbg("START CONSTRUCTOR");\n', '')
content = content.replace('    logdbg("CLEARED CCPARAMS");\n', '')
content = content.replace('    logdbg("DONE SYXPARAMMAP");\n', '')
content = content.replace('    logdbg("ABOUT TO START TIMER");\n', '')
content = content.replace('    logdbg("CONSTRUCTOR FINISHED");\n', '')
content = content.replace('    logdbg("CALLING createEditor");\n', '')
content = content.replace('    logdbg("START DESTRUCTOR");\n', '')
content = content.replace('    logdbg("STOPPED TIMER");\n', '')
content = content.replace('    logdbg("DESTRUCTOR FINISHED");\n', '')
content = content.replace('    logdbg("START PREPARETOPLAY");\n', '')
content = content.replace('    logdbg("START PROCESSBLOCK");\n', '')
content = content.replace('    logdbg("START TIMERCALLBACK");\n', '')

with open('Source/PluginProcessor.cpp', 'w') as f:
    f.write(content)

with open('Source/PluginEditor.cpp', 'r') as f:
    ed_content = f.read()

# Fix Editor syntax error if any
ed_content = ed_content.replace('    logdbg("EDITOR CONSTRUCTOR START");\n', '')
ed_content = ed_content.replace('#include <fstream>\nextern void logdbg(const char* m);\n', '')

# REMOVE MIDI INPUT BOXES FROM EDITOR (THE REAL FIX!)
ed_content = ed_content.replace(
    'auto inDevices = juce::MidiInput::getAvailableDevices();',
    '/* auto inDevices = juce::MidiInput::getAvailableDevices();'
)
ed_content = ed_content.replace(
    'midiInBox.onChange = [this]() {',
    '*/\n    /* midiInBox.onChange = [this]() {'
)
ed_content = ed_content.replace(
    'readPresetBtn.setBounds(890, 302, 100, 24);',
    '*/\n    readPresetBtn.setBounds(890, 302, 100, 24);'
)

ed_content = ed_content.replace(
    'midiInBox.setBounds(630, 302, 120, 24);',
    '// midiInBox.setBounds(630, 302, 120, 24);'
)
ed_content = ed_content.replace(
    'midiInBox.setTextWhenNothingSelected("MIDI Input...");',
    '// midiInBox.setTextWhenNothingSelected("MIDI Input...");'
)
ed_content = ed_content.replace(
    'mainPanel->addAndMakeVisible(midiInBox);',
    '// mainPanel->addAndMakeVisible(midiInBox);'
)

ed_content = ed_content.replace(
    'midiOutBox.setBounds(760, 302, 120, 24);',
    '// midiOutBox.setBounds(760, 302, 120, 24);'
)
ed_content = ed_content.replace(
    'midiOutBox.setTextWhenNothingSelected("MIDI Output...");',
    '// midiOutBox.setTextWhenNothingSelected("MIDI Output...");'
)
ed_content = ed_content.replace(
    'mainPanel->addAndMakeVisible(midiOutBox);',
    '// mainPanel->addAndMakeVisible(midiOutBox);'
)

with open('Source/PluginEditor.cpp', 'w') as f:
    f.write(ed_content)

print("Fixed syntax and removed MIDI polling")
