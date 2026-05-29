import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from humanlang import read_source_file, translate


HEADER = translate("").removesuffix("\n")


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
print(_human_text("Hello ", name))
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

        self.assertEqual(translate(source), HEADER + '''number = _human_number_input("Enter a number: ")
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

        self.assertEqual(translate(source), HEADER + '''first_number = _human_number_input("enter the first number  ")

second_number = _human_number_input("enter the second number  ")

addition = first_number + second_number
print(addition)
''')

    def test_accepts_beginner_calculator_variants(self):
        source = '''say number "enter the first_number " and remember it as first_number

say number "enter the second_number " and remember it as the second_number

calculate first_number plus second_number as addition,
calculate first_number plus second_number
'''

        self.assertEqual(translate(source), HEADER + '''first_number = _human_number_input("enter the first_number  ")

second_number = _human_number_input("enter the second_number  ")

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
first_number = _human_number_input("First? ")
second_number = _human_number_input("Second? ")
print(_human_text("Hello ", user_name))
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

    def test_translates_real_app_building_blocks(self):
        source = '''to greet user with name:
    say "Hello " plus name
end

greet user with "Steven"

make map "name": "Steven", "age": 25 as user profile
say user profile's "name"

remember 20 as age
remember "active" as status
if age is at least 18 and status is "active":
    say "Access granted"

remember 2 as balance
while balance is greater than 0:
    say balance
    change balance to balance minus 1

remember "Apple,Orange" as text
calculate lowercase of text as lower text
calculate uppercase of text as upper text
calculate replace "Apple" with "Mango" in text as changed text
split text by "," as parts
calculate number of "123" as my value
calculate text of 456 as my string

try:
    read file "missing.txt" as data
if error:
    say "Could not find the file"
'''

        self.assertEqual(translate(source), HEADER + '''def greet_user(name):
    print(_human_text("Hello ", name))


greet_user("Steven")

user_profile = {"name": "Steven", "age": 25}
print(user_profile["name"])

age = 20
status = "active"
if age >= 18 and status == "active":
    print("Access granted")

balance = 2
while balance > 0:
    print(balance)
    balance = balance - 1

text = "Apple,Orange"
lower_text = text.lower()
upper_text = text.upper()
changed_text = text.replace("Apple", "Mango")
parts = text.split(",")
my_value = float("123")
my_string = str(456)

try:
    data = Path("missing.txt").read_text(encoding="utf-8")
except Exception as error:
    print("Could not find the file")
''')

    def test_translates_safety_and_real_world_features(self):
        source = '''remember 85 as score
remember yes as has permission
make list "apple", "banana" and "mango" as fruits
remember 1 as counter
say "Score: " plus score
say first item of fruits
say item 2 of fruits
remove "banana" from fruits
repeat while counter is less than 3:
    change counter to counter plus 1
if score is at least 90:
    say "A"
otherwise if score is at least 80:
    say "B"
otherwise:
    say "C"
if "apple" is in fruits and "mango" is in fruits:
    say "Fruit found"
if "banana" is not in fruits:
    say "No banana"
if "Error" contains "err" ignoring case:
    say "Has error"
wait 1 seconds
remember argument 1 as file name
remember command arguments as all arguments
get from "https://example.com" as response text
clear screen
stop program
exit program
'''

        self.assertEqual(translate(source), HEADER + '''score = 85
has_permission = True
fruits = ["apple", "banana", "mango"]
counter = 1
print(_human_text("Score: ", score))
print(fruits[0])
print(fruits[int(2) - 1])
fruits.remove("banana")
while counter < 3:
    counter = counter + 1
if score >= 90:
    print("A")
elif score >= 80:
    print("B")
else:
    print("C")
if "apple" in fruits and "mango" in fruits:
    print("Fruit found")
if "banana" not in fruits:
    print("No banana")
if str("err").lower() in str("Error").lower():
    print("Has error")
time.sleep(float(1))
file_name = sys.argv[int(1) + 2]
all_arguments = sys.argv[3:]
response_text = urllib.request.urlopen("https://example.com", timeout=30).read().decode("utf-8")
os.system("cls" if os.name == "nt" else "clear")
sys.exit(0)
sys.exit(0)
''')

    def test_translates_app_platform_starters(self):
        source = '''open window "Demo" size 400 by 300
add text "Hello GUI" to window
add button "Close" to window
show window

create web page "Home" as page
add heading "Welcome" to page
add paragraph "Hello web" to page
save web page page to file "index.html"

open database "app.db" as database
run sql "CREATE TABLE IF NOT EXISTS users(name TEXT)" on database
query sql "SELECT name FROM users" on database as rows

open game screen "Cube" size 500 by 400
draw cube at x 0 y 0 size 80
show game

create mobile app "Demo Mobile" as mobile app
add mobile screen "Home" to mobile app
save mobile app mobile app to folder "mobile_demo"
'''

        self.assertEqual(translate(source), HEADER + '''_human_open_window("Demo", 400, 300)
_human_add_text_to_window("Hello GUI")
_human_add_button_to_window("Close")
_human_show_window()

page = _human_web_page("Home")
page["body"].append("<h1>" + html.escape(str("Welcome")) + "</h1>")
page["body"].append("<p>" + html.escape(str("Hello web")) + "</p>")
_human_save_web_page(page, "index.html")

database = sqlite3.connect("app.db")
database.execute("""CREATE TABLE IF NOT EXISTS users(name TEXT)""")
database.commit()
rows = database.execute("""SELECT name FROM users""").fetchall()

_human_open_game_screen("Cube", 500, 400)
_human_draw_cube(0, 0, 80)
_human_show_game()

mobile_app = _human_mobile_app("Demo Mobile")
mobile_app["screens"].append("Home")
_human_save_mobile_app(mobile_app, "mobile_demo")
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
