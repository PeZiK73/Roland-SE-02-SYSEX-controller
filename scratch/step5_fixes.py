import re

with open('Source/PluginEditor.cpp', 'r') as f:
    content = f.read()

# 1. Update setSize
content = content.replace("setSize (1024, 330);", "setSize (2048, 660);")

# 2. Update MIDI ComboBox memory
midi_logic_old = '''    auto inDevices = juce::MidiInput::getAvailableDevices();
    for (auto& dev : inDevices) midiInBox.addItem(dev.name, midiInBox.getNumItems() + 1);
    
    auto outDevices = juce::MidiOutput::getAvailableDevices();
    for (auto& dev : outDevices) midiOutBox.addItem(dev.name, midiOutBox.getNumItems() + 1);'''

midi_logic_new = '''    auto inDevices = juce::MidiInput::getAvailableDevices();
    int i = 1;
    for (auto& dev : inDevices) {
        midiInBox.addItem(dev.name, i);
        if (dev.name == audioProcessor.lastMidiInName) midiInBox.setSelectedId(i, juce::dontSendNotification);
        i++;
    }
    
    auto outDevices = juce::MidiOutput::getAvailableDevices();
    i = 1;
    for (auto& dev : outDevices) {
        midiOutBox.addItem(dev.name, i);
        if (dev.name == audioProcessor.lastMidiOutName) midiOutBox.setSelectedId(i, juce::dontSendNotification);
        i++;
    }'''

content = content.replace(midi_logic_old, midi_logic_new)

# 3. Update loadPresetFromFile math
load_math_old = '''            if (maxDiscrete == 5) {
                normalized = (float)rawVal / 5.0f;
            } else if (maxDiscrete == 2) {
                normalized = (float)rawVal / 2.0f;
            } else if (maxDiscrete == 1) {
                normalized = rawVal > 0 ? 1.0f : 0.0f;
            } else {
                normalized = (float)rawVal / 255.0f;
            }'''

load_math_new = '''            if (maxDiscrete == 5) {
                float vals[6] = {0.0f, 26.0f, 51.0f, 77.0f, 102.0f, 127.0f};
                normalized = vals[juce::jlimit(0, 5, rawVal)] / 127.0f;
            } else if (maxDiscrete == 2) {
                float vals[3] = {0.0f, 64.0f, 127.0f};
                normalized = vals[juce::jlimit(0, 2, rawVal)] / 127.0f;
            } else if (maxDiscrete == 1) {
                normalized = rawVal > 0 ? 1.0f : 0.0f;
            } else {
                normalized = (float)rawVal / 255.0f;
            }'''
            
content = content.replace(load_math_old, load_math_new)

# 4. Update savePresetToFile math
save_math_old = '''        if (maxDiscrete == 5) val = juce::roundToInt(normalizedVal * 5.0f);
        else if (maxDiscrete == 2) val = juce::roundToInt(normalizedVal * 2.0f);
        else if (maxDiscrete == 1) val = normalizedVal > 0.5f ? 1 : 0;
        else val = juce::roundToInt(normalizedVal * 255.0f);'''

save_math_new = '''        if (maxDiscrete == 5) {
            float vals[6] = {0.0f, 26.0f, 51.0f, 77.0f, 102.0f, 127.0f};
            float ccVal = normalizedVal * 127.0f;
            float minDist = 999.0f;
            int bestIdx = 0;
            for (int i=0; i<6; ++i) {
                if (std::abs(ccVal - vals[i]) < minDist) {
                    minDist = std::abs(ccVal - vals[i]);
                    bestIdx = i;
                }
            }
            val = bestIdx;
        } else if (maxDiscrete == 2) {
            float vals[3] = {0.0f, 64.0f, 127.0f};
            float ccVal = normalizedVal * 127.0f;
            float minDist = 999.0f;
            int bestIdx = 0;
            for (int i=0; i<3; ++i) {
                if (std::abs(ccVal - vals[i]) < minDist) {
                    minDist = std::abs(ccVal - vals[i]);
                    bestIdx = i;
                }
            }
            val = bestIdx;
        } else if (maxDiscrete == 1) {
            val = normalizedVal > 0.5f ? 1 : 0;
        } else {
            val = juce::roundToInt(normalizedVal * 255.0f);
        }'''
        
content = content.replace(save_math_old, save_math_new)

with open('Source/PluginEditor.cpp', 'w') as f:
    f.write(content)
