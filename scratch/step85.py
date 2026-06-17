import re

with open('Source/PluginEditor.cpp', 'r') as f:
    content = f.read()

# Comment out MIDI device querying
content = content.replace(
    'auto inDevices = juce::MidiInput::getAvailableDevices();',
    '/* auto inDevices = juce::MidiInput::getAvailableDevices();'
)
content = content.replace(
    'midiInBox.onChange = [this]() {',
    '*/\n    /* midiInBox.onChange = [this]() {'
)
content = content.replace(
    'readPresetBtn.setBounds(890, 302, 100, 24);',
    '*/\n    readPresetBtn.setBounds(890, 302, 100, 24);'
)

content = content.replace(
    'midiInBox.setBounds(630, 302, 120, 24);',
    '// midiInBox.setBounds(630, 302, 120, 24);'
)
content = content.replace(
    'midiInBox.setTextWhenNothingSelected("MIDI Input...");',
    '// midiInBox.setTextWhenNothingSelected("MIDI Input...");'
)
content = content.replace(
    'mainPanel->addAndMakeVisible(midiInBox);',
    '// mainPanel->addAndMakeVisible(midiInBox);'
)

content = content.replace(
    'midiOutBox.setBounds(760, 302, 120, 24);',
    '// midiOutBox.setBounds(760, 302, 120, 24);'
)
content = content.replace(
    'midiOutBox.setTextWhenNothingSelected("MIDI Output...");',
    '// midiOutBox.setTextWhenNothingSelected("MIDI Output...");'
)
content = content.replace(
    'mainPanel->addAndMakeVisible(midiOutBox);',
    '// mainPanel->addAndMakeVisible(midiOutBox);'
)

# Also remove the debug logs I added!
content = content.replace('#include <fstream>\nextern void logdbg(const char* m);\n', '')
content = content.replace('    logdbg("EDITOR CONSTRUCTOR START");\n', '')
content = content.replace('    logdbg("ADDING KNOBS");\n', '')
content = content.replace('    logdbg("ADDING SWITCHES");\n', '')
content = content.replace('    logdbg("EDITOR CONSTRUCTOR FINISHED");\n', '')

with open('Source/PluginEditor.cpp', 'w') as f:
    f.write(content)

with open('Source/PluginProcessor.cpp', 'r') as f:
    p_content = f.read()

p_content = p_content.replace('#include <fstream>\nvoid logdbg(const char* m) { std::ofstream f("C:/TEMP/crash_debug.txt", std::ios::app); f << m << std::endl; }\n', '')
p_content = p_content.replace('    logdbg("START CONSTRUCTOR");\n', '')
p_content = p_content.replace('    logdbg("CLEARED CCPARAMS");\n', '')
p_content = p_content.replace('    logdbg("DONE SYXPARAMMAP");\n', '')
p_content = p_content.replace('    logdbg("ABOUT TO START TIMER");\n', '')
p_content = p_content.replace('    logdbg("CONSTRUCTOR FINISHED");\n', '')
p_content = p_content.replace('    logdbg("CALLING createEditor");\n', '')
p_content = p_content.replace('    logdbg("START DESTRUCTOR");\n', '')
p_content = p_content.replace('    logdbg("STOPPED TIMER");\n', '')
p_content = p_content.replace('    logdbg("DESTRUCTOR FINISHED");\n', '')
p_content = p_content.replace('    logdbg("RELEASE RESOURCES");\n', '')
p_content = p_content.replace('    logdbg("START PREPARETOPLAY");\n', '')
p_content = p_content.replace('    logdbg("START PROCESSBLOCK");\n', '')
p_content = p_content.replace('    logdbg("START TIMERCALLBACK");\n', '')

with open('Source/PluginProcessor.cpp', 'w') as f:
    f.write(p_content)

print("Removed MIDI polling and debug logs")
