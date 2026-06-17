import sys
try:
    import mido
except ImportError:
    print("mido not installed")
    sys.exit(0)

print("Inputs:", mido.get_input_names())
print("Outputs:", mido.get_output_names())
