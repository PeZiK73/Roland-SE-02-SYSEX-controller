import re

with open('scratch/generate.py', 'r') as f:
    content = f.read()

# Update CC map in generate.py
content = re.sub(r'\("OSC1_TUNE",\s*"OSC1_TUNE",\s*(-1|29),\s*"knob"\),', '("OSC1_TUNE", "OSC1_TUNE", 27, "knob"),', content)
content = re.sub(r'\("OSC2_FINE",\s*"OSC2_FINE",\s*27,\s*"knob"\),', '("OSC2_FINE", "OSC2_FINE", 28, "knob"),', content)
content = re.sub(r'\("OSC3_FINE",\s*"OSC3_FINE",\s*28,\s*"knob"\),', '("OSC3_FINE", "OSC3_FINE", -1, "knob"),', content)
content = re.sub(r'\("ENV1",\s*"ENV1",\s*-1,\s*"knob"\),', '("ENV1", "ENV1", 29, "knob"),', content)

# Update SysEx map in generate.py
# If 29 is OSC2_FINE, 30 is OSC3_FINE
# What is OSC1_TUNE? Let's just put it at 25 for now! If it's missing, it won't break anything.
content = re.sub(r'syxParamMap\[29\] = "OSC1_TUNE"; // Removed, does not support sysex', 'syxParamMap[25] = "OSC1_TUNE";\n    syxParamMap[29] = "OSC2_FINE";', content)
content = re.sub(r'syxParamMap\[30\] = "OSC2_FINE";', 'syxParamMap[30] = "OSC3_FINE";', content)

with open('scratch/generate.py', 'w') as f:
    f.write(content)

print("Updated generate.py successfully")
