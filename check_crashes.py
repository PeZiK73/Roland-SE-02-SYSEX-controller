import json

log_path = 'C:/Users/Notandi/.gemini/antigravity/brain/2998c07f-d36f-45f4-a7b7-e5f7bbc844a5/.system_generated/logs/transcript.jsonl'

crashes = []
with open(log_path, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            data = json.loads(line)
        except:
            continue
        
        if data.get('type') == 'USER_INPUT':
            content = data.get('content', '').lower()
            if 'crash' in content:
                # remove the <USER_REQUEST> tags and whitespace for clean printing
                clean = content.replace('<user_request>', '').replace('</user_request>', '').replace('<additional_metadata>', '').replace('</additional_metadata>', '').strip()
                crashes.append(clean.split('\n')[0])
                
print(f"Total crashes found: {len(crashes)}")
for i, c in enumerate(crashes):
    print(f"{i+1}: {c}")
