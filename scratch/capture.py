import mido
import time

inport_name = [name for name in mido.get_input_names() if 'SE-02' in name]
if not inport_name:
    print("SE-02 not found")
    exit()

print(f"Listening on {inport_name[0]} for ALL MIDI messages...")

try:
    with mido.open_input(inport_name[0]) as inport:
        start_time = time.time()
        with open("C:/TEMP/ANTIGRAVITIY_ROLANDS_SCRIPTS/SE02_Controller/midi_capture.txt", "w") as f:
            while time.time() - start_time < 60:
                for msg in inport.iter_pending():
                    if msg.type not in ['clock', 'active_sensing']:
                        print(f"Captured: {msg}")
                        f.write(str(msg) + "\\n")
                        f.flush()
                time.sleep(0.1)
except Exception as e:
    print(f"Error: {e}")
