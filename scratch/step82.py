import re

# Fix PluginEditor
with open('Source/PluginEditor.cpp', 'r') as f:
    ed_content = f.read()

ed_content = ed_content.replace('logdbg("EDITOR CONSTRUCTOR START");\nSE02_ControllerAudioProcessorEditor::SE02_ControllerAudioProcessorEditor', 'SE02_ControllerAudioProcessorEditor::SE02_ControllerAudioProcessorEditor')

ed_content = ed_content.replace('    setSize (1024, 330);', '    logdbg("EDITOR CONSTRUCTOR START");\n    setSize (1024, 330);')

with open('Source/PluginEditor.cpp', 'w') as f:
    f.write(ed_content)
