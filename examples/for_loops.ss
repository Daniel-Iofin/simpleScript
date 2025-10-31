#!/usr/bin/env python3 /Users/danieliofin/Documents/GitHub/simpleScript/ss_interpreter.py
// For loops and break/continue example

// Basic for loop
print("Basic for loop:");
for (let i = 0; i < 5; ) {
    print("i = " + str(i));
    i = i + 1;
}

// For loop with break
print("\nFor loop with break:");
for (let j = 0; j < 10; ) {
    if (j == 3) {
        print("Breaking at j = " + str(j));
        break;
    }
    print("j = " + str(j));
    j = j + 1;
}

// For loop with continue
print("\nFor loop with continue:");
for (let k = 0; k < 5; ) {
    k = k + 1;
    if (k == 2) {
        print("Skipping k = " + str(k));
        continue;
    }
    print("k = " + str(k));
}

// For loop with array
print("\nFor loop with array:");
let numbers = [10, 20, 30, 40, 50];
for (let idx = 0; idx < len(numbers); ) {
    print("numbers[" + str(idx) + "] = " + str(numbers[idx]));
    idx = idx + 1;
}

// While loop with break/continue for comparison
print("\nWhile loop with break:");
let counter = 0;
while (counter < 10) {
    if (counter == 5) {
        break;
    }
    print("counter = " + str(counter));
    counter = counter + 1;
}
