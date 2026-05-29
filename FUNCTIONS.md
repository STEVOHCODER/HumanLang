# HumanLang Function Examples

Use `.hl` files and run them with:

```powershell
hl run your_file.hl
```

## Output

```humanlang
say "Hello"
show "Hello"
print "Hello"
```

## Text Input

```humanlang
ask "What is your name?" and remember it as user name
get "What is your name?" and remember it as user name
say "Hello " plus user name
```

## Number Input

```humanlang
ask number "Enter a number:" and remember it as first number
get number "Enter a number:" and remember it as second number
say number "Enter a number:" and remember it as third number
```

## Variables

```humanlang
remember 10 as first number
remember "Steven" as user name
set first number to 20
change first number to 30
```

## Arithmetic

```humanlang
calculate first number plus second number
calculate first number minus second number
calculate first number times second number
calculate first number multiplied by second number
calculate first number divided by second number
calculate first number modulo second number
calculate first number to the power of second number
calculate first number plus second number as addition
calculate first number plus second number as addition,
```

`calculate ... as addition` stores the answer. `calculate ... as addition,` stores and prints the answer.

## Scientific Math

```humanlang
calculate the square root of 16
calculate the sine of radians of 90
calculate the cosine of radians of 0
calculate the tangent of radians of 45
calculate the log of 1000
calculate the natural log of e
calculate the absolute value of -10
calculate the floor of 4.9
calculate the ceiling of 4.1
calculate the factorial of 5
calculate the rounded value of 4.7
```

## Helpers

```humanlang
calculate average of first number and second number
calculate the maximum of first number and second number
calculate the minimum of first number and second number
calculate 10 percent of first number
```

## Conditions

```humanlang
if age is at least 18:
    say "Adult"
otherwise:
    say "Minor"
```

Supported comparisons:

```humanlang
is
is not
equals
does not equal
is greater than
is less than
is at least
is at most
```

## Repeat

```humanlang
repeat 3 times:
    say "Hello"
```

## Lists

```humanlang
make list "apples", "bananas" and "mangoes" as fruits
create list 1, 2 and 3 as numbers
add "oranges" to fruits
calculate length of fruits

for each fruit in fruits:
    say fruit
```

## Random

```humanlang
calculate random integer between 1 and 6
calculate random number between 1 and 2
```

## Date And Time

```humanlang
remember current date as today
remember current time as now
remember current datetime as timestamp
say today
```

## Files

```humanlang
write "Hello" to file "note.txt"
append " world" to file "note.txt"
read file "note.txt" as note text
say note text
```

## Comments

```humanlang
# This is a comment
// This is also a comment
```

## Functions

```humanlang
to greet user with name:
    say "Hello " plus name
end

greet user with "Steven"
```

## Maps

```humanlang
make map "name": "Steven", "age": 25 as user profile
say user profile's "name"
```

## Compound Logic

```humanlang
if age is at least 18 and status is "active":
    say "Access granted"
```

## While Loops

```humanlang
while balance is greater than 0:
    say balance
    change balance to balance minus 1
```

## String Tools

```humanlang
calculate lowercase of text as lower text
calculate uppercase of text as upper text
calculate replace "apple" with "orange" in text as changed text
split text by "," as parts
```

## Type Conversion

```humanlang
calculate number of "123" as my value
calculate integer of "123" as my integer
calculate text of 456 as my string
```

## Error Handling

```humanlang
try:
    read file "config.txt" as data
if error:
    say "Could not find the file"
```

## Modules

```humanlang
use "math_helpers.hl"
double number with 21
```
