import json
import os

log_path = 'C:/Users/Notandi/.gemini/antigravity/brain/2998c07f-d36f-45f4-a7b7-e5f7bbc844a5/.system_generated/logs/transcript_full.jsonl'

editor_cpp = ''
processor_cpp = ''
editor_h = ''
processor_h = ''

with open(log_path, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            data = json.loads(line)
        except:
            continue
            
        if data.get('created_at', '') > '2026-06-11T18:54:00Z':
            break
            
        if data.get('type') == 'PLANNER_RESPONSE':
            tool_calls = data.get('tool_calls', [])
            for call in tool_calls:
                if call['name'] == 'write_to_file':
                    args = call.get('args', {})
                    path = args.get('TargetFile', '')
                    content = args.get('CodeContent', '')
                    if 'PluginEditor.cpp' in path: editor_cpp = content
                    if 'PluginEditor.h' in path: editor_h = content
                    if 'PluginProcessor.cpp' in path: processor_cpp = content
                    if 'PluginProcessor.h' in path: processor_h = content
                elif call['name'] == 'run_command':
                    # Sometimes I overwrite files via bash commands. Let's not try to parse all of them, just assume the python scripts did the job.
                    pass

print("Extracted lengths:")
print("Editor.cpp:", len(editor_cpp))
print("Processor.cpp:", len(processor_cpp))
print("Editor.h:", len(editor_h))
print("Processor.h:", len(processor_h))
