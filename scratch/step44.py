import sys
import re

with open('Source/PluginProcessor.cpp', 'r') as f:
    content = f.read()

# I will find the EXACT string block using regex
pattern = re.compile(r'(logFile << "Index " << i << " \(" << syxParamMap\[i\] << "\) rawSysEx=" << hwVal << std::endl;)', re.MULTILINE)

replacement = r'''if (!wroteLog) {
                  logFile.open("C:/TEMP/ANTIGRAVITIY_ROLANDS_SCRIPTS/SE02_Controller/vst_log_raw.txt", std::ios_base::app);
                  logFile << "--- NEW SYSEX READ ---" << std::endl;
                  for (int k = 20; k <= 40; ++k) {
                      logFile << "RAW_DUMP Index " << k << " = " << incomingSysExValues[k].load() << std::endl;
                  }
                  logFile.close();
                  wroteLog = true;
              }
              \1'''

content = pattern.sub(replacement, content)

with open('Source/PluginProcessor.cpp', 'w') as f:
    f.write(content)
    print("Injected RAW_DUMP logic")
