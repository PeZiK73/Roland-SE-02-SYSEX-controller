import json
import os

log_path = r'C:\Users\Notandi\.gemini\antigravity\brain\2998c07f-d36f-45f4-a7b7-e5f7bbc844a5\.system_generated\logs\transcript.jsonl'

with open(log_path, 'r', encoding='utf-8') as f:
    for line in f:
        if 'showParameters' in line or 'Show parameters' in line or 'showValuesBtn' in line:
            print("Found reference to Show parameters")
            # print snippet
            entry = json.loads(line)
            content = json.dumps(entry, indent=2)
            idx = content.find('showValues')
            if idx == -1: idx = content.find('showParameters')
            if idx == -1: idx = content.find('Show parameters')
            start = max(0, idx - 100)
            end = min(len(content), idx + 2000)
            print(content[start:end].replace('\\n', '\n').replace('\\r', '\r'))
            break
