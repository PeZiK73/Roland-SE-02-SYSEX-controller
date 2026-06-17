import re

with open('Source/PluginProcessor.cpp', 'r') as f:
    content = f.read()

# Fix timerCallback
timer_loop_old = """    for (auto& cp : ccParams)
    {
        float hwVal = incomingCcValues[cp.ccNumber].exchange(-1.0f);
        if (hwVal >= 0.0f)
        {
            if (auto* param = apvts.getParameter(cp.id))
            {
                param->setValueNotifyingHost(param->convertTo0to1(hwVal));
            }
        }
    }"""

timer_loop_new = """    for (auto& cp : ccParams)
    {
        if (cp.ccNumber >= 0 && cp.ccNumber < 128) {
            float hwVal = incomingCcValues[cp.ccNumber].exchange(-1.0f);
            if (hwVal >= 0.0f)
            {
                if (auto* param = apvts.getParameter(cp.id))
                {
                    param->setValueNotifyingHost(param->convertTo0to1(hwVal));
                }
            }
        }
    }"""

content = content.replace(timer_loop_old, timer_loop_new)

# Fix processBlock
process_loop_old = """    for (auto& cp : ccParams)
    {
        if (cp.param != nullptr)
        {
            float currentVal = *cp.param;
            if (std::abs(currentVal - cp.lastValue) > 0.1f)
            {
                int ccValue = juce::jlimit(0, 127, juce::roundToInt(currentVal));
                auto message = juce::MidiMessage::controllerEvent(1, cp.ccNumber, ccValue);
                midiOutputQueue.addEvent(message, 0);
                cp.lastValue = currentVal;
            }
        }
    }"""

process_loop_new = """    for (auto& cp : ccParams)
    {
        if (cp.param != nullptr && cp.ccNumber >= 0 && cp.ccNumber < 128)
        {
            float currentVal = *cp.param;
            if (std::abs(currentVal - cp.lastValue) > 0.1f)
            {
                int ccValue = juce::jlimit(0, 127, juce::roundToInt(currentVal));
                auto message = juce::MidiMessage::controllerEvent(1, cp.ccNumber, ccValue);
                midiOutputQueue.addEvent(message, 0);
                cp.lastValue = currentVal;
            }
        }
    }"""

content = content.replace(process_loop_old, process_loop_new)

with open('Source/PluginProcessor.cpp', 'w') as f:
    f.write(content)

print("Fixed out-of-bounds access for CC -1 (OSC3_FINE)!")
