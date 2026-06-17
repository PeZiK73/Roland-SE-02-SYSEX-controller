import re

with open(r'C:\Users\Notandi\.gemini\antigravity\brain\2998c07f-d36f-45f4-a7b7-e5f7bbc844a5\.system_generated\steps\5537\content.md', 'r', encoding='utf-8') as f:
    text = f.read()

# Extract just the parameter names to see the full list of what is controllable
pattern = r'<td class="parameter human.*?">(.*?)</td>'
matches = re.findall(pattern, text, re.IGNORECASE)

print("ALL PARAMETERS:")
for match in matches:
    print(match.strip())

