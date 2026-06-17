import json
import re

log_path = 'C:/Users/Notandi/.gemini/antigravity/brain/2998c07f-d36f-45f4-a7b7-e5f7bbc844a5/.system_generated/logs/transcript.jsonl'

events = []

with open(log_path, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            data = json.loads(line)
        except:
            continue
            
        step_index = data.get('step_index', 0)
        source = data.get('source', '')
        msg_type = data.get('type', '')
        content = data.get('content', '')
        
        if msg_type == 'USER_INPUT':
            events.append(f"Step {step_index} [USER]: {content.strip()}")
            
        elif msg_type == 'PLANNER_RESPONSE':
            tool_calls = data.get('tool_calls', [])
            for call in tool_calls:
                if call['name'] == 'run_command':
                    cmd = call['args'].get('CommandLine', '')
                    if 'cmake --build' in cmd or 'Copy-Item' in cmd:
                        # Extract the interesting part of the command
                        cmd_short = cmd.replace('\n', ' ')[:100]
                        events.append(f"Step {step_index} [AGENT CMD]: {cmd_short}")
        elif msg_type == 'TOOL_RESPONSE':
             # Maybe check if copy was successful, but probably not strictly necessary
             pass
             
print("Recent Events:")
# Print the last 50 events to capture the rollback loops
for e in events[-50:]:
    print(e)
