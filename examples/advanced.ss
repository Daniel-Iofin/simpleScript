#!/usr/bin/env python3 /Users/danieliofin/Documents/GitHub/simpleScript/ss_interpreter.py

print("=== SimpleScript Advanced Features Demo ===\n");

// 1. Arrays
print("1. Arrays:");
let fruits = ["Apple", "Banana", "Cherry"];
print("Fruits: " + str(fruits));
push(fruits, "Date");
print("After push: " + str(fruits));
let last = pop(fruits);
print("Popped: " + last + ", Remaining: " + str(fruits));

// Array access and modification
fruits[1] = "Blueberry";
print("Modified fruits[1]: " + str(fruits));

// 2. For loops with break/continue
print("\n2. For loops with break/continue:");
for (let i = 0; i < 10; ) {
    if (i == 3) {
        print("Breaking at i = " + str(i));
        break;
    }
    if (i % 2 == 0) {
        print("Even: " + str(i));
    } else {
        print("Skipping odd: " + str(i));
        i++;
        continue;
    }
    i++;
}

// 3. Increment/Decrement operators
print("\n3. Increment/Decrement operators:");
let counter = 5;
print("Initial counter: " + str(counter));
print("Postfix increment: " + str(counter++));
print("After postfix: " + str(counter));
print("Prefix increment: " + str(++counter));
print("Prefix decrement: " + str(--counter));

// 4. Compound assignment operators
print("\n4. Compound assignment operators:");
let value = 10;
print("Initial value: " + str(value));
value += 5;
print("After += 5: " + str(value));
value *= 2;
print("After *= 2: " + str(value));
value /= 3;
print("After /= 3: " + str(value));

// Compound assignment with arrays
let scores = [10, 20, 30];
scores[0] += 5;
scores[1] *= 2;
print("Modified scores: " + str(scores));

// 5. Advanced built-in functions
print("\n5. Advanced built-in functions:");

// Math functions
let num = -3.14159;
print("abs(" + str(num) + "): " + str(abs(num)));
print("sqrt(25): " + str(sqrt(25)));
print("pow(2, 8): " + str(pow(2, 8)));
print("floor(3.9): " + str(floor(3.9)));
print("ceil(3.1): " + str(ceil(3.1)));
print("round(3.14159, 2): " + str(round(3.14159, 2)));

// String functions
let message = "Hello, SimpleScript World!";
print("Original: " + message);
print("tolower: " + tolower(message));
print("toupper: " + toupper(message));
print("substring(7, 18): " + substring(message, 7, 18));
print("replace('SimpleScript', 'AwesomeScript'): " + replace(message, "SimpleScript", "AwesomeScript"));
print("startswith('Hello'): " + str(startswith(message, "Hello")));
print("endswith('!'): " + str(endswith(message, "!")));

// Array utilities
let data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
print("Original data: " + str(data));
print("slice(2, 7): " + str(slice(data, 2, 7)));
print("join with '-': " + join(data, "-"));

// Range function
let indices = range(5);
print("range(5): " + str(indices));

let even_numbers = range(0, 11, 2);
print("range(0, 11, 2): " + str(even_numbers));

// Type checking
print("\n6. Type checking:");
let test_values = [42, 3.14, "hello", true, [1, 2, 3]];
for (let i = 0; i < len(test_values); ) {
    let val = test_values[i];
    print("Value: " + str(val) + " -> Type: " + type(val));
    i++;
}

// 7. Complex example: Finding primes
print("\n7. Finding prime numbers using arrays and loops:");

def is_prime(n) {
    if (n <= 1) {
        return false;
    }
    if (n <= 3) {
        return true;
    }
    if (n % 2 == 0 || n % 3 == 0) {
        return false;
    }

    for (let i = 5; i * i <= n; ) {
        if (n % i == 0 || n % (i + 2) == 0) {
            return false;
        }
        i += 6;
    }
    return true;
}

let primes = [];
for (let num = 2; num <= 50; ) {
    if (is_prime(num)) {
        push(primes, num);
    }
    num++;
}

print("Prime numbers up to 50: " + str(primes));
print("Found " + str(len(primes)) + " prime numbers");

// 8. Array manipulation with functions
print("\n8. Array manipulation:");

def double_array(arr) {
    let result = [];
    for (let i = 0; i < len(arr); ) {
        push(result, arr[i] * 2);
        i++;
    }
    return result;
}

def filter_even(arr) {
    let result = [];
    for (let i = 0; i < len(arr); ) {
        if (arr[i] % 2 == 0) {
            push(result, arr[i]);
        }
        i++;
    }
    return result;
}

let numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
let doubled = double_array(numbers);
let evens = filter_even(numbers);

print("Original: " + str(numbers));
print("Doubled: " + str(doubled));
print("Evens only: " + str(evens));

print("\n=== Demo Complete ===");
