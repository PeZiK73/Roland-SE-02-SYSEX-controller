import json
import os

log_path = r'C:\Users\Notandi\.gemini\antigravity\brain\2998c07f-d36f-45f4-a7b7-e5f7bbc844a5\.system_generated\logs\transcript.jsonl'

latest_generate_code = ""

with open(log_path, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            entry = json.loads(line)
            if entry.get('type') == 'PLANNER_RESPONSE':
                # Just checking
                pass
            if 'tool_calls' in entry:
                for call in entry['tool_calls']:
                    if call['name'] == 'write_to_file':
                        args = call.get('args', {})
                        if args.get('TargetFile') and 'generate.py' in args.get('TargetFile'):
                            latest_generate_code = args.get('CodeContent', '')
        except Exception as e:
            pass

print(f"Length of extracted code: {len(latest_generate_code)}")

if len(latest_generate_code) > 0:
    with open('scratch/extracted_generate.py', 'w', encoding='utf-8') as out:
        out.write(latest_generate_code)
