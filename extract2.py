import json
with open('C:/Users/Notandi/.gemini/antigravity/brain/2998c07f-d36f-45f4-a7b7-e5f7bbc844a5/.system_generated/logs/transcript_full.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        if 'PresetBrowser.h' in line and 'Set-Content' in line and 'PLANNER_RESPONSE' in line:
            try:
                obj = json.loads(line.strip())
                for tool in obj.get('tool_calls', []):
                    cmd = tool.get('args', {}).get('CommandLine', '')
                    if 'Set-Content' in cmd and 'PresetBrowser.h' in cmd and 'PresetBrowser.cpp' not in cmd:
                        code = cmd.split('@\"')[1].split('\"@')[0].strip()
                        with open('Source/PresetBrowser.h', 'w', encoding='utf-8') as out:
                            out.write(code)
                        print('Saved PresetBrowser.h!')
            except:
                pass
        
        if 'PresetBrowser.cpp' in line and 'Set-Content' in line and 'PLANNER_RESPONSE' in line:
            try:
                obj = json.loads(line.strip())
                for tool in obj.get('tool_calls', []):
                    cmd = tool.get('args', {}).get('CommandLine', '')
                    if 'Set-Content' in cmd and 'PresetBrowser.cpp' in cmd:
                        code = cmd.split('@\"')[1].split('\"@')[0].strip()
                        with open('Source/PresetBrowser.cpp', 'w', encoding='utf-8') as out:
                            out.write(code)
                        print('Saved PresetBrowser.cpp!')
            except:
                pass
