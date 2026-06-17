import re

with open('Source/PluginProcessor.cpp', 'r') as f:
    content = f.read()

# 1. Remove startTimerHz from the middle of the constructor
content = content.replace('    startTimerHz(30);\n', '')

# 2. Add startTimerHz to the end of the constructor
constructor_end_regex = r'(syxParamMap\[102\] = "DLY_AMOUNT";\s*\})'
replacement = r'syxParamMap[102] = "DLY_AMOUNT";\n    startTimerHz(30);\n}'
content = re.sub(constructor_end_regex, replacement, content)

with open('Source/PluginProcessor.cpp', 'w') as f:
    f.write(content)

print("Moved startTimerHz(30) to the absolute end of the constructor!")
