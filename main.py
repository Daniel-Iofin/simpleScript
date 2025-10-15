#!/usr/bin/env python3

import sys
import os
from lexer import Lexer
from parser import Parser
from interpreter import Interpreter, RuntimeError

def run_file(filename):
    if not os.path.exists(filename):
        print(f"Error: File '{filename}' not found")
        sys.exit(1)

    with open(filename, 'r') as f:
        source_code = f.read()

    run(source_code, filename)

def run(source_code, filename="<string>"):
    try:
        # Lexing
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()

        # Parsing
        parser = Parser(tokens)
        program = parser.parse_program()

        # Interpretation
        interpreter = Interpreter()
        interpreter.interpret(program)

    except ValueError as e:
        print(f"Syntax Error: {e}")
        sys.exit(1)
    except RuntimeError as e:
        print(f"Runtime Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <filename>")
        print("Example: python main.py examples/hello.ss")
        sys.exit(1)

    filename = sys.argv[1]
    run_file(filename)

if __name__ == "__main__":
    main()
