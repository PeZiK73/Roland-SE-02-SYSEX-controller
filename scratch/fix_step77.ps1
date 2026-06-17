import re

with open('scratch/step77.py', 'r') as f:
    content = f.read()

# Fix the regex that extracts cc_init_code
bad_regex = r"prep_match = re.search\(r'void SE02_ControllerAudioProcessor::prepareToPlay\[\^\\\{\]\+\\\{\\s\*\(ccParams\\.clear\(\);.*?\\s\*\\\}', content, re.DOTALL\)"
good_regex = r"prep_match = re.search(r'(ccParams\\.clear\\(\\);.*?for \\(auto& cp : ccParams\\)[^}]+}[^}]+})', content, re.DOTALL)"

# Just completely overwrite step77.py with a robust script
new_script = """import re

with open('Source/PluginProcessor.cpp', 'r') as f:
    content = f.read()

# 1. Erase all logger code
content = re.sub(r'juce::Logger::writeToLog\\("SysEx_DUMP Byte " \\+ juce::String\\(payloadOffset \\+ i\\) \\+ " = " \\+ juce::String\\(b\\)\\);', '', content)

log_code_regex = r'bool wroteLog = false;.*?if \\(wroteLog\\) logFile\\.close\\(\\);'

clean_sysex_code = '''    // Process SysEx
    for (int i = 0; i < 120; ++i)
    {
        float hwVal = incomingSysExValues[i].exchange(-1.0f);
        if (hwVal >= 0.0f && syxParamMap[i].isNotEmpty())
        {
            if (auto* param = apvts.getParameter(syxParamMap[i]))
            {
                float mappedVal = sysexToCc(syxParamMap[i], hwVal);
                param->setValueNotifyingHost(param->convertTo0to1(mappedVal));
                
                for (auto& cp : ccParams) {
                    if (cp.id == syxParamMap[i]) {
                        cp.lastValue = mappedVal;
                    }
                }
            }
        }
    }'''

content = re.sub(log_code_regex, clean_sysex_code, content, flags=re.DOTALL)

# 2. Extract ccParams initialization from prepareToPlay and move it to the Constructor
# Safely find the clear() to the end of the for loop
prep_match = re.search(r'(ccParams\\.clear\\(\\);.*?for \\(auto& cp : ccParams\\)[^{]+\\{[^}]+\\})', content, re.DOTALL)
if prep_match:
    cc_init_code = prep_match.group(1)
    # Remove from prepareToPlay
    content = content.replace(cc_init_code, '')
    # Add to Constructor BEFORE startTimerHz
    content = content.replace('    startTimerHz(30);', cc_init_code + '\\n\\n    startTimerHz(30);')

with open('Source/PluginProcessor.cpp', 'w') as f:
    f.write(content)
"""

with open('scratch/step77_fixed.py', 'w') as f:
    f.write(new_script)

print("Created step77_fixed.py")
