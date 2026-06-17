import sys

with open('Source/PluginProcessor.cpp', 'r') as f:
    content = f.read()

old_log = """              if (!wroteLog) {
                  logFile.open("C:/TEMP/ANTIGRAVITIY_ROLANDS_SCRIPTS/SE02_Controller/vst_log.txt", std::ios_base::app);
                  logFile << "--- NEW SYSEX READ ---" << std::endl;
                  wroteLog = true;
              }
              logFile << "Index " << i << " (" << syxParamMap[i] << ") rawSysEx=" << hwVal << std::endl;"""

new_log = """              if (!wroteLog) {
                  logFile.open("C:/TEMP/ANTIGRAVITIY_ROLANDS_SCRIPTS/SE02_Controller/vst_log.txt", std::ios_base::app);
                  logFile << "--- NEW SYSEX READ ---" << std::endl;
                  // DUMP ALL RAW VALUES 20-40 to solve the mystery
                  for (int k = 20; k <= 40; ++k) {
                      logFile << "RAW_DUMP Index " << k << " = " << incomingSysExValues[k].load() << std::endl;
                  }
                  wroteLog = true;
              }
              logFile << "Index " << i << " (" << syxParamMap[i] << ") rawSysEx=" << hwVal << std::endl;"""

if old_log in content:
    content = content.replace(old_log, new_log)
    with open('Source/PluginProcessor.cpp', 'w') as f:
        f.write(content)
        print("Injected RAW_DUMP logic")
else:
    print("Could not inject RAW_DUMP logic")
