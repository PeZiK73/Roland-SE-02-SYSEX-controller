import re

with open("C:/TEMP/ANTIGRAVITIY_ROLANDS_SCRIPTS/SE02_Controller/scratch/generate.py", "r") as f:
    code = f.read()

# 1. Add #include <fstream>
if "#include <fstream>" not in code:
    code = code.replace('#include "PluginProcessor.h"', '#include "PluginProcessor.h"\n#include <fstream>')

# 2. Add ccBlockTimer update
sysex_parse_replacement = """
                for (int i = 0; i < byteCount; ++i)
                {
                    if (payloadOffset + i < 120)
                    {
                        juce::uint8 b = ((nibbles[i*2] & 0x0F) << 4) | (nibbles[i*2+1] & 0x0F);
                        incomingSysExValues[payloadOffset + i].store((float)b);
                    }
                }
                ccBlockTimer.store(20);
"""
code = re.sub(r'                for \(int i = 0; i < byteCount; \+\+i\)\n\s*\{\n\s*if \(payloadOffset \+ i < 120\)\n\s*\{\n\s*juce::uint8 b = \(\(nibbles\[i\*2\] & 0x0F\) << 4\) \| \(nibbles\[i\*2\+1\] & 0x0F\);\n\s*incomingSysExValues\[payloadOffset \+ i\]\.store\(\(float\)b\);\n\s*\}\n\s*\}', sysex_parse_replacement, code)

# 3. Add timerCallback logging and logic
timer_repl = """
    if (ccBlockTimer.load() > 0) ccBlockTimer.fetch_sub(1);

    bool wroteLog = false;
    std::ofstream logFile;
    
    // Process SysEx
    for (int i = 0; i < 120; ++i)
    {
        float hwVal = incomingSysExValues[i].exchange(-1.0f);
        if (hwVal >= 0.0f && syxParamMap[i].isNotEmpty())
        {
            if (!wroteLog) {
                logFile.open("C:/TEMP/ANTIGRAVITIY_ROLANDS_SCRIPTS/SE02_Controller/vst_log.txt", std::ios_base::app);
                logFile << "--- NEW SYSEX READ ---" << std::endl;
                wroteLog = true;
            }
            logFile << "Index " << i << " (" << syxParamMap[i] << ") rawSysEx=" << hwVal << std::endl;
            
            if (auto* param = apvts.getParameter(syxParamMap[i]))
            {
                float mappedVal = sysexToCc(syxParamMap[i], hwVal);
                logFile << "  -> mapped to CC value: " << mappedVal << std::endl;
                param->setValueNotifyingHost(param->convertTo0to1(mappedVal));
                
                for (auto& cp : ccParams) {
                    if (cp.id == syxParamMap[i]) {
                        cp.lastValue = mappedVal;
                    }
                }
            }
        }
    }
    if (wroteLog) logFile.close();
"""
code = re.sub(r'    // Process SysEx\n\s*for \(int i = 0; i < 120; \+\+i\)\n\s*\{\n.*?\}\n\s*\}', timer_repl, code, flags=re.DOTALL)

# 4. Add processBlock CC blocker
process_block_repl = """
    if (ccBlockTimer.load() > 0)
    {
        for (auto& cp : ccParams)
        {
            if (cp.param != nullptr) cp.lastValue = *cp.param;
        }
    }
    else
    {
        for (auto& cp : ccParams)
        {
            if (cp.param != nullptr)
            {
                float currentVal = *cp.param;
                if (std::abs(currentVal - cp.lastValue) > 0.1f)
                {
                    int ccValue = juce::jlimit(0, 127, juce::roundToInt(currentVal));
                    auto message = juce::MidiMessage::controllerEvent(1, cp.ccNumber, ccValue);
                    if (hardwareMidiOut) hardwareMidiOut->sendMessageNow(message);
                    else midiOutputQueue.addEvent(message, 0);
                    cp.lastValue = currentVal;
                    
                    std::ofstream logFile("C:/TEMP/ANTIGRAVITIY_ROLANDS_SCRIPTS/SE02_Controller/vst_log.txt", std::ios_base::app);
                    logFile << "Sent CC: " << cp.ccNumber << " val: " << ccValue << std::endl;
                }
            }
        }
    }
"""
code = re.sub(r'    for \(auto& cp : ccParams\)\n\s*\{\n\s*if \(cp\.param != nullptr\)\n\s*\{\n\s*float currentVal = \*cp\.param;\n\s*if \(std::abs\(currentVal - cp\.lastValue\) > 0\.1f\)\n\s*\{\n\s*int ccValue = juce::jlimit\(0, 127, juce::roundToInt\(currentVal\)\);\n\s*auto message = juce::MidiMessage::controllerEvent\(1, cp\.ccNumber, ccValue\);\n\s*if \(hardwareMidiOut\) hardwareMidiOut->sendMessageNow\(message\);\n\s*else midiOutputQueue\.addEvent\(message, 0\);\n\s*cp\.lastValue = currentVal;\n\s*\}\n\s*\}\n\s*\}', process_block_repl, code)

with open("C:/TEMP/ANTIGRAVITIY_ROLANDS_SCRIPTS/SE02_Controller/scratch/generate.py", "w") as f:
    f.write(code)

print("generate.py patched successfully.")
