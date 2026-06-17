import json

log_path = r'C:\Users\Notandi\.gemini\antigravity\brain\2998c07f-d36f-45f4-a7b7-e5f7bbc844a5\.system_generated\logs\transcript.jsonl'

with open(log_path, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            entry = json.loads(line)
            if entry.get('step_index') == 2675:
                for call in entry['tool_calls']:
                    args = call.get('args', {})
                    for item in args.get('ReplacementChunks', []):
                        content = item.get('ReplacementContent', '')
                        if 'void SE02_ControllerAudioProcessor::requestSysExPreset()' in content:
                            with open('scratch/rq1.cpp', 'w', encoding='utf-8') as out:
                                out.write(content)
                            print("Saved to scratch/rq1.cpp")
        except Exception as e:
            pass
