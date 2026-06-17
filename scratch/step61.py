import sys

with open('Source/PluginProcessor.cpp', 'r') as f:
    content = f.read()

old_code = """                float mappedVal = sysexToCc(syxParamMap[i], hwVal);
                logFile << "  -> mapped to CC value: " << mappedVal << std::endl;
                param->setValueNotifyingHost(param->convertTo0to1(mappedVal));
                
                for (auto& cp : ccParams) {
                    if (cp.id == syxParamMap[i]) {
                        cp.lastValue = mappedVal;
                    }
                }"""

new_code = """                float mappedVal = sysexToCc(syxParamMap[i], hwVal);
                logFile << "  -> mapped to CC value: " << mappedVal << std::endl;
                
                for (auto& cp : ccParams) {
                    if (cp.id == syxParamMap[i]) {
                        cp.lastValue = mappedVal;
                    }
                }
                
                param->setValueNotifyingHost(param->convertTo0to1(mappedVal));"""

if old_code in content:
    content = content.replace(old_code, new_code)
    print("Fixed race condition")
else:
    print("Could not find old_code")

with open('Source/PluginProcessor.cpp', 'w') as f:
    f.write(content)
