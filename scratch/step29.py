import sys

with open('Source/PresetBrowser.cpp', 'r') as f:
    content = f.read()

content = content.replace("PresetBrowser::~PresetBrowser()\n{\n}", "PresetBrowser::~PresetBrowser()\n{\n    stopTimer();\n}")

with open('Source/PresetBrowser.cpp', 'w') as f:
    f.write(content)
