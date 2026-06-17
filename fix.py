import re
with open('Source_backup/PluginEditor.cpp', 'r') as f:
    backup = f.read()

match = re.search(r'(SE02_ControllerAudioProcessorEditor::~SE02_ControllerAudioProcessorEditor.*)', backup, re.DOTALL)
if match:
    methods = match.group(1)
    
    with open('Source/PluginEditor.cpp', 'r') as f:
        current = f.read()
    
    current = current + '\n' + methods
    
    with open('Source/PluginEditor.cpp', 'w') as f:
        f.write(current)
    print('Methods restored')
else:
    print('Match not found')
