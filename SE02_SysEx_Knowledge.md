# Roland SE-02 SysEx Knowledge Base

Based on reverse-engineering efforts from the Electra One community (specifically user `NewIgnis`), the Roland SE-02 has an undocumented SysEx implementation for patch retrieval and parsing. Here are the key findings from intercepting the official SE-02 software editor:

## 1. SysEx Header Format
The SE-02 adheres to standard Roland SysEx formatting:
- `F0` - SysEx Start
- `41` - Roland Manufacturer ID
- `10` - Device ID
- `00 00 00 44` - SE-02 Model ID
- `11` - Command: RQ1 (Request Data)
- `12` - Command: DT1 (Data Transmission / Response)

## 2. Edit Buffer Patch Requests
When the editor asks the SE-02 for the current patch (the Edit Buffer), it must send exactly **4 request messages**. 
The SE-02 responds with **4 chunks of data** matching those requests.

**The 4 Request Strings (Hex):**
1. `F0 41 10 00 00 00 44 11 05 00 00 00 00 00 00 40 3B F7` -> Responds with **78 bytes**
2. `F0 41 10 00 00 00 44 11 05 00 00 40 00 00 00 40 7B F7` -> Responds with **78 bytes**
3. `F0 41 10 00 00 00 44 11 05 00 01 00 00 00 00 40 3A F7` -> Responds with **78 bytes**
4. `F0 41 10 00 00 00 44 11 05 00 01 40 00 00 00 30 0A F7` -> Responds with **62 bytes**

*Note: In the responses, the 8th byte (`11` for request) flips to `12` (Data Transfer), followed by the address, the payload data, the checksum, and `F7`.*

## 3. Patch Names
Patch names are fixed at **16 characters long** and are padded with `00` bytes. 
For example, a patch named "Inbound" would be encoded as `49 6E 62 6F 75 6E 64` followed by nine `00` bytes.

## 4. Parameter Scaling (SysEx vs CC)
There is a known discrepancy between how the SE-02 handles values over MIDI CC versus how it handles them internally in SysEx.
- **SysEx Scale:** Discrete parameters are usually stored as their exact index (e.g., `0` to `5` for a 6-position rotary switch like VCO1 Range).
- **MIDI CC Scale:** The same parameter over CC is spread across the 0-127 range (e.g., `0, 25, 51, 76, 102, 127`).
*When parsing SysEx dumps back into UI components, a translation function is required to map the discrete SysEx index (0-5) back to the normalized UI/CC value.*

## 5. Global Settings Retrieval
When the official editor first connects, it sends two specific SysEx requests to interrogate the SE-02's global state. The responses contain:
- Roland Firmware Version (e.g., v1.11)
- Global MIDI Channel
- MIDI Thru Setting (On/Off)
