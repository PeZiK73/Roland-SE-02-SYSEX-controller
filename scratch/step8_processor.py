import re

with open('Source/PluginProcessor.cpp', 'r') as f:
    content = f.read()

# 1. Update sysexToCc vals
content = content.replace("float vals[6] = {10.0f, 32.0f, 53.0f, 74.0f, 95.0f, 116.0f};", "float vals[6] = {0.0f, 25.4f, 50.8f, 76.2f, 101.6f, 127.0f};")

# 2. Decouple CC in processBlock
process_block_old = '''            if (std::abs(currentVal - cp.lastValue) > 0.1f)
            {
                int ccValue = juce::jlimit(0, 127, juce::roundToInt(currentVal));
                auto message = juce::MidiMessage::controllerEvent(1, cp.ccNumber, ccValue);'''

process_block_new = '''            if (std::abs(currentVal - cp.lastValue) > 0.1f)
            {
                int ccValue = juce::jlimit(0, 127, juce::roundToInt(currentVal));
                
                // DECOUPLE OSC RANGE CCs
                if (cp.ccNumber == 22 || cp.ccNumber == 26 || cp.ccNumber == 30) // OSC1, 2, 3 Range
                {
                    int idx = juce::roundToInt((currentVal / 127.0f) * 5.0f);
                    idx = juce::jlimit(0, 5, idx);
                    int hwCCs[6] = {8, 24, 40, 56, 72, 88};
                    ccValue = hwCCs[idx];
                }
                
                auto message = juce::MidiMessage::controllerEvent(1, cp.ccNumber, ccValue);'''

content = content.replace(process_block_old, process_block_new)

with open('Source/PluginProcessor.cpp', 'w') as f:
    f.write(content)
