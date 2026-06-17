import json

log_path = r'C:\Users\Notandi\.gemini\antigravity\brain\2998c07f-d36f-45f4-a7b7-e5f7bbc844a5\.system_generated\logs\transcript.jsonl'

with open(log_path, 'r', encoding='utf-8') as f:
    for line in f:
        if 'sendRQ1Requests' in line:
            entry = json.loads(line)
            content = json.dumps(entry, indent=2)
            idx = content.find('sendRQ1Requests')
            if idx != -1:
                print(f"--- STEP {entry.get('step_index')} ---")
                start = max(0, idx - 100)
                end = min(len(content), idx + 2000)
                print(content[start:end].replace('\\n', '\n').replace('\\r', '\r'))
                break
