import re

with open('Source/PluginProcessor.cpp', 'r') as f:
    proc = f.read()

# 1. Revert createParameterLayout
layout_match = re.search(r'(juce::AudioProcessorValueTreeState::ParameterLayout SE02_ControllerAudioProcessor::createParameterLayout\(\)\s*\{.*?auto addCcParam = .*?;\s*\n\s*)(.*?)(\s*return layout;\s*\})', proc, re.DOTALL)
if layout_match:
    old_params = '''addCcParam("GLIDE", "GLIDE", 0.0f, 127.0f, 0.0f);
    addCcParam("GLIDE_TYPE", "TYPE", 0.0f, 127.0f, 0.0f);
    addCcParam("WHL_MIX", "WHL MIX", 0.0f, 127.0f, 0.0f);'''
    proc = proc[:layout_match.start(2)] + old_params + proc[layout_match.end(2):]

# 2. Revert syxParamMap
syx_match = re.search(r'(syxParamMap\[22\] = "WHL_MIX";\s*)(.*?)(\s*// --- MOVED FROM prepareToPlay)', proc, re.DOTALL)
if syx_match:
    proc = proc[:syx_match.start(2)] + proc[syx_match.end(2):]

# 3. Revert ccParams
cc_match = re.search(r'(ccParams\.push_back\(\{"WHL_MIX", 13\}\);\s*)(.*?)(\s*for \(auto& cp : ccParams\))', proc, re.DOTALL)
if cc_match:
    proc = proc[:cc_match.start(2)] + proc[cc_match.end(2):]

with open('Source/PluginProcessor.cpp', 'w') as f:
    f.write(proc)


with open('Source/PluginEditor.cpp', 'r') as f:
    editor = f.read()

# 1. Revert addKnob calls in constructor
knobs_match = re.search(r'(addKnob\("WHL_MIX", "WHL MIX", 46, r3, kSize\);\s*)(.*?)(\s*// resizer.setBounds)', editor, re.DOTALL)
if knobs_match:
    editor = editor[:knobs_match.start(2)] + editor[knobs_match.end(2):]

with open('Source/PluginEditor.cpp', 'w') as f:
    f.write(editor)

print('Reverted safely!')
