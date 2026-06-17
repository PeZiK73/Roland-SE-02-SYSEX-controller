python -c "
import json
with open('C:/Users/Notandi/.gemini/antigravity/brain/2998c07f-d36f-45f4-a7b7-e5f7bbc844a5/.system_generated/logs/transcript_full.jsonl', 'r') as f:
    for line in f:
        if 'PresetGrid::PresetGrid(SE02_ControllerAudioProcessor' in line and 'PLANNER_RESPONSE' in line:
            obj = json.loads(line)
            with open('raw_tool_call.json', 'w') as out:
                json.dump(obj, out)
            print('Extracted!')
            break
"