import re

with open('Source/PluginProcessor.cpp', 'r') as f:
    content = f.read()

# 1. Bounds Check
timer_loop_old = """    for (auto& cp : ccParams)\n    {\n        float hwVal = incomingCcValues[cp.ccNumber].exchange(-1.0f);\n        if (hwVal >= 0.0f)\n        {\n            if (auto* param = apvts.getParameter(cp.id))\n            {\n                param->setValueNotifyingHost(param->convertTo0to1(hwVal));\n            }\n        }\n    }"""
timer_loop_new = """    for (auto& cp : ccParams)\n    {\n        if (cp.ccNumber >= 0 && cp.ccNumber < 128) {\n            float hwVal = incomingCcValues[cp.ccNumber].exchange(-1.0f);\n            if (hwVal >= 0.0f)\n            {\n                if (auto* param = apvts.getParameter(cp.id))\n                {\n                    param->setValueNotifyingHost(param->convertTo0to1(hwVal));\n                }\n            }\n        }\n    }"""
content = content.replace(timer_loop_old, timer_loop_new)

process_loop_old = """    for (auto& cp : ccParams)\n    {\n        if (cp.param != nullptr)\n        {\n            float currentVal = *cp.param;\n            if (std::abs(currentVal - cp.lastValue) > 0.1f)\n            {\n                int ccValue = juce::jlimit(0, 127, juce::roundToInt(currentVal));\n                auto message = juce::MidiMessage::controllerEvent(1, cp.ccNumber, ccValue);\n                midiOutputQueue.addEvent(message, 0);\n                cp.lastValue = currentVal;\n            }\n        }\n    }"""
process_loop_new = """    for (auto& cp : ccParams)\n    {\n        if (cp.param != nullptr && cp.ccNumber >= 0 && cp.ccNumber < 128)\n        {\n            float currentVal = *cp.param;\n            if (std::abs(currentVal - cp.lastValue) > 0.1f)\n            {\n                int ccValue = juce::jlimit(0, 127, juce::roundToInt(currentVal));\n                auto message = juce::MidiMessage::controllerEvent(1, cp.ccNumber, ccValue);\n                midiOutputQueue.addEvent(message, 0);\n                cp.lastValue = currentVal;\n            }\n        }\n    }"""
content = content.replace(process_loop_old, process_loop_new)

# 2. Data Race Timer fix
content = content.replace('    startTimerHz(30);\n', '')
constructor_end_regex = r'(syxParamMap\[102\] = "DLY_AMOUNT";\s*\})'
replacement = r'syxParamMap[102] = "DLY_AMOUNT";\n    startTimerHz(30);\n}'
content = re.sub(constructor_end_regex, replacement, content)

with open('Source/PluginProcessor.cpp', 'w') as f:
    f.write(content)

# 3. Strip Hardware MIDI
with open('Source/PluginEditor.cpp', 'r') as f:
    ed_content = f.read()

ed_content = ed_content.replace('auto inDevices = juce::MidiInput::getAvailableDevices();\n    for (auto& dev : inDevices) midiInBox.addItem(dev.name, midiInBox.getNumItems() + 1);', '')
ed_content = ed_content.replace('auto outDevices = juce::MidiOutput::getAvailableDevices();\n    for (auto& dev : outDevices) midiOutBox.addItem(dev.name, midiOutBox.getNumItems() + 1);', '')
ed_content = ed_content.replace('midiInBox.setBounds(630, 302, 120, 24);\n    midiInBox.setTextWhenNothingSelected("MIDI Input...");\n    mainPanel->addAndMakeVisible(midiInBox);\n', '')
ed_content = ed_content.replace('midiOutBox.setBounds(760, 302, 120, 24);\n    midiOutBox.setTextWhenNothingSelected("MIDI Output...");\n    mainPanel->addAndMakeVisible(midiOutBox);\n', '')

inbox_lambda = r'midiInBox\.onChange = \[this\]\(\) \{.*?\n    \};\n'
ed_content = re.sub(inbox_lambda, '', ed_content, flags=re.DOTALL)
outbox_lambda = r'midiOutBox\.onChange = \[this\]\(\) \{.*?\n    \};\n'
ed_content = re.sub(outbox_lambda, '', ed_content, flags=re.DOTALL)

with open('Source/PluginEditor.cpp', 'w') as f:
    f.write(ed_content)

print("Applied 3 fixes.")
