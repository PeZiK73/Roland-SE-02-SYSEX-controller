with open('Source/PluginEditor.cpp', 'r') as f:
    lines = f.readlines()

with open('Source/PluginEditor.cpp', 'w') as f:
    for line in lines:
        if 'valLabel' not in line:
            f.write(line)
