import json
import os

log_path = r'C:\Users\Notandi\.gemini\antigravity\brain\2998c07f-d36f-45f4-a7b7-e5f7bbc844a5\.system_generated\logs\transcript.jsonl'

latest_code = ""

with open(log_path, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            entry = json.loads(line)
            step = entry.get('step_index')
            if step > 1150:
                break
                
            if 'tool_calls' in entry:
                for call in entry['tool_calls']:
                    if call['name'] in ['write_to_file', 'multi_replace_file_content']:
                        args = call.get('args', {})
                        if args.get('TargetFile') and 'generate.py' in args.get('TargetFile'):
                            if call['name'] == 'write_to_file':
                                latest_code = args.get('CodeContent', '')
                            else:
                                pass # ignore replacements for now, or we can just cat the file?
                                # wait, the transcript only has the edits, not the full file.
                                # But we want to just recover the file from the filesystem if we can? No, we overwrote the file!
        except Exception as e:
            pass

print("Length found:", len(latest_code))
if len(latest_code) > 0:
    with open('scratch/extracted_generate_1150.py', 'w', encoding='utf-8') as out:
        out.write(latest_code)
