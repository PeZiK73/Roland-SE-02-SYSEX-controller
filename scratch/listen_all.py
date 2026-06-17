import mido
import time

inport_name = [name for name in mido.get_input_names() if 'SE-02' in name]
if not inport_name:
    print("SE-02 not found")
    exit()

print(f"Listening on {inport_name[0]} for ALL MIDI messages...")
messages = []

try:
    with mido.open_input(inport_name[0]) as inport:
        start_time = time.time()
        while time.time() - start_time < 300:
            for msg in inport.iter_pending():
                if msg.type != 'clock' and msg.type != 'active_sensing':
                    print(msg)
                    messages.append(str(msg))
                    with open("C:/TEMP/ANTIGRAVITIY_ROLANDS_SCRIPTS/SE02_Controller/midi_dump.txt", "a") as f:
                        f.write(str(msg) + "\\n")
            time.sleep(0.01)
except Exception as e:
    print(f"Error: {e}")
