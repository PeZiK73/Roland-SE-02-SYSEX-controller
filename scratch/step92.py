import re

with open('scratch/generate_clean.py', 'r') as f:
    text = f.read()

text = text.replace('int x = cx - width / 2;', 'int x = cx - 15;')
text = text.replace('int y = cy - height / 2;', 'int y = cy - 20;')
text = text.replace('comp->slider.setBounds(x, y, width, height + 16);', 'comp->slider.setBounds(x, y, 30, 40 + 16);')

with open('scratch/generate_clean.py', 'w') as f:
    f.write(text)

print("generate_clean.py fixed.")
