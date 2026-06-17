import json
import re

log_path = r'C:\Users\Notandi\.gemini\antigravity\brain\2998c07f-d36f-45f4-a7b7-e5f7bbc844a5\.system_generated\logs\transcript.jsonl'

with open(log_path, 'r', encoding='utf-8') as f:
    for line in f:
        if 'void SE02_ControllerAudioProcessor::requestSysExPreset()' in line:
            # We found a line with it. Print the surrounding json
            entry = json.loads(line)
            content = json.dumps(entry, indent=2)
            # Find the index of the function and print 1000 characters around it
            idx = content.find('void SE02_ControllerAudioProcessor::requestSysExPreset()')
            if idx != -1:
                print(f"--- STEP {entry.get('step_index')} ---")
                start = max(0, idx - 100)
                end = min(len(content), idx + 2000)
                print(content[start:end].replace('\\n', '\n').replace('\\r', '\r'))
                break
