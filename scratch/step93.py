import re

with open('Source/PluginEditor.h', 'r') as f:
    h_content = f.read()
h_content = h_content.replace('juce::ComboBox midiInBox;\n', '')
h_content = h_content.replace('    juce::ComboBox midiOutBox;\n', '')
with open('Source/PluginEditor.h', 'w') as f:
    f.write(h_content)

with open('Source/PluginEditor.cpp', 'r') as f:
    c_content = f.read()

midi_init_code = """    midiInBox.setBounds(630, 302, 120, 24);
    midiInBox.setTextWhenNothingSelected("MIDI Input...");
    mainPanel->addAndMakeVisible(midiInBox);

    midiOutBox.setBounds(760, 302, 120, 24);
    midiOutBox.setTextWhenNothingSelected("MIDI Output...");
    mainPanel->addAndMakeVisible(midiOutBox);

    auto inDevices = juce::MidiInput::getAvailableDevices();
    for (auto& dev : inDevices) midiInBox.addItem(dev.name, midiInBox.getNumItems() + 1);
    
    auto outDevices = juce::MidiOutput::getAvailableDevices();
    for (auto& dev : outDevices) midiOutBox.addItem(dev.name, midiOutBox.getNumItems() + 1);
    
    midiInBox.onChange = [this]() {
        auto devs = juce::MidiInput::getAvailableDevices();
        int idx = midiInBox.getSelectedItemIndex();
        if (idx >= 0 && idx < devs.size()) audioProcessor.openMidiInput(devs[idx].identifier);
    };
    
    midiOutBox.onChange = [this]() {
        auto devs = juce::MidiOutput::getAvailableDevices();
        int idx = midiOutBox.getSelectedItemIndex();
        if (idx >= 0 && idx < devs.size()) audioProcessor.openMidiOutput(devs[idx].identifier);
    };"""

c_content = c_content.replace(midi_init_code, '')

with open('Source/PluginEditor.cpp', 'w') as f:
    f.write(c_content)

with open('Source/PluginProcessor.cpp', 'r') as f:
    content = f.read()

timer_loop_old = """    for (auto& cp : ccParams)
    {
        float hwVal = incomingCcValues[cp.ccNumber].exchange(-1.0f);"""
timer_loop_new = """    for (auto& cp : ccParams)
    {
        if (cp.ccNumber >= 0 && cp.ccNumber < 128) {
            float hwVal = incomingCcValues[cp.ccNumber].exchange(-1.0f);"""
content = content.replace(timer_loop_old, timer_loop_new)

timer_loop_end_old = """            if (auto* param = apvts.getParameter(cp.id))
            {
                param->setValueNotifyingHost(param->convertTo0to1(hwVal));
            }
        }
    }"""
timer_loop_end_new = """            if (auto* param = apvts.getParameter(cp.id))
            {
                param->setValueNotifyingHost(param->convertTo0to1(hwVal));
            }
        }
        }
    }"""
content = content.replace(timer_loop_end_old, timer_loop_end_new)

process_loop_old = """    for (auto& cp : ccParams)
    {
        if (cp.param != nullptr)"""
process_loop_new = """    for (auto& cp : ccParams)
    {
        if (cp.param != nullptr && cp.ccNumber >= 0 && cp.ccNumber < 128)"""
content = content.replace(process_loop_old, process_loop_new)

content = content.replace('    startTimerHz(30);\n', '')
content = content.replace('syxParamMap[102] = "DLY_AMOUNT";\n}', 'syxParamMap[102] = "DLY_AMOUNT";\n    startTimerHz(30);\n}')

with open('Source/PluginProcessor.cpp', 'w') as f:
    f.write(content)

print("done patching.")
