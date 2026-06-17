import sys

with open('Source/PluginEditor.cpp', 'r') as f:
    editor = f.read()
with open('Source/PluginProcessor.cpp', 'r') as f:
    proc = f.read()

import re
def get_block(text, start_str, end_str):
    start = text.find(start_str)
    if start == -1: return ""
    end = text.find(end_str, start)
    if end == -1: return ""
    return text[start:end]

ed_block = get_block(editor, 'formatLine("CTRL_GLIDE", "GLIDE", -1);', 'file.replaceWithText(lines.joinIntoString')
pr_block = get_block(proc, 'formatLine("CTRL_GLIDE", "GLIDE", -1);', 'file.replaceWithText(lines.joinIntoString')

if ed_block == pr_block:
    print("Blocks are exactly identical!")
else:
    print("Blocks differ!")
    print("Editor block length:", len(ed_block))
    print("Processor block length:", len(pr_block))

