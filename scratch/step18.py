import sys
with open('Source/PluginProcessor.cpp', 'r') as f:
    lines = f.readlines()

new_lines = []
for i, line in enumerate(lines):
    if 210 <= i <= 215:
        # 210 is line 211
        continue
    new_lines.append(line)

new_lines.insert(210, "                }\n            }\n        }\n")

with open('Source/PluginProcessor.cpp', 'w') as f:
    f.writelines(new_lines)
