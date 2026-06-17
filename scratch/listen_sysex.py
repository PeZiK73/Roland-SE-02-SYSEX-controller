import mido
import time

inport_name = [name for name in mido.get_input_names() if 'SE-02' in name]
if not inport_name:
    print("SE-02 not found")
    exit()

print(f"Listening on {inport_name[0]} for SysEx...")
try:
    with mido.open_input(inport_name[0]) as inport:
        start_time = time.time()
        while time.time() - start_time < 300:
            for msg in inport.iter_pending():
                if msg.type == 'sysex':
                    print("Received SysEx!")
                    with open("C:/TEMP/ANTIGRAVITIY_ROLANDS_SCRIPTS/SE02_Controller/sysex_dump.txt", "w") as f:
                        f.write(msg.hex() + "\\n")
                    exit(0)
            time.sleep(0.1)
        print("Timeout waiting for SysEx")
except Exception as e:
    print(f"Error: {e}")
