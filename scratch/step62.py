import sys

with open('Source/PluginProcessor.cpp', 'r') as f:
    content = f.read()

old_code = """        if (hwVal >= 0.0f && syxParamMap[i].isNotEmpty())
        {
            if (!wroteLog) {"""

new_code = """        if (hwVal >= 0.0f)
        {
            if (!wroteLog) {"""

if old_code in content:
    content = content.replace(old_code, new_code)
    
old_code2 = """            logFile << "Index " << i << " (" << syxParamMap[i] << ") rawSysEx=" << hwVal << std::endl;
            
            if (auto* param = apvts.getParameter(syxParamMap[i]))"""

new_code2 = """            logFile << "Index " << i << " (" << syxParamMap[i] << ") rawSysEx=" << hwVal << std::endl;
            
            if (syxParamMap[i].isNotEmpty()) {
                if (auto* param = apvts.getParameter(syxParamMap[i]))"""

if old_code2 in content:
    content = content.replace(old_code2, new_code2)

# Fix brace matching
old_code3 = """                param->setValueNotifyingHost(param->convertTo0to1(mappedVal));
            }
        }
    }"""

new_code3 = """                param->setValueNotifyingHost(param->convertTo0to1(mappedVal));
                }
            }
        }
    }"""

if old_code3 in content:
    content = content.replace(old_code3, new_code3)

with open('Source/PluginProcessor.cpp', 'w') as f:
    f.write(content)
