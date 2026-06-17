import mido
import time

inports = [name for name in mido.get_input_names() if 'SE-02' in name]
outports = [name for name in mido.get_output_names() if 'SE-02' in name]

if not inports or not outports:
    print("SE-02 ports not found")
    exit()

def send_rq1(outport, address, size):
    # F0 41 10 00 00 00 44 11 [Address 4] [Size 4] [Checksum] F7
    # Model ID 00 00 00 44
    msg_bytes = [0x41, 0x10, 0x00, 0x00, 0x00, 0x44, 0x11]
    msg_bytes.extend(address)
    msg_bytes.extend(size)
    
    checksum_sum = sum(address) + sum(size)
    checksum = (128 - (checksum_sum % 128)) % 128
    
    msg_bytes.append(checksum)
    
    msg = mido.Message('sysex', data=msg_bytes)
    outport.send(msg)

with mido.open_input(inports[0]) as inport, mido.open_output(outports[0]) as outport:
    print(f"Opened {inports[0]} and {outports[0]}")
    
    addresses = [
        [0x01, 0x00, 0x00, 0x00],
        [0x02, 0x00, 0x00, 0x00],
        [0x11, 0x00, 0x00, 0x00],
        [0x00, 0x00, 0x00, 0x00],
        [0x00, 0x01, 0x00, 0x00]
    ]
    size = [0x00, 0x00, 0x00, 0x40] # 64 bytes
    
    for addr in addresses:
        print(f"Trying address {addr}...")
        send_rq1(outport, addr, size)
        time.sleep(0.5)
        for msg in inport.iter_pending():
            if msg.type == 'sysex':
                print(f"Success! Response to {addr}: {msg.hex()}")
                with open("C:/TEMP/ANTIGRAVITIY_ROLANDS_SCRIPTS/SE02_Controller/sysex_dump.txt", "w") as f:
                    f.write(msg.hex() + "\\n")
                exit(0)
    print("No response from SE-02")
