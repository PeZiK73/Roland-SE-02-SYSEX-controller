import re
with open('Source/PluginProcessor.h', 'r') as f:
    content = f.read()

content = content.replace("int ccBlockTimer = 0;", "std::atomic<int> ccBlockTimer {0};")

with open('Source/PluginProcessor.h', 'w') as f:
    f.write(content)
