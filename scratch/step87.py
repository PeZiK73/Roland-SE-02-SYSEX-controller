import re

with open('Source/PluginEditor.cpp', 'r') as f:
    ed_content = f.read()

# Fix multi-line comment error
ed_content = ed_content.replace('/* auto inDevices', '// auto inDevices')
ed_content = ed_content.replace('*/\n    /* midiInBox', '// midiInBox')
ed_content = ed_content.replace('*/\n    readPresetBtn', '    readPresetBtn')
ed_content = ed_content.replace('/* ', '// ')
ed_content = ed_content.replace('*/ ', '// ')

with open('Source/PluginEditor.cpp', 'w') as f:
    f.write(ed_content)

with open('Source/PluginProcessor.cpp', 'r') as f:
    p_content = f.read()

p_content = p_content.replace('    logdbg("CALLING createEditor");\n', '')

with open('Source/PluginProcessor.cpp', 'w') as f:
    f.write(p_content)

print("Fixed syntax")
