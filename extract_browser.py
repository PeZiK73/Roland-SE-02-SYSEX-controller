import json

log_path = 'C:/Users/Notandi/.gemini/antigravity/brain/2998c07f-d36f-45f4-a7b7-e5f7bbc844a5/.system_generated/logs/transcript_full.jsonl'

h_code = ""
cpp_code = ""

with open(log_path, 'r', encoding='utf-8') as f:
    for line in f:
        if 'write_to_file' in line and 'PresetBrowser.h' in line:
            data = json.loads(line)
            for call in data.get('tool_calls', []):
                if call['name'] == 'write_to_file' and 'PresetBrowser.h' in call['args']['TargetFile']:
                    h_code = call['args']['CodeContent']
                    
        if 'write_to_file' in line and 'PresetBrowser.cpp' in line:
            data = json.loads(line)
            for call in data.get('tool_calls', []):
                if call['name'] == 'write_to_file' and 'PresetBrowser.cpp' in call['args']['TargetFile']:
                    cpp_code = call['args']['CodeContent']

if h_code:
    with open('Source/PresetBrowser.h', 'w', encoding='utf-8') as f:
        f.write(h_code)
    print("Extracted PresetBrowser.h")
else:
    print("Could not find PresetBrowser.h in transcript!")

if cpp_code:
    with open('Source/PresetBrowser.cpp', 'w', encoding='utf-8') as f:
        f.write(cpp_code)
    print("Extracted PresetBrowser.cpp")
else:
    print("Could not find PresetBrowser.cpp in transcript!")
