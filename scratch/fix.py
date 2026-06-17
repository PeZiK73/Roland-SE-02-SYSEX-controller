import re

def fix_errors():
    with open('Source/PluginProcessor.h', 'r') as f:
        h = f.read()
    h = re.sub(r'    void handleIncomingMidiMessage.*?\n', '', h)
    with open('Source/PluginProcessor.h', 'w') as f:
        f.write(h)

    with open('Source/PluginProcessor.cpp', 'r') as f:
        cpp = f.read()
    cpp = re.sub(r'    for \(int i = 0; i < 120; \+\+i\) incomingSysExValues\[i\]\.store\(-1\.0f\);\n', '', cpp)
    with open('Source/PluginProcessor.cpp', 'w') as f:
        f.write(cpp)

    with open('Source/PluginEditor.cpp', 'r') as f:
        ed = f.read()
    # remove showValuesBtn.getToggleState() occurrences
    ed = re.sub(r'    comp->valLabel.setVisible\(showValuesBtn.getToggleState\(\)\);\n', '    comp->valLabel.setVisible(false);\n', ed)
    with open('Source/PluginEditor.cpp', 'w') as f:
        f.write(ed)

fix_errors()
print("Fixed!")
