import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from humanlang import read_source_file, translate


HEADER = "import datetime\nimport math\nimport random\nfrom pathlib import Path\n\n"


class TranslatorTests(unittest.TestCase):
    def test_translates_basic_program(self):
        source = '''ask "What is your name?" and remember it as name
remember 20 as age
say "Hello " plus name
if age is at least 18:
    say "You are an adult"
otherwise:
    say "You are not an adult"
'''

        self.assertEqual(translate(source), HEADER + '''name = input("What is your name? ")
age = 20
print("Hello " + name)
if age >= 18:
    print("You are an adult")
else:
    print("You are not an adult")
''')

    def test_translates_scientific_math(self):
        source = '''ask number "Enter a number:" and remember it as number
calculate the square root of number as root
calculate number to the power of 2 as squared
calculate the sine of radians of 90 as sine_value
say root
'''

        self.assertEqual(translate(source), HEADER + '''number = float(input("Enter a number: "))
root = math.sqrt(number)
squared = number ** 2
sine_value = math.sin(math.radians(90))
print(root)
''')

    def test_does_not_translate_inside_quoted_text(self):
        source = '''say "Pi is:"
say "2 to the power of 10:"
say pi
'''

        self.assertEqual(translate(source), HEADER + '''print("Pi is:")
print("2 to the power of 10:")
print(math.pi)
''')

    def test_accepts_english_variable_names_and_case_insensitive_commands(self):
        source = '''ASK NUMBER "enter the first number " AND remember it AS a first number

ask number "enter the second number " and remember it as a second number

calculate first number plus second number as addition
say addition
'''

        self.assertEqual(translate(source), HEADER + '''first_number = float(input("enter the first number  "))

second_number = float(input("enter the second number  "))

addition = first_number + second_number
print(addition)
''')

    def test_accepts_beginner_calculator_variants(self):
        source = '''say number "enter the first_number " and remember it as first_number

say number "enter the second_number " and remember it as the second_number

calculate first_number plus second_number as addition,
calculate first_number plus second_number
'''

        self.assertEqual(translate(source), HEADER + '''first_number = float(input("enter the first_number  "))

second_number = float(input("enter the second_number  "))

addition = first_number + second_number
print(addition)
print(first_number + second_number)
''')

    def test_translates_minimal_language_features(self):
        source = '''// comment
get "Your name?" and remember it as user name
get number "First?" and remember it as first number
get number "Second?" and remember it as second number
show "Hello " plus user name
calculate average of first number and second number as average value
calculate the maximum of first number and second number as biggest value
calculate the minimum of first number and second number as smallest value
calculate 10 percent of second number as percent value
calculate the factorial of 5 as factorial value
calculate the rounded value of 4.7 as rounded value
repeat 2 times:
    print average value
'''

        self.assertEqual(translate(source), HEADER + '''# comment
user_name = input("Your name? ")
first_number = float(input("First? "))
second_number = float(input("Second? "))
print("Hello " + user_name)
average_value = ((first_number + second_number) / 2)
biggest_value = max(first_number, second_number)
smallest_value = min(first_number, second_number)
percent_value = ((10) / 100 * (second_number))
factorial_value = math.factorial(5)
rounded_value = round(4.7)
for _ in range(int(2)):
    print(average_value)
''')

    def test_translates_lists_files_random_and_dates(self):
        source = '''make list "apples", "bananas" and "mangoes" as fruits
add "oranges" to fruits
for each fruit in fruits:
    say fruit
calculate length of fruits as fruit count
calculate random integer between 1 and 6 as dice roll
calculate random number between 1 and 2 as random value
remember current date as today
remember current time as now
write "hello" to file "sample.txt"
append " world" to file "sample.txt"
read file "sample.txt" as file text
'''

        self.assertEqual(translate(source), HEADER + '''fruits = ["apples", "bananas", "mangoes"]
fruits.append("oranges")
for fruit in fruits:
    print(fruit)
fruit_count = len(fruits)
dice_roll = random.randint(int(1), int(6))
random_value = random.uniform(1, 2)
today = datetime.date.today().isoformat()
now = datetime.datetime.now().strftime('%H:%M:%S')
Path("sample.txt").write_text(str("hello"), encoding="utf-8")
Path("sample.txt").open("a", encoding="utf-8").write(str(" world"))
file_text = Path("sample.txt").read_text(encoding="utf-8")
''')


class SourceFileTests(unittest.TestCase):
    def test_missing_source_file_has_friendly_error(self):
        with self.assertRaisesRegex(FileNotFoundError, "HumanLang could not find"):
            read_source_file(Path("missing.hl"))

    def test_source_file_must_use_hl_extension(self):
        with TemporaryDirectory() as directory:
            source = Path(directory) / "app.txt"
            source.write_text('say "Hello"', encoding="utf-8")

            with self.assertRaisesRegex(ValueError, ".hl extension"):
                read_source_file(source)


if __name__ == "__main__":
    unittest.main()
