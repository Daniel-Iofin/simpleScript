#!/usr/bin/env python3 /Users/danieliofin/Documents/GitHub/programmingLanguage/ss_interpreter.py
// Functions example
def greet(name) {
    print("Hello, " + name + "!");
    return "Greeting sent";
}

def add(a, b) {
    return a + b;
}

def factorial(n) {
    if (n <= 1) {
        return 1;
    } else {
        return n * factorial(n - 1);
    }
}

def is_even(number) {
    return number % 2 == 0;
}

// Using the functions
let greeting = greet("World");
print(greeting);

let sum = add(5, 3);
print("5 + 3 = " + str(sum));

let fact = factorial(5);
print("Factorial of 5 = " + str(fact));

let num = 10;
if (is_even(num)) {
    print(str(num) + " is even");
} else {
    print(str(num) + " is odd");
}

// Built-in functions
let length = len("Hello");
print("Length of 'Hello': " + str(length));

let user_input = input("Enter your name: ");
print("You entered: " + user_input);
