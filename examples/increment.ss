#!/usr/bin/env python3 /Users/danieliofin/Documents/GitHub/simpleScript/ss_interpreter.py
// Increment/Decrement operators example

let x = 5;
print("Initial x: " + str(x));

// Postfix increment
let result = x++;
print("x++ returns: " + str(result));
print("x after x++: " + str(x));

// Prefix increment
result = ++x;
print("++x returns: " + str(result));
print("x after ++x: " + str(x));

// Postfix decrement
result = x--;
print("x-- returns: " + str(result));
print("x after x--: " + str(x));

// Prefix decrement
result = --x;
print("--x returns: " + str(result));
print("x after --x: " + str(x));

// Using in expressions
let y = 10;
let z = ++y + y++;
print("y: " + str(y));
print("z = ++y + y++: " + str(z));

// Using in loops
print("\nLoop with increment:");
for (let i = 0; i < 5; ) {
    print("i: " + str(i));
    i++;
}
