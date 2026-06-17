import subprocess
import os
import sys

scripts = [
    'step5_fixes.py', 'step6_h.py', 'step6_cpp.py', 'step6_cpp_fix.py', 'step7_editor_fix.py',
    'step8_processor.py', 'step8_editor.py', 'generate_names.py', 'step1_processor_h.py',
    'step2_processor_cpp.py', 'step3_processor_cpp.py', 'step4_processor_cpp.py',
    'step5_processor_cpp.py', 'step6_processor_cpp.py', 'step7_editor_h.py',
    'step8_editor_cpp.py', 'step9_cmake.py', 'step10_clean_editor.py', 'step11_fix_timeout.py',
    'view_handler.py', 'step12_inject_hook.py', 'step13_sequential_sysex.py', 'step14_h.py',
    'step15_cpp.py', 'step16_clean_stray.py', 'step17.py', 'step18.py', 'step19.py',
    'step20.py', 'step21.py', 'step28.py', 'step30.py', 'step31.py', 'step32.py',
    'step34.py', 'step35.py', 'step36.py', 'step37.py', 'step38.py',
    'step39.py', 'step40.py', 'step41.py', 'step42.py', 'step43.py', 'step44.py',
    'step45.py', 'step46.py', 'step47.py', 'step48.py',
    'step55.py', 'step56.py', 'step57.py'
]

print('Resetting Source folder to 19:46 baseline...', flush=True)
subprocess.run(['powershell', '-Command', 'Remove-Item -Recurse -Force Source; Copy-Item -Recurse Source_backup Source'], check=True)

print('Restoring PresetBrowser.h and PresetBrowser.cpp...', flush=True)
subprocess.run(['python', 'extract_browser.py'], check=True)

print('Replaying patches sequentially up to 14:44 baseline...', flush=True)

for script in scripts:
    path = f'scratch/{script}'
    if not os.path.exists(path):
        continue
    
    res = subprocess.run(['python', path], capture_output=True, text=True)
    if res.returncode != 0:
        print(f'FATAL: {script} failed to execute!\nSTDERR: {res.stderr}\nSTDOUT: {res.stdout}', flush=True)
        sys.exit(1)
    
print('Rollback successful!', flush=True)
