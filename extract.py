import json
import re

with open('timestamp_match.json', 'r', encoding='utf-16le', errors='replace') as f:
    text = f.read()

matches = re.finditer(r'\"CommandLine\":\"(.*?)\"\}', text, re.DOTALL)
for i, match in enumerate(matches):
    cmd = match.group(1)
    try:
        cmd = json.loads('\"' + cmd + '\"')
        if 'PresetBrowser.h' in cmd and 'PresetBrowser.cpp' not in cmd:
            with open('Source/PresetBrowser.h', 'w', encoding='utf-8') as out:
                # the powershell script was: @"\n...code..."@ | Set-Content ...
                code = cmd.split('@\"')[1].split('\"@')[0].strip()
                out.write(code)
            print('Saved h!')
        elif 'PresetBrowser.cpp' in cmd:
            with open('Source/PresetBrowser.cpp', 'w', encoding='utf-8') as out:
                code = cmd.split('@\"')[1].split('\"@')[0].strip()
                out.write(code)
            print('Saved cpp!')
    except:
        pass
