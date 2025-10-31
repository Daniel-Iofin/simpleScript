#!/usr/bin/env python3 /Users/danieliofin/Documents/GitHub/simpleScript/ss_interpreter.py
// Arrays example
let numbers = [1, 2, 3, 4, 5];
print("Original array: " + str(numbers));
print("Length: " + str(len(numbers)));

print("Element at index 2: " + str(numbers[2]));

// Modify array
numbers[0] = 10;
print("After modifying index 0: " + str(numbers));

// Array functions
push(numbers, 6);
print("After push: " + str(numbers));

let popped = pop(numbers);
print("Popped value: " + str(popped));
print("After pop: " + str(numbers));

let joined = join(numbers, ", ");
print("Joined: " + joined);

let sliced = slice(numbers, 1, 4);
print("Slice [1:4]: " + str(sliced));

// Empty array
let empty = [];
print("Empty array: " + str(empty));
push(empty, "hello");
push(empty, "world");
print("After adding elements: " + str(empty));
