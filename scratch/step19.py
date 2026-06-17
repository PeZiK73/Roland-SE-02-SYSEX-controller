import re
with open('Source/PluginProcessor.cpp', 'r') as f:
    content = f.read()

bad_code = '''        int msb = 85; 
        int lsb = fetchBankIndex; 
        if (fetchBankIndex == 4) lsb = 0; 
        int pc = fetchPatchIndex;'''

good_code = '''        int msb = fetchBankIndex; 
        int lsb = 0; 
        int pc = fetchPatchIndex;'''

content = content.replace(bad_code, good_code)

with open('Source/PluginProcessor.cpp', 'w') as f:
    f.write(content)
