import re

with open('Source/PluginEditor.cpp', 'r') as f:
    content = f.read()

# 1. Update savePresetToFile vals
save_old = '''        if (maxDiscrete == 5) {
            float vals[6] = {10.0f, 32.0f, 53.0f, 74.0f, 95.0f, 116.0f};'''
save_new = '''        if (maxDiscrete == 5) {
            float vals[6] = {0.0f, 25.4f, 50.8f, 76.2f, 101.6f, 127.0f};'''
content = content.replace(save_old, save_new)

# 2. Update loadPresetFromFile vals
load_old = '''            if (maxDiscrete == 5) {
                float vals[6] = {10.0f, 32.0f, 53.0f, 74.0f, 95.0f, 116.0f};'''
load_new = '''            if (maxDiscrete == 5) {
                float vals[6] = {0.0f, 25.4f, 50.8f, 76.2f, 101.6f, 127.0f};'''
content = content.replace(load_old, load_new)

with open('Source/PluginEditor.cpp', 'w') as f:
    f.write(content)
