#!/usr/bin/env python3 /Users/danieliofin/Documents/GitHub/simpleScript/ss_interpreter.py
// Compound assignment operators example

let x = 10;
print("Initial x: " + str(x));

x += 5;
print("x += 5: " + str(x));

x -= 3;
print("x -= 3: " + str(x));

x *= 2;
print("x *= 2: " + str(x));

x /= 4;
print("x /= 4: " + str(x));

x %= 3;
print("x %= 3: " + str(x));

// With arrays
let arr = [1, 2, 3];
print("Initial array: " + str(arr));

arr[0] += 10;
print("arr[0] += 10: " + str(arr));

arr[1] *= 3;
print("arr[1] *= 3: " + str(arr));
