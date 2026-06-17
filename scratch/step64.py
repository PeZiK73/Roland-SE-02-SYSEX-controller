import sys

with open('Source/PluginProcessor.cpp', 'r') as f:
    content = f.read()

old_code = """        if (msg.isSysEx())
        {
            auto data = msg.getRawData();
            int size = msg.getRawDataSize();
            
            // F0 41 10 00 00 00 44 12"""

new_code = """        if (msg.isSysEx())
        {
            auto data = msg.getRawData();
            int size = msg.getRawDataSize();
            
            static FILE* rawLog = fopen("C:/TEMP/ANTIGRAVITIY_ROLANDS_SCRIPTS/SE02_Controller/raw_sysex_log.txt", "a");
            if (rawLog) {
                fprintf(rawLog, "RAW SYSEX (size %d): ", size);
                for (int j = 0; j < size; ++j) {
                    fprintf(rawLog, "%02X ", data[j]);
                }
                fprintf(rawLog, "\\n");
                fflush(rawLog);
            }
            
            // F0 41 10 00 00 00 44 12"""

if old_code in content:
    content = content.replace(old_code, new_code)
    
with open('Source/PluginProcessor.cpp', 'w') as f:
    f.write(content)
