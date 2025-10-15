#!/usr/bin/env python3

import sys
import os
from main import run

def main():
    # Get the script file path (the .ss file being executed)
    # When run as shebang, the .ss file is in sys.argv[1]
    if len(sys.argv) > 1:
        script_file = sys.argv[1]
    else:
        script_file = sys.argv[0]

    # Check if file exists and has .ss extension
    if not os.path.exists(script_file):
        print(f"Error: File '{script_file}' not found")
        sys.exit(1)

    if not script_file.endswith('.ss'):
        print("Error: Script must have .ss extension")
        sys.exit(1)

    # Read the script content (skip the first line which is the shebang)
    with open(script_file, 'r') as f:
        lines = f.readlines()

    # Skip the shebang line (first line) and any empty lines
    source_lines = []
    for line in lines[1:]:  # Skip first line (shebang)
        if line.strip():  # Skip empty lines
            source_lines.append(line)

    source_code = ''.join(source_lines)

    # Run the script
    run(source_code, script_file)

if __name__ == "__main__":
    main()
