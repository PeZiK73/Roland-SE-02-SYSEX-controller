import re

with open('CMakeLists.txt', 'r') as f:
    content = f.read()

if 'Source/PresetBrowser.cpp' not in content:
    content = content.replace('Source/PluginEditor.h', 'Source/PluginEditor.h\n    Source/PresetBrowser.cpp\n    Source/PresetBrowser.h')
    with open('CMakeLists.txt', 'w') as f:
        f.write(content)
