#!/usr/bin/env python3 /Users/danieliofin/Documents/GitHub/programmingLanguage/ss_interpreter.py
// Control flow example with if/else and while loops
let x = 10;

if (x > 5) {
    print("x is greater than 5");
} else {
    print("x is less than or equal to 5");
}

let counter = 0;
while (counter < 5) {
    print("Counter: " + str(counter));
    counter = counter + 1;
}

// More complex condition
let age = 20;
let can_vote = age >= 18;
if (can_vote) {
    print("You can vote!");
} else {
    print("You cannot vote yet.");
}

// Loop with condition
let i = 1;
while (i <= 10) {
    if (i % 2 == 0) {
        print(str(i) + " is even");
    } else {
        print(str(i) + " is odd");
    }
    i = i + 1;
}
