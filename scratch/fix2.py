import re

with open('Source/PluginProcessor.cpp', 'r') as f:
    content = f.read()

# Replace the broken lines
def replacer(match):
    name = match.group(1)
    val = "64.0f" if name in ["OSC2_FINE", "OSC3_FINE"] else "0.0f"
    return f'addCcParam("{name}", "{match.group(2)}", 0.0f, 127.0f, {val});'

content = re.sub(r'addCcParam\("([^"]+)", "([^"]+)", 0\.0f, 127\.0f, 64\.0f if "[^"]+" == "OSC2_FINE" or "[^"]+" == "OSC3_FINE" else 0\.0f\);', replacer, content)

with open('Source/PluginProcessor.cpp', 'w') as f:
    f.write(content)

print("Fixed C++ syntax!")
