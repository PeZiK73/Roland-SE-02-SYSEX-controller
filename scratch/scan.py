import mido
import time

inports = [name for name in mido.get_input_names() if 'SE-02' in name]
outports = [name for name in mido.get_output_names() if 'SE-02' in name]

def send_rq1(outport, address, size):
    msg_bytes = [0x41, 0x10, 0x00, 0x00, 0x00, 0x44, 0x11]
    msg_bytes.extend(address)
    msg_bytes.extend(size)
    checksum = (128 - ((sum(address) + sum(size)) % 128)) % 128
    msg_bytes.append(checksum)
    msg = mido.Message('sysex', data=msg_bytes)
    outport.send(msg)

with mido.open_input(inports[0]) as inport, mido.open_output(outports[0]) as outport:
    print("Scanning memory map...")
    
    # Common Roland memory maps:
    # 01 00 00 00 System
    # 02 00 00 00 Temporary Patch / Tone
    # 11 00 00 00 User Patch 1
    
    addresses_to_try = []
    for high_byte in [0x01, 0x02, 0x11]:
        for mid_byte in [0x00, 0x10, 0x20]:
            addresses_to_try.append([high_byte, 0x00, mid_byte, 0x00])

    size = [0x00, 0x00, 0x02, 0x00] # Request 256 bytes

    responses = {}

    for addr in addresses_to_try:
        send_rq1(outport, addr, size)
        time.sleep(0.3)
        for msg in inport.iter_pending():
            if msg.type == 'sysex':
                data_len = len(msg.data) - 13 # subtract header and checksum
                print(f"Address {addr} -> Got {data_len} bytes")
                responses[str(addr)] = msg.hex()

    with open("C:/TEMP/ANTIGRAVITIY_ROLANDS_SCRIPTS/SE02_Controller/sysex_scan.txt", "w") as f:
        for addr, hex_str in responses.items():
            f.write(f"{addr}: {hex_str}\\n")
    print("Done scanning.")
