###
# Greg Jewell
# Phase 1.2 Limp, main file
###

import os
import sys
from Lexp import *

if __name__ == "__main__":
    try:
        try:
            print("Starting!")
            open(sys.argv[2], 'w').close()  # Clears current content of file to prevent continuous appending
            with open(sys.argv[1], "rt") as file:
                count = 0
                lines = []
                for line in file.readlines():
                    count = count + 1
                    if len(line) > 1:  # Check for 'empty' lines
                        line = line.rstrip('\n')
                        line = line.lstrip(' ')
                        lines.append([count, tokenize(sys.argv[2], line)])

            print("Tokenizing Complete!")

            print(f"Printing to {sys.argv[2]}")
            output(lines)

            print("Parsing!")
            parse()

            print("Operation Complete!")

        except IOError:
            print(f"{sys.argv[1]} not found")
            exit(0)

    except IndexError:
        print("A file is required.")
        print("Ex.) python3 Limp.py input.txt output.txt")
    except:
        print("Unidentified Error Occurred")
