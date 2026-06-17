import json
import sys

log_path = r'C:\Users\Notandi\.gemini\antigravity\brain\2998c07f-d36f-45f4-a7b7-e5f7bbc844a5\.system_generated\logs\transcript.jsonl'

latest_code = ""

with open(log_path, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            entry = json.loads(line)
            if entry.get('type') == 'TOOL_CALL':
                calls = entry.get('tool_calls', [])
                for call in calls:
                    if call.get('name') == 'write_to_file':
                        args = call.get('args', {})
                        if args.get('TargetFile') and 'generate.py' in args.get('TargetFile'):
                            latest_code = args.get('CodeContent', '')
                            # We can keep going or break.
        except Exception as e:
            pass

with open('scratch/extracted_generate.py', 'w', encoding='utf-8') as out:
    out.write(latest_code)
print("Extracted the latest generate.py from the transcript into scratch/extracted_generate.py!")
