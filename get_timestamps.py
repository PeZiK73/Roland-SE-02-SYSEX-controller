import json

log_path = 'C:/Users/Notandi/.gemini/antigravity/brain/2998c07f-d36f-45f4-a7b7-e5f7bbc844a5/.system_generated/logs/transcript.jsonl'

with open(log_path, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            data = json.loads(line)
        except:
            continue
            
        time = data.get('created_at', '')
        if time > '2026-06-11T18:49:00Z' and time < '2026-06-11T18:52:00Z':
            if data.get('type') == 'PLANNER_RESPONSE':
                tool_calls = data.get('tool_calls', [])
                for call in tool_calls:
                    if call['name'] == 'run_command':
                        print(time, call['args'].get('CommandLine', '')[:100])
