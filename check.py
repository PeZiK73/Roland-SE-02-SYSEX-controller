
import re
with open('Source/PluginProcessor.cpp') as f: proc = f.read()
with open('Source/PluginEditor.cpp') as f: ed = f.read()
proc_ids = set(re.findall(r'addCcParam\(\"([^\"]+)\"', proc))
ed_ids = set(re.findall(r'add(?:Knob|Switch)\(\"([^\"]+)\"', ed))

missing_in_proc = ed_ids - proc_ids
missing_in_ed = proc_ids - ed_ids

print('Missing in processor:', missing_in_proc)
print('Missing in editor:', missing_in_ed)

