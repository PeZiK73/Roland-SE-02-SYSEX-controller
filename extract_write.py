import json
with open('C:/Users/Notandi/.gemini/antigravity/brain/2998c07f-d36f-45f4-a7b7-e5f7bbc844a5/.system_generated/logs/transcript_full.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        if 'PresetBrowser.h' in line and 'write_to_file' in line and 'PLANNER_RESPONSE' in line:
            try:
                obj = json.loads(line.strip())
                for tool in obj.get('tool_calls', []):
                    if tool.get('name') == 'write_to_file':
                        target = tool.get('args', {}).get('TargetFile', '')
                        if 'PresetBrowser.h' in target:
                            code = tool.get('args', {}).get('CodeContent', '')
                            with open('Source/PresetBrowser.h', 'w', encoding='utf-8') as out:
                                out.write(code)
                            print('Recovered PresetBrowser.h from write_to_file!')
                            break
            except:
                pass
