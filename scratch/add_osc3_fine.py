import re

with open('scratch/generate_safe.py', 'r') as f:
    content = f.read()

# Add OSC3_FINE to the params array
if '"OSC3_FINE"' not in content:
    content = content.replace('("OSC3_RANGE", "RANGE", 25, "knob"),', '("OSC3_RANGE", "RANGE", 25, "knob"),\n    ("OSC3_FINE", "FINE", 28, "knob"),')

with open('scratch/generate_safe.py', 'w') as f:
    f.write(content)
