import json

log_path = 'C:/Users/Notandi/.gemini/antigravity/brain/2998c07f-d36f-45f4-a7b7-e5f7bbc844a5/.system_generated/logs/transcript.jsonl'

events = []
with open(log_path, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            data = json.loads(line)
        except:
            continue
        
        if data.get('created_at', '') > '2026-06-11T18:55:00Z':
            break
            
        if data.get('type') == 'PLANNER_RESPONSE':
            tool_calls = data.get('tool_calls', [])
            for call in tool_calls:
                if call['name'] == 'run_command':
                    cmd = call['args'].get('CommandLine', '')
                    if 'python' in cmd or 'cmake' in cmd:
                        events.append(cmd.replace('\n', ' ')[:100])

for e in events[-20:]:
    print(e)
