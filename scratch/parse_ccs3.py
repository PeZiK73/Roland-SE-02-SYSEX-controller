import re

with open(r'C:\Users\Notandi\.gemini\antigravity\brain\2998c07f-d36f-45f4-a7b7-e5f7bbc844a5\.system_generated\steps\5537\content.md', 'r', encoding='utf-8') as f:
    text = f.read()

pattern = r'<td class="parameter human.*?">(.*?)</td>\s*<td.*?><a.*?>(.*?)</a>'
matches = re.findall(pattern, text, re.IGNORECASE)

if not matches:
    # Alternative format where the CC is just in a td
    pattern2 = r'<td class="parameter human.*?">(.*?)</td>\s*<td.*?>\s*(.*?)\s*</td>'
    matches = re.findall(pattern2, text, re.IGNORECASE)

for match in matches:
    print(f"{match[0].strip()}: {match[1].strip()}")

