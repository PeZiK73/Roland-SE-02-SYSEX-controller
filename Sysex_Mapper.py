import mido
import time
import sys

def get_se02_ports():
    inputs = mido.get_input_names()
    outputs = mido.get_output_names()
    
    in_port_name = None
    out_port_name = None
    
    # Prioritize the USB SE-02 over UM-ONE
    for name in inputs:
        if "SE-02" in name:
            in_port_name = name
            break
            
    for name in outputs:
        if "SE-02" in name:
            out_port_name = name
            break
            
    if not in_port_name or not out_port_name:
        # Fallback to UM-ONE
        for name in inputs:
            if "UM-ONE" in name:
                in_port_name = name
                break
        for name in outputs:
            if "UM-ONE" in name:
                out_port_name = name
                break
                
    return in_port_name, out_port_name

# SE-02 RQ1 Requests
req_1 = mido.Message('sysex', data=[0x41, 0x10, 0x00, 0x00, 0x00, 0x44, 0x11, 0x05, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x40, 0x3B])
req_2 = mido.Message('sysex', data=[0x41, 0x10, 0x00, 0x00, 0x00, 0x44, 0x11, 0x05, 0x00, 0x00, 0x40, 0x00, 0x00, 0x00, 0x40, 0x7B])
req_3 = mido.Message('sysex', data=[0x41, 0x10, 0x00, 0x00, 0x00, 0x44, 0x11, 0x05, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x40, 0x3A])
req_4 = mido.Message('sysex', data=[0x41, 0x10, 0x00, 0x00, 0x00, 0x44, 0x11, 0x05, 0x00, 0x01, 0x40, 0x00, 0x00, 0x00, 0x30, 0x0A])

requests = [req_1, req_2, req_3, req_4]

def request_patch(inport, outport):
    responses = []
    # Clear input buffer
    for msg in inport.iter_pending():
        pass
        
    for req in requests:
        outport.send(req)
        # Wait for reply
        start = time.time()
        reply_received = False
        while time.time() - start < 1.0:
            msg = inport.poll()
            if msg and msg.type == 'sysex' and len(msg.data) > 6 and msg.data[6] == 0x12: # DT1
                responses.append(msg.data)
                reply_received = True
                break
            time.sleep(0.01)
        if not reply_received:
            print("Timeout waiting for response!")
            return None
    return responses

def compare_patches(baseline, new_patch):
    if not baseline or not new_patch: return
    
    found_diff = False
    for chunk_idx in range(4):
        base_data = baseline[chunk_idx]
        new_data = new_patch[chunk_idx]
        
        if len(base_data) != len(new_data):
            print(f"Chunk {chunk_idx + 1} length mismatch!")
            continue
            
        for i in range(len(base_data)):
            if base_data[i] != new_data[i]:
                # Ignoring checksum byte which is usually the last byte before F7 (so index -1 in data)
                if i == len(base_data) - 1:
                    continue
                found_diff = True
                
                # The address bytes are at index 7, 8, 9, 10
                address_offset = i - 11 # 11 is the start of the payload
                print(f"Difference found in Chunk {chunk_idx + 1} at payload offset {address_offset} (byte index {i}).")
                print(f"  Old value: {base_data[i]} (0x{base_data[i]:02X})")
                print(f"  New value: {new_data[i]} (0x{new_data[i]:02X})")
                
    if not found_diff:
        print("No differences found! (Are you sure the parameter changed?)")

def manual_mode():
    in_name, out_name = get_se02_ports()
    if not in_name or not out_name:
        print("Could not find SE-02 MIDI ports.")
        return
        
    print(f"Connecting to:\n  IN: {in_name}\n OUT: {out_name}")
    try:
        with mido.open_input(in_name) as inport, mido.open_output(out_name) as outport:
            print("Taking baseline snapshot...")
            baseline = request_patch(inport, outport)
            if not baseline:
                print("Failed to get baseline. Make sure the SE-02 is connected and not locked by another app.")
                return
                
            print("Baseline acquired!")
            input(">>> WAITING: Press Enter AFTER you have turned the knob or changed the setting on the hardware...")
            
            print("Taking new snapshot...")
            new_patch = request_patch(inport, outport)
            if not new_patch:
                print("Failed to get new patch.")
                return
                
            print("\n--- RESULTS ---")
            compare_patches(baseline, new_patch)
            print("---------------")
            
    except Exception as e:
        print(f"Error opening MIDI ports: {e}")
        print("Bitwig or the JUCE plugin might be locking the port. You may need to close the editor.")

def automated_mode():
    in_name, out_name = get_se02_ports()
    if not in_name or not out_name:
        print("Could not find SE-02 MIDI ports.")
        return
        
    print(f"Connecting to:\n  IN: {in_name}\n OUT: {out_name}")
    try:
        with mido.open_input(in_name) as inport, mido.open_output(out_name) as outport:
            for cc_num in range(0, 120): # Standard CC range
                # Wait a tiny bit between tests
                time.sleep(0.05)
                
                # Take baseline
                baseline = request_patch(inport, outport)
                if not baseline: continue
                
                # Send CC with value 127
                outport.send(mido.Message('control_change', channel=0, control=cc_num, value=127))
                time.sleep(0.05) # Give the hardware a tiny fraction of a second to process
                
                # Take new snapshot
                new_patch = request_patch(inport, outport)
                
                # Reset CC to 0
                outport.send(mido.Message('control_change', channel=0, control=cc_num, value=0))
                
                if not new_patch: continue
                
                # Compare
                print(f"--- Testing CC #{cc_num} ---")
                found = False
                for chunk_idx in range(4):
                    base_data = baseline[chunk_idx]
                    new_data = new_patch[chunk_idx]
                    if len(base_data) != len(new_data): continue
                        
                    for i in range(len(base_data)):
                        if base_data[i] != new_data[i] and i != len(base_data) - 1:
                            address_offset = i - 11
                            print(f"CC #{cc_num} -> Chunk {chunk_idx + 1}, Payload Offset {address_offset} (Byte Index {i}) [Values: {base_data[i]} -> {new_data[i]}]")
                            found = True
                
                if not found:
                    pass # CC might not be mapped to any SysEx parameter
                    
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    automated_mode()
