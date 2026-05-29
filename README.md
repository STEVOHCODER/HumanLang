# HumanLang

HumanLang is a simple English-like programming language for people who want to code by writing clear instructions.

This first version lets you write `.hl` files in English and run them from the command line. Python is used as the hidden runtime.

## Install

Open PowerShell in this folder and run:

```powershell
.\install.ps1
```

Or double-click:

```text
install.bat
```

After install, check it:

```powershell
humanlang --help
```

You can also use the short command:

```powershell
hl --help
```

If Windows says `humanlang` is not recognized, add this folder to your user `PATH`:

```text
C:\Users\NIYOMUGABO Steven\AppData\Roaming\Python\Python314\Scripts
```

You can still run HumanLang from this project folder without changing `PATH`:

```powershell
.\humanlang.cmd run examples\simple.hl
```

The project also includes a starter app:

```powershell
humanlang run app.hl
hl run app.hl
```

## Example

```humanlang
ask "What is your name?" and remember it as name
remember 20 as age

say "Hello " plus name

if age is at least 18:
    say "You are an adult"
otherwise:
    say "You are not an adult"
```

Run it:

```powershell
humanlang run examples\hello.hl
```

From inside this project folder, this also works:

```powershell
.\humanlang.cmd run examples\hello.hl
```

Build it into Python if you want to see what HumanLang creates:

```powershell
humanlang build examples\hello.hl --out hello.py
```

Print the generated Python:

```powershell
humanlang translate examples\hello.hl
```

## VS Code

Use the `.hl` extension:

```text
hello.hl
```

To add basic HumanLang syntax highlighting in VS Code:

1. Open the folder `vscode\humanlang-language`.
2. Copy that folder into your VS Code extensions folder:

```powershell
Copy-Item -Recurse vscode\humanlang-language "$env:USERPROFILE\.vscode\extensions\humanlang-language"
```

3. Restart VS Code.

Now `.hl` files will be detected as HumanLang.

## Commands

```powershell
humanlang run examples\hello.hl
humanlang build examples\hello.hl --out hello.py
humanlang translate examples\hello.hl
humanlang run app.hl
humanlang run examples\science_demo.hl
humanlang run examples\scientific_calculator.hl
humanlang run examples\your_calculator.hl
humanlang run examples\minimal_calculator.hl
humanlang run examples\all_functions.hl
humanlang run examples\data_tools.hl
humanlang run examples\real_app_basics.hl
humanlang run examples\modules_demo.hl
humanlang run examples\safety_and_control.hl
humanlang run examples\arguments_demo.hl hello
```

## Current HumanLang Rules

| HumanLang | Python |
| --- | --- |
| `say "Hello"` | `print("Hello")` |
| `show "Hello"` | `print("Hello")` |
| `print "Hello"` | `print("Hello")` |
| `ask "Name?" and remember it as name` | `name = input("Name? ")` |
| `get "Name?" and remember it as name` | `name = input("Name? ")` |
| `remember 20 as age` | `age = 20` |
| `ask number "Value?" and remember it as value` | `value = float(input("Value? "))` |
| `get number "Value?" and remember it as value` | `value = float(input("Value? "))` |
| `say number "Value?" and remember it as value` | `value = float(input("Value? "))` |
| `ask number "Value?" and remember it as a first number` | `first_number = float(input("Value? "))` |
| `calculate value plus 10 as total` | `total = value + 10` |
| `calculate value plus 10` | `print(value + 10)` |
| `calculate first number plus second number as addition` | `addition = first_number + second_number` |
| `if age is at least 18:` | `if age >= 18:` |
| `otherwise:` | `else:` |
| `plus` | `+` |
| `minus` | `-` |
| `times` | `*` |
| `divided by` | `/` |
| `to the power of` | `**` |
| `the square root of 16` | `math.sqrt(16)` |
| `the sine of radians of 90` | `math.sin(math.radians(90))` |
| `the cosine of radians of 90` | `math.cos(math.radians(90))` |
| `the log of 1000` | `math.log10(1000)` |
| `the natural log of e` | `math.log(math.e)` |
| `the absolute value of -10` | `abs(-10)` |
| `the floor of 4.9` | `math.floor(4.9)` |
| `the ceiling of 4.1` | `math.ceil(4.1)` |
| `the factorial of 5` | `math.factorial(5)` |
| `the rounded value of 4.7` | `round(4.7)` |
| `average of a and b` | `(a + b) / 2` |
| `the maximum of a and b` | `max(a, b)` |
| `the minimum of a and b` | `min(a, b)` |
| `10 percent of value` | `(10 / 100) * value` |
| `pi` | `math.pi` |
| `repeat 3 times:` | `for _ in range(int(3)):` |
| `make list "a", "b" as items` | `items = ["a", "b"]` |
| `add "c" to items` | `items.append("c")` |
| `for each item in items:` | `for item in items:` |
| `length of items` | `len(items)` |
| `random integer between 1 and 6` | `random.randint(1, 6)` |
| `random number between 1 and 2` | `random.uniform(1, 2)` |
| `current date` | today's date |
| `current time` | current time |
| `write "Hello" to file "note.txt"` | writes a file |
| `append " world" to file "note.txt"` | appends to a file |
| `read file "note.txt" as text` | reads a file |
| `to greet user with name:` | defines a function |
| `greet user with "Steven"` | calls a function |
| `make map "name": "Steven" as user profile` | creates a map |
| `user profile's "name"` | reads a map value |
| `if age is at least 18 and status is "active":` | compound condition |
| `otherwise if score is at least 80:` | else-if condition |
| `while balance is greater than 0:` | while loop |
| `yes` / `no` | booleans |
| `first item of fruits` | first list item |
| `item 2 of fruits` | second list item |
| `remove "apple" from fruits` | remove from list |
| `"apple" is in fruits` | list membership |
| `message contains "error"` | text containment |
| `message contains "error" ignoring case` | case-insensitive containment |
| `wait 2 seconds` | pause program |
| `argument 1` | first command-line argument |
| `command arguments` | all command-line arguments |
| `get from "https://example.com" as response` | download web text |
| `exit program` | stop the program |
| `lowercase of text` | lowercase text |
| `uppercase of text` | uppercase text |
| `replace "a" with "b" in text` | replace text |
| `split text by "," as parts` | split text into a list |
| `number of "123"` | convert text to number |
| `text of 456` | convert value to text |
| `try:` / `if error:` | handle errors |
| `use "helpers.hl"` | import another HumanLang file |

See [FUNCTIONS.md](FUNCTIONS.md) for a full example of every current HumanLang feature.

## Goal

HumanLang should be simple on the surface and powerful underneath:

- English syntax for beginners
- Python backend first
- Later backends for Go, Rust, C++, and Rux
- Support for speed, memory control, concurrency, and scientific computing
