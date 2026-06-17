import re

with open('scratch/generate.py', 'r') as f:
    content = f.read()

# Comment out the PluginEditor.cpp write
content = re.sub(r'with open\("C:/TEMP/ANTIGRAVITIY_ROLANDS_SCRIPTS/SE02_Controller/Source/PluginEditor.cpp"', r'#with open(', content)
content = re.sub(r'    f\.write\(editor_code\)', r'#f.write(editor_code)', content)

with open('scratch/generate_safe.py', 'w') as f:
    f.write(content)
