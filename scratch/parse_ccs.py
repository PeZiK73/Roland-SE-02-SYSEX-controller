import re

with open(r'C:\Users\Notandi\.gemini\antigravity\brain\2998c07f-d36f-45f4-a7b7-e5f7bbc844a5\.system_generated\steps\5537\content.md', 'r', encoding='utf-8') as f:
    text = f.read()

# Extract parameters and CCs
pattern = r'<td class="parameter human.*?">(.*?)</td>\s*<td.*?><a.*?>(.*?)</a>'
matches = re.findall(pattern, text, re.IGNORECASE)

for match in matches:
    if "Oscillator" in match[0] or "Xmod" in match[0]:
        print(f"{match[0]}: {match[1]}")
