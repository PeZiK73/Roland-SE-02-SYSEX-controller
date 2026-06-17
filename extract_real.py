import json
with open('C:/Users/Notandi/.gemini/antigravity/brain/2998c07f-d36f-45f4-a7b7-e5f7bbc844a5/.system_generated/logs/transcript_full.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        if 'PresetBrowser.h' in line and '#pragma once' in line and 'PLANNER_RESPONSE' in line:
            try:
                obj = json.loads(line.strip())
                for tool in obj.get('tool_calls', []):
                    cmd = tool.get('args', {}).get('CommandLine', '')
                    if '#pragma once' in cmd and 'class PresetBrowser' in cmd:
                        if 'extract' not in cmd and 'python' not in cmd and 'json.loads' not in cmd and 'Select-String' not in cmd:
                            with open('dump_real_h.txt', 'w', encoding='utf-8') as out:
                                out.write(cmd)
                            print('Dumped TRUE PresetBrowser.h script!')
                            break
            except:
                pass
