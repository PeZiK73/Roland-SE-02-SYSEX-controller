import json

log_path = r'C:\Users\Notandi\.gemini\antigravity\brain\2998c07f-d36f-45f4-a7b7-e5f7bbc844a5\.system_generated\logs\transcript.jsonl'

with open(log_path, 'r', encoding='utf-8') as f:
    for line in f:
        if 'showValuesBtn' in line and 'Colour' in line:
            pass # just a quick check

        if 'g.setColour' in line and 'showValues' in line:
            entry = json.loads(line)
            content = json.dumps(entry, indent=2)
            idx = content.find('showValues')
            start = max(0, idx - 100)
            end = min(len(content), idx + 1000)
            print(f"--- STEP {entry.get('step_index')} ---")
            print(content[start:end].replace('\\n', '\n').replace('\\r', '\r'))
            break
