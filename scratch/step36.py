import sys

with open('Source/PluginProcessor.cpp', 'r') as f:
    content = f.read()

old_loop = """    for (auto& cp : ccParams)
    {
        float hwVal = incomingCcValues[cp.ccNumber].exchange(-1.0f);"""

new_loop = """    for (auto& cp : ccParams)
    {
        if (cp.ccNumber < 0 || cp.ccNumber >= 128) continue;
        float hwVal = incomingCcValues[cp.ccNumber].exchange(-1.0f);"""

if new_loop not in content:
    content = content.replace(old_loop, new_loop)
    with open('Source/PluginProcessor.cpp', 'w') as f:
        f.write(content)
        print("Fixed out-of-bounds CC array access")
else:
    print("Already fixed")
