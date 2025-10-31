#!/usr/bin/env python3 /Users/danieliofin/Documents/GitHub/simpleScript/ss_interpreter.py
// Built-in functions example

// Math functions
print("Math functions:");
print("abs(-5): " + str(abs(-5)));
print("pow(2, 3): " + str(pow(2, 3)));
print("sqrt(16): " + str(sqrt(16)));
print("floor(3.7): " + str(floor(3.7)));
print("ceil(3.2): " + str(ceil(3.2)));
print("round(3.14159, 2): " + str(round(3.14159, 2)));
print("min(1, 5, 3): " + str(min(1, 5, 3)));
print("max(1, 5, 3): " + str(max(1, 5, 3)));

// String functions
print("\nString functions:");
let text = "Hello, World!";
print("Original: " + text);
print("substring(text, 7): " + substring(text, 7));
print("substring(text, 0, 5): " + substring(text, 0, 5));
print("replace(text, 'World', 'Universe'): " + replace(text, "World", "Universe"));
print("tolower(text): " + tolower(text));
print("toupper(text): " + toupper(text));
print("startswith(text, 'Hello'): " + str(startswith(text, "Hello")));
print("endswith(text, '!'): " + str(endswith(text, "!")));

// Split function
let sentence = "The quick brown fox";
let words = split(sentence, " ");
print("split('" + sentence + "', ' '): " + str(words));

// Array functions (additional)
print("\nArray functions:");
let numbers = [1, 2, 3, 4, 5];
print("Original array: " + str(numbers));
print("slice(numbers, 1, 4): " + str(slice(numbers, 1, 4)));
print("join(numbers, '-'): " + join(numbers, "-"));

// Utility functions
print("\nUtility functions:");
print("range(5): " + str(range(5)));
print("range(1, 6): " + str(range(1, 6)));
print("range(0, 10, 2): " + str(range(0, 10, 2)));

let test_values = [42, "hello", true, [1, 2, 3]];
for (let i = 0; i < len(test_values); ) {
    let val = test_values[i];
    print("type(" + str(val) + "): " + type(val));
    i++;
}
