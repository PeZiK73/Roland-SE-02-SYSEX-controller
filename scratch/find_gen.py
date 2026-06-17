import json
import os

log_path = r'C:\Users\Notandi\.gemini\antigravity\brain\2998c07f-d36f-45f4-a7b7-e5f7bbc844a5\.system_generated\logs\transcript.jsonl'

generate_outputs = []

with open(log_path, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            entry = json.loads(line)
            if 'tool_calls' in entry:
                for call in entry['tool_calls']:
                    if call['name'] == 'run_command':
                        args = call.get('args', {})
                        if 'generate.py' in args.get('CommandLine', ''):
                            generate_outputs.append((entry['step_index'], args['CommandLine']))
        except Exception as e:
            pass

print("Executions found:")
for step, cmd in generate_outputs:
    print(f"Step {step}")
