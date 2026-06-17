import sys
import re
with open('Source/PluginProcessor.cpp', 'r') as f:
    content = f.read()

content = re.sub(r'\s*else if \(baseAddress == 0x40 && fetchState == FetchState::WaitSysEx_40\).*?fetchTimeoutCounter = 5; fetchRetryCounter = 0;\n                  \}', '', content, flags=re.DOTALL)

with open('Source/PluginProcessor.cpp', 'w') as f:
    f.write(content)
