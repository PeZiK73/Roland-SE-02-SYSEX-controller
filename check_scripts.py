import os
scripts = [
    'step5_fixes.py', 'step6_h.py', 'step6_cpp.py', 'step6_cpp_fix.py', 'step7_editor_fix.py',
    'step8_processor.py', 'step8_editor.py', 'generate_names.py', 'step1_processor_h.py',
    'step2_processor_cpp.py', 'step3_processor_cpp.py', 'step4_processor_cpp.py',
    'step5_processor_cpp.py', 'step6_processor_cpp.py', 'step7_editor_h.py',
    'step8_editor_cpp.py', 'step9_cmake.py', 'step10_clean_editor.py', 'step11_fix_timeout.py',
    'view_handler.py', 'step12_inject_hook.py', 'step13_sequential_sysex.py', 'step14_h.py',
    'step15_cpp.py', 'step16_clean_stray.py', 'step17.py', 'step18.py', 'step19.py',
    'step20.py', 'step21.py', 'step23.py', 'step24.py', 'step25.py', 'step26.py',
    'step27.py', 'step28.py', 'step29.py', 'step30.py', 'step31.py', 'step32.py',
    'step33.py', 'step34.py', 'step35.py', 'step36.py', 'step37.py', 'step38.py',
    'step39.py', 'step40.py', 'step41.py', 'step42.py', 'step43.py', 'step44.py',
    'step45.py', 'step46.py', 'step47.py', 'step48.py', 'step49.py', 'step50.py',
    'step51.py', 'step52.py', 'step53.py', 'step54.py', 'step55.py', 'step56.py',
    'step57.py', 'step58.py'
]

skip = []
for script in scripts:
    path = f'scratch/{script}'
    if not os.path.exists(path): continue
    with open(path, 'r') as f:
        code = f.read()
        if 'PresetBrowser.h' in code or 'PresetBrowser.cpp' in code:
            skip.append(script)
            
print(skip)
