from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


HUMAN_NAME = r"[A-Za-z_][A-Za-z0-9_]*(?:\s+[A-Za-z0-9_]+)*"
FUNCTION_NAME = r"[A-Za-z_][A-Za-z0-9_]*(?:\s+(?!with\b)[A-Za-z0-9_]+)*"
VALUE_PATTERN = r'"[^"]*"|[^,\s]+(?:\s+[^,\s]+)*?'
ASK_RE = re.compile(rf'^(?:ask|get)\s+"(?P<question>.*)"\s+and\s+remember\s+it\s+as\s+(?P<name>{HUMAN_NAME})$', re.IGNORECASE)
ASK_NUMBER_RE = re.compile(rf'^(?:ask|get|say)\s+number\s+"(?P<question>.*)"\s+and\s+remember\s+it\s+as\s+(?P<name>{HUMAN_NAME})$', re.IGNORECASE)
REMEMBER_RE = re.compile(rf"^remember\s+(?P<value>.+)\s+as\s+(?P<name>{HUMAN_NAME})$", re.IGNORECASE)
CALCULATE_RE = re.compile(rf"^calculate\s+(?P<value>.+?)\s+as\s+(?P<name>{HUMAN_NAME})$", re.IGNORECASE)
CALCULATE_PRINT_RE = re.compile(r"^calculate\s+(?P<value>.+)$", re.IGNORECASE)
CHANGE_RE = re.compile(rf"^(?:change|set)\s+(?P<name>{HUMAN_NAME})\s+to\s+(?P<value>.+)$", re.IGNORECASE)
REPEAT_RE = re.compile(r"^repeat\s+(?P<count>.+)\s+times:$", re.IGNORECASE)
REPEAT_WHILE_RE = re.compile(r"^repeat\s+while\s+(?P<condition>.+):$", re.IGNORECASE)
LIST_RE = re.compile(rf"^(?:make|create|remember)\s+list\s+(?P<items>.+)\s+as\s+(?P<name>{HUMAN_NAME})$", re.IGNORECASE)
ADD_TO_LIST_RE = re.compile(r"^add\s+(?P<value>.+)\s+to\s+(?P<name>.+)$", re.IGNORECASE)
REMOVE_FROM_LIST_RE = re.compile(r"^remove\s+(?P<value>.+)\s+from\s+(?P<name>.+)$", re.IGNORECASE)
FOR_EACH_RE = re.compile(rf"^for\s+each\s+(?P<item>{HUMAN_NAME})\s+in\s+(?P<items>.+):$", re.IGNORECASE)
READ_FILE_RE = re.compile(rf'^read\s+file\s+"(?P<path>.+)"\s+as\s+(?P<name>{HUMAN_NAME})$', re.IGNORECASE)
WRITE_FILE_RE = re.compile(r'^write\s+(?P<value>.+)\s+to\s+file\s+"(?P<path>.+)"$', re.IGNORECASE)
APPEND_FILE_RE = re.compile(r'^append\s+(?P<value>.+)\s+to\s+file\s+"(?P<path>.+)"$', re.IGNORECASE)
WEB_GET_RE = re.compile(rf'^get\s+from\s+"(?P<url>.+)"\s+as\s+(?P<name>{HUMAN_NAME})$', re.IGNORECASE)
FUNCTION_DEF_RE = re.compile(rf"^to\s+(?P<name>{FUNCTION_NAME})(?:\s+with\s+(?P<params>.+))?:$", re.IGNORECASE)
FUNCTION_CALL_RE = re.compile(rf"^(?P<name>{FUNCTION_NAME})(?:\s+with\s+(?P<args>.+))?$", re.IGNORECASE)
MAP_RE = re.compile(rf"^(?:make|create|remember)\s+map\s+(?P<items>.+)\s+as\s+(?P<name>{HUMAN_NAME})$", re.IGNORECASE)
MAP_GET_RE = re.compile(r"^(?P<name>.+?)'s\s+\"(?P<key>.+)\"$", re.IGNORECASE)
SPLIT_RE = re.compile(rf'^split\s+(?P<value>.+)\s+by\s+"(?P<separator>.*)"\s+as\s+(?P<name>{HUMAN_NAME})$', re.IGNORECASE)
REPLACE_RE = re.compile(r'^replace\s+"(?P<old>.*)"\s+with\s+"(?P<new>.*)"\s+in\s+(?P<value>.+)$', re.IGNORECASE)
USE_RE = re.compile(r'^use\s+"(?P<path>.+\.hl)"$', re.IGNORECASE)
IF_RE = re.compile(
    r"^if\s+(?P<left>.+?)\s+(?P<operator>is at least|is at most|is greater than|is less than|is not|is|equals|does not equal)\s+(?P<right>.+):$",
    re.IGNORECASE,
)
WHILE_RE = re.compile(
    r"^while\s+(?P<left>.+?)\s+(?P<operator>is at least|is at most|is greater than|is less than|is not|is|equals|does not equal)\s+(?P<right>.+):$",
    re.IGNORECASE,
)
WAIT_RE = re.compile(r"^wait\s+(?P<seconds>.+)\s+seconds?$", re.IGNORECASE)
OPEN_WINDOW_RE = re.compile(r'^open\s+window\s+"(?P<title>.+)"\s+size\s+(?P<width>.+?)\s+by\s+(?P<height>.+)$', re.IGNORECASE)
ADD_TEXT_WINDOW_RE = re.compile(r'^add\s+text\s+(?P<value>.+)\s+to\s+window$', re.IGNORECASE)
ADD_BUTTON_WINDOW_RE = re.compile(r'^add\s+button\s+"(?P<label>.+)"\s+to\s+window$', re.IGNORECASE)
WEB_PAGE_RE = re.compile(rf'^create\s+web\s+page\s+"(?P<title>.+)"\s+as\s+(?P<name>{HUMAN_NAME})$', re.IGNORECASE)
WEB_HEADING_RE = re.compile(r'^add\s+heading\s+(?P<value>.+)\s+to\s+(?P<name>.+)$', re.IGNORECASE)
WEB_PARAGRAPH_RE = re.compile(r'^add\s+paragraph\s+(?P<value>.+)\s+to\s+(?P<name>.+)$', re.IGNORECASE)
SAVE_WEB_PAGE_RE = re.compile(r'^save\s+web\s+page\s+(?P<name>.+)\s+to\s+file\s+"(?P<path>.+)"$', re.IGNORECASE)
OPEN_DATABASE_RE = re.compile(rf'^open\s+database\s+"(?P<path>.+)"\s+as\s+(?P<name>{HUMAN_NAME})$', re.IGNORECASE)
RUN_SQL_RE = re.compile(r'^run\s+sql\s+"(?P<sql>.+)"\s+on\s+(?P<name>.+)$', re.IGNORECASE)
QUERY_SQL_RE = re.compile(rf'^query\s+sql\s+"(?P<sql>.+)"\s+on\s+(?P<database>.+)\s+as\s+(?P<name>{HUMAN_NAME})$', re.IGNORECASE)
OPEN_GAME_RE = re.compile(r'^open\s+game\s+screen\s+"(?P<title>.+)"\s+size\s+(?P<width>.+?)\s+by\s+(?P<height>.+)$', re.IGNORECASE)
DRAW_CUBE_RE = re.compile(r'^draw\s+cube\s+at\s+x\s+(?P<x>.+?)\s+y\s+(?P<y>.+?)\s+size\s+(?P<size>.+)$', re.IGNORECASE)
MOBILE_APP_RE = re.compile(rf'^create\s+mobile\s+app\s+"(?P<title>.+)"\s+as\s+(?P<name>{HUMAN_NAME})$', re.IGNORECASE)
MOBILE_SCREEN_RE = re.compile(r'^add\s+mobile\s+screen\s+"(?P<title>.+)"\s+to\s+(?P<name>.+)$', re.IGNORECASE)
SAVE_MOBILE_RE = re.compile(r'^save\s+mobile\s+app\s+(?P<name>.+)\s+to\s+folder\s+"(?P<path>.+)"$', re.IGNORECASE)


MATH_FUNCTIONS = {
    "the square root of": "math.sqrt",
    "square root of": "math.sqrt",
    "the sine of": "math.sin",
    "sine of": "math.sin",
    "the cosine of": "math.cos",
    "cosine of": "math.cos",
    "the tangent of": "math.tan",
    "tangent of": "math.tan",
    "the natural log of": "math.log",
    "natural log of": "math.log",
    "the log of": "math.log10",
    "log of": "math.log10",
    "the absolute value of": "abs",
    "absolute value of": "abs",
    "the floor of": "math.floor",
    "floor of": "math.floor",
    "the ceiling of": "math.ceil",
    "ceiling of": "math.ceil",
    "the factorial of": "math.factorial",
    "factorial of": "math.factorial",
    "the rounded value of": "round",
    "rounded value of": "round",
}


def normalize_name(name: str) -> str:
    cleaned = re.sub(r"\s+", " ", name.strip().lower())
    cleaned = re.sub(r"^(a|an|the)\s+", "", cleaned)
    cleaned = re.sub(r"[^a-z0-9_]+", "_", cleaned)
    cleaned = cleaned.strip("_")

    if not cleaned:
        raise ValueError(f"Invalid HumanLang name: {name}")

    if cleaned[0].isdigit():
        cleaned = f"value_{cleaned}"

    return cleaned


def remember_name(variables: dict[str, str], name: str) -> str:
    normalized = normalize_name(name)
    keys = {
        re.sub(r"\s+", " ", name.strip().lower()),
        re.sub(r"^(a|an|the)\s+", "", re.sub(r"\s+", " ", name.strip().lower())),
        normalized.replace("_", " "),
        normalized,
    }

    for key in keys:
        variables[key] = normalized

    return normalized


def split_human_args(text: str) -> list[str]:
    if not text:
        return []

    parts = []
    current = []
    in_quote = False
    index = 0

    while index < len(text):
        character = text[index]

        if character == '"' and (index == 0 or text[index - 1] != "\\"):
            in_quote = not in_quote
            current.append(character)
        elif not in_quote and character == ",":
            parts.append("".join(current).strip())
            current = []
        elif not in_quote and text[index : index + 5].lower() == " and ":
            parts.append("".join(current).strip())
            current = []
            index += 4
        else:
            current.append(character)

        index += 1

    if current:
        parts.append("".join(current).strip())

    return [part for part in parts if part]


def split_quoted_text(expression: str) -> list[tuple[str, bool]]:
    parts = []
    current = []
    in_quote = False
    index = 0

    while index < len(expression):
        character = expression[index]
        current.append(character)

        if character == '"' and (index == 0 or expression[index - 1] != "\\"):
            if in_quote:
                parts.append(("".join(current), True))
                current = []
                in_quote = False
            else:
                if len(current) > 1:
                    parts.append(("".join(current[:-1]), False))
                    current = ['"']
                in_quote = True

        index += 1

    if current:
        parts.append(("".join(current), in_quote))

    return parts


def replace_known_names(expression: str, variables: dict[str, str]) -> str:
    for human_name, python_name in sorted(variables.items(), key=lambda item: len(item[0]), reverse=True):
        pattern = rf"\b{re.escape(human_name)}\b"
        expression = re.sub(pattern, python_name, expression, flags=re.IGNORECASE)
    return expression


def translate_map_access(expression: str, variables: dict[str, str]) -> str:
    match = MAP_GET_RE.match(expression.strip())
    if not match:
        return expression

    name = translate_expression(match.group("name"), variables)
    key = match.group("key")
    return f'{name}["{key}"]'


def translate_code_words(expression: str, variables: dict[str, str]) -> str:
    expression = translate_map_access(expression, variables)
    expression = replace_known_names(expression, variables)
    expression = re.sub(
        r"\b(.+?)\s+percent\s+of\s+(.+)\b",
        lambda match: f"(({translate_expression(match.group(1), variables)}) / 100 * ({translate_expression(match.group(2), variables)}))",
        expression,
        flags=re.IGNORECASE,
    )
    expression = re.sub(r"\bpi\b", "math.pi", expression, flags=re.IGNORECASE)
    expression = re.sub(r"\be\b", "math.e", expression, flags=re.IGNORECASE)
    expression = re.sub(r"\bto the power of\b", "**", expression, flags=re.IGNORECASE)
    expression = re.sub(r"\bplus\b", "+", expression, flags=re.IGNORECASE)
    expression = re.sub(r"\bminus\b", "-", expression, flags=re.IGNORECASE)
    expression = re.sub(r"\btimes\b", "*", expression, flags=re.IGNORECASE)
    expression = re.sub(r"\bmultiplied by\b", "*", expression, flags=re.IGNORECASE)
    expression = re.sub(r"\bdivided by\b", "/", expression, flags=re.IGNORECASE)
    expression = re.sub(r"\bmodulo\b", "%", expression, flags=re.IGNORECASE)
    expression = re.sub(r"\band\b", "and", expression, flags=re.IGNORECASE)
    expression = re.sub(r"\bor\b", "or", expression, flags=re.IGNORECASE)
    return expression


def split_plus_expression(expression: str) -> list[str]:
    parts = []
    current = []
    in_quote = False
    index = 0

    while index < len(expression):
        character = expression[index]

        if character == '"' and (index == 0 or expression[index - 1] != "\\"):
            in_quote = not in_quote
            current.append(character)
        elif not in_quote and expression[index : index + 6].lower() == " plus ":
            parts.append("".join(current).strip())
            current = []
            index += 5
        else:
            current.append(character)

        index += 1

    if current:
        parts.append("".join(current).strip())

    return parts


def translate_say_expression(expression: str, variables: dict[str, str]) -> str:
    parts = split_plus_expression(expression)
    if len(parts) <= 1:
        return translate_expression(expression, variables)

    return "_human_text(" + ", ".join(translate_expression(part, variables) for part in parts) + ")"


def translate_expression(expression: str, variables: dict[str, str]) -> str:
    expression = expression.strip().rstrip(",")
    lowered = expression.lower()

    map_access_match = MAP_GET_RE.match(expression)
    if map_access_match:
        return translate_map_access(expression, variables)

    if lowered == "current date":
        return "datetime.date.today().isoformat()"

    if lowered == "current time":
        return "datetime.datetime.now().strftime('%H:%M:%S')"

    if lowered == "current datetime":
        return "datetime.datetime.now().isoformat(timespec='seconds')"

    if lowered == "true":
        return "True"

    if lowered == "false":
        return "False"

    if lowered == "yes":
        return "True"

    if lowered == "no":
        return "False"

    if lowered == "nothing":
        return "None"

    if lowered == "command arguments":
        return "sys.argv[3:]"

    argument_match = re.match(r"^argument\s+(.+)$", expression, flags=re.IGNORECASE)
    if argument_match:
        number = translate_expression(argument_match.group(1), variables)
        return f"sys.argv[int({number}) + 2]"

    first_item_match = re.match(r"^first\s+item\s+of\s+(.+)$", expression, flags=re.IGNORECASE)
    if first_item_match:
        return f"{translate_expression(first_item_match.group(1), variables)}[0]"

    item_match = re.match(r"^item\s+(.+?)\s+of\s+(.+)$", expression, flags=re.IGNORECASE)
    if item_match:
        number = translate_expression(item_match.group(1), variables)
        items = translate_expression(item_match.group(2), variables)
        return f"{items}[int({number}) - 1]"

    if lowered.startswith("number of "):
        value = expression[len("number of ") :].strip()
        return f"float({translate_expression(value, variables)})"

    if lowered.startswith("integer of "):
        value = expression[len("integer of ") :].strip()
        return f"int({translate_expression(value, variables)})"

    if lowered.startswith("text of "):
        value = expression[len("text of ") :].strip()
        return f"str({translate_expression(value, variables)})"

    if lowered.startswith("lowercase of "):
        value = expression[len("lowercase of ") :].strip()
        return f"{translate_expression(value, variables)}.lower()"

    if lowered.startswith("uppercase of "):
        value = expression[len("uppercase of ") :].strip()
        return f"{translate_expression(value, variables)}.upper()"

    replace_match = REPLACE_RE.match(expression)
    if replace_match:
        value = translate_expression(replace_match.group("value"), variables)
        return f'{value}.replace("{replace_match.group("old")}", "{replace_match.group("new")}")'

    if lowered.startswith("length of "):
        value = expression[len("length of ") :].strip()
        return f"len({translate_expression(value, variables)})"

    random_integer = re.match(r"^random\s+integer\s+between\s+(.+?)\s+and\s+(.+)$", expression, flags=re.IGNORECASE)
    if random_integer:
        start = translate_expression(random_integer.group(1), variables)
        end = translate_expression(random_integer.group(2), variables)
        return f"random.randint(int({start}), int({end}))"

    random_number = re.match(r"^random\s+number\s+between\s+(.+?)\s+and\s+(.+)$", expression, flags=re.IGNORECASE)
    if random_number:
        start = translate_expression(random_number.group(1), variables)
        end = translate_expression(random_number.group(2), variables)
        return f"random.uniform({start}, {end})"

    if lowered.startswith("average of "):
        values = [value.strip() for value in re.split(r"\s+and\s+", expression[len("average of ") :], flags=re.IGNORECASE)]
        translated_values = [translate_expression(value, variables) for value in values if value]
        return f"(({ ' + '.join(translated_values) }) / {len(translated_values)})"

    if lowered.startswith("the maximum of ") or lowered.startswith("maximum of "):
        prefix = "the maximum of " if lowered.startswith("the maximum of ") else "maximum of "
        values = [value.strip() for value in re.split(r"\s+and\s+", expression[len(prefix) :], flags=re.IGNORECASE)]
        return f"max({', '.join(translate_expression(value, variables) for value in values if value)})"

    if lowered.startswith("the minimum of ") or lowered.startswith("minimum of "):
        prefix = "the minimum of " if lowered.startswith("the minimum of ") else "minimum of "
        values = [value.strip() for value in re.split(r"\s+and\s+", expression[len(prefix) :], flags=re.IGNORECASE)]
        return f"min({', '.join(translate_expression(value, variables) for value in values if value)})"

    for phrase, function_name in MATH_FUNCTIONS.items():
        if lowered.startswith(f"{phrase} "):
            value = expression[len(phrase) :].strip()
            return f"{function_name}({translate_expression(value, variables)})"

    if lowered.startswith("degrees of "):
        value = expression[len("degrees of ") :].strip()
        return f"math.degrees({translate_expression(value, variables)})"

    if lowered.startswith("radians of "):
        value = expression[len("radians of ") :].strip()
        return f"math.radians({translate_expression(value, variables)})"

    return "".join(
        part if is_quoted else translate_code_words(part, variables)
        for part, is_quoted in split_quoted_text(expression)
    )


def translate_condition(left: str, operator: str, right: str, variables: dict[str, str]) -> str:
    operators = {
        "is at least": ">=",
        "is at most": "<=",
        "is greater than": ">",
        "is less than": "<",
        "is not": "!=",
        "is": "==",
        "equals": "==",
        "does not equal": "!=",
    }
    return f"{translate_expression(left, variables)} {operators[operator.lower()]} {translate_expression(right, variables)}"


def translate_compound_condition(condition: str, variables: dict[str, str]) -> str:
    pieces = re.split(r"\s+(and|or)\s+", condition, flags=re.IGNORECASE)
    translated = []

    for piece in pieces:
        lowered = piece.lower()
        if lowered in {"and", "or"}:
            translated.append(lowered)
            continue

        contains_ignoring_case_match = re.match(r"^(?P<left>.+?)\s+contains\s+(?P<right>.+?)\s+ignoring\s+case$", piece, flags=re.IGNORECASE)
        if contains_ignoring_case_match:
            translated.append(
                f"str({translate_expression(contains_ignoring_case_match.group('right'), variables)}).lower() in str({translate_expression(contains_ignoring_case_match.group('left'), variables)}).lower()"
            )
            continue

        contains_match = re.match(r"^(?P<left>.+?)\s+contains\s+(?P<right>.+)$", piece, flags=re.IGNORECASE)
        if contains_match:
            translated.append(
                f"{translate_expression(contains_match.group('right'), variables)} in {translate_expression(contains_match.group('left'), variables)}"
            )
            continue

        not_in_match = re.match(r"^(?P<left>.+?)\s+is\s+not\s+in\s+(?P<right>.+)$", piece, flags=re.IGNORECASE)
        if not_in_match:
            translated.append(
                f"{translate_expression(not_in_match.group('left'), variables)} not in {translate_expression(not_in_match.group('right'), variables)}"
            )
            continue

        in_match = re.match(r"^(?P<left>.+?)\s+is\s+in\s+(?P<right>.+)$", piece, flags=re.IGNORECASE)
        if in_match:
            translated.append(
                f"{translate_expression(in_match.group('left'), variables)} in {translate_expression(in_match.group('right'), variables)}"
            )
            continue

        ignoring_case_match = re.match(r"^(?P<left>.+?)\s+(equals|is)\s+(?P<right>.+?)\s+ignoring\s+case$", piece, flags=re.IGNORECASE)
        if ignoring_case_match:
            translated.append(
                f"str({translate_expression(ignoring_case_match.group('left'), variables)}).lower() == str({translate_expression(ignoring_case_match.group('right'), variables)}).lower()"
            )
            continue

        match = re.match(
            r"^(?P<left>.+?)\s+(?P<operator>is at least|is at most|is greater than|is less than|is not|is|equals|does not equal)\s+(?P<right>.+)$",
            piece,
            flags=re.IGNORECASE,
        )
        if not match:
            translated.append(translate_expression(piece, variables))
            continue

        translated.append(
            translate_condition(
                match.group("left"),
                match.group("operator"),
                match.group("right"),
                variables,
            )
        )

    return " ".join(translated)


def translate_line(line: str, line_number: int, variables: dict[str, str]) -> str:
    raw_stripped = line.strip()
    should_print_assignment = raw_stripped.endswith(",")
    stripped = raw_stripped.rstrip(",")
    indent = line[: len(line) - len(line.lstrip(" "))]
    lowered = stripped.lower()

    if not stripped:
        return ""

    if stripped.startswith("#"):
        return stripped

    if stripped.startswith("//"):
        return f"{indent}#{stripped[2:]}"

    if lowered == "end":
        return ""

    if lowered == "try:":
        return f"{indent}try:"

    if lowered == "if error:":
        return f"{indent}except Exception as error:"

    if lowered.startswith("otherwise if ") and lowered.endswith(":"):
        condition = stripped[len("otherwise if ") : -1].strip()
        return f"{indent}elif {translate_compound_condition(condition, variables)}:"

    use_match = USE_RE.match(stripped)
    if use_match:
        return ""

    function_def_match = FUNCTION_DEF_RE.match(stripped)
    if function_def_match:
        name = remember_name(variables, function_def_match.group("name"))
        params = [
            remember_name(variables, parameter)
            for parameter in split_human_args(function_def_match.group("params") or "")
        ]
        return f"{indent}def {name}({', '.join(params)}):"

    ask_number_match = ASK_NUMBER_RE.match(stripped)
    if ask_number_match:
        question = ask_number_match.group("question")
        name = remember_name(variables, ask_number_match.group("name"))
        return f'{indent}{name} = _human_number_input("{question} ")'

    ask_match = ASK_RE.match(stripped)
    if ask_match:
        question = ask_match.group("question")
        name = remember_name(variables, ask_match.group("name"))
        return f'{indent}{name} = input("{question} ")'

    open_window_match = OPEN_WINDOW_RE.match(stripped)
    if open_window_match:
        title = open_window_match.group("title")
        width = translate_expression(open_window_match.group("width"), variables)
        height = translate_expression(open_window_match.group("height"), variables)
        return f'{indent}_human_open_window("{title}", {width}, {height})'

    add_text_window_match = ADD_TEXT_WINDOW_RE.match(stripped)
    if add_text_window_match:
        value = translate_expression(add_text_window_match.group("value"), variables)
        return f"{indent}_human_add_text_to_window({value})"

    add_button_window_match = ADD_BUTTON_WINDOW_RE.match(stripped)
    if add_button_window_match:
        label = add_button_window_match.group("label")
        return f'{indent}_human_add_button_to_window("{label}")'

    if lowered == "show window":
        return f"{indent}_human_show_window()"

    web_page_match = WEB_PAGE_RE.match(stripped)
    if web_page_match:
        name = remember_name(variables, web_page_match.group("name"))
        title = web_page_match.group("title")
        return f'{indent}{name} = _human_web_page("{title}")'

    web_heading_match = WEB_HEADING_RE.match(stripped)
    if web_heading_match:
        name = translate_expression(web_heading_match.group("name"), variables)
        value = translate_expression(web_heading_match.group("value"), variables)
        return f'{indent}{name}["body"].append("<h1>" + html.escape(str({value})) + "</h1>")'

    web_paragraph_match = WEB_PARAGRAPH_RE.match(stripped)
    if web_paragraph_match:
        name = translate_expression(web_paragraph_match.group("name"), variables)
        value = translate_expression(web_paragraph_match.group("value"), variables)
        return f'{indent}{name}["body"].append("<p>" + html.escape(str({value})) + "</p>")'

    save_web_page_match = SAVE_WEB_PAGE_RE.match(stripped)
    if save_web_page_match:
        name = translate_expression(save_web_page_match.group("name"), variables)
        path = save_web_page_match.group("path")
        return f'{indent}_human_save_web_page({name}, "{path}")'

    open_database_match = OPEN_DATABASE_RE.match(stripped)
    if open_database_match:
        name = remember_name(variables, open_database_match.group("name"))
        path = open_database_match.group("path")
        return f'{indent}{name} = sqlite3.connect("{path}")'

    run_sql_match = RUN_SQL_RE.match(stripped)
    if run_sql_match:
        name = translate_expression(run_sql_match.group("name"), variables)
        sql = run_sql_match.group("sql")
        return f'{indent}{name}.execute("""{sql}""")\n{indent}{name}.commit()'

    query_sql_match = QUERY_SQL_RE.match(stripped)
    if query_sql_match:
        database = translate_expression(query_sql_match.group("database"), variables)
        name = remember_name(variables, query_sql_match.group("name"))
        sql = query_sql_match.group("sql")
        return f'{indent}{name} = {database}.execute("""{sql}""").fetchall()'

    open_game_match = OPEN_GAME_RE.match(stripped)
    if open_game_match:
        title = open_game_match.group("title")
        width = translate_expression(open_game_match.group("width"), variables)
        height = translate_expression(open_game_match.group("height"), variables)
        return f'{indent}_human_open_game_screen("{title}", {width}, {height})'

    draw_cube_match = DRAW_CUBE_RE.match(stripped)
    if draw_cube_match:
        x = translate_expression(draw_cube_match.group("x"), variables)
        y = translate_expression(draw_cube_match.group("y"), variables)
        size = translate_expression(draw_cube_match.group("size"), variables)
        return f"{indent}_human_draw_cube({x}, {y}, {size})"

    if lowered == "show game":
        return f"{indent}_human_show_game()"

    mobile_app_match = MOBILE_APP_RE.match(stripped)
    if mobile_app_match:
        name = remember_name(variables, mobile_app_match.group("name"))
        title = mobile_app_match.group("title")
        return f'{indent}{name} = _human_mobile_app("{title}")'

    mobile_screen_match = MOBILE_SCREEN_RE.match(stripped)
    if mobile_screen_match:
        name = translate_expression(mobile_screen_match.group("name"), variables)
        title = mobile_screen_match.group("title")
        return f'{indent}{name}["screens"].append("{title}")'

    save_mobile_match = SAVE_MOBILE_RE.match(stripped)
    if save_mobile_match:
        name = translate_expression(save_mobile_match.group("name"), variables)
        path = save_mobile_match.group("path")
        return f'{indent}_human_save_mobile_app({name}, "{path}")'

    list_match = LIST_RE.match(stripped)
    if list_match:
        items = [
            translate_expression(item.strip(), variables)
            for item in re.split(r"\s*,\s*|\s+and\s+", list_match.group("items"), flags=re.IGNORECASE)
            if item.strip()
        ]
        name = remember_name(variables, list_match.group("name"))
        return f"{indent}{name} = [{', '.join(items)}]"

    map_match = MAP_RE.match(stripped)
    if map_match:
        entries = []
        for item in split_human_args(map_match.group("items")):
            if ":" not in item:
                raise SyntaxError(f"Line {line_number}: map items must look like \"key\": value")
            key, value = item.split(":", 1)
            entries.append(f"{key.strip()}: {translate_expression(value.strip(), variables)}")

        name = remember_name(variables, map_match.group("name"))
        return f"{indent}{name} = {{{', '.join(entries)}}}"

    add_to_list_match = ADD_TO_LIST_RE.match(stripped)
    if add_to_list_match:
        value = translate_expression(add_to_list_match.group("value"), variables)
        name = translate_expression(add_to_list_match.group("name"), variables)
        return f"{indent}{name}.append({value})"

    remove_from_list_match = REMOVE_FROM_LIST_RE.match(stripped)
    if remove_from_list_match:
        value = translate_expression(remove_from_list_match.group("value"), variables)
        name = translate_expression(remove_from_list_match.group("name"), variables)
        return f"{indent}{name}.remove({value})"

    read_file_match = READ_FILE_RE.match(stripped)
    if read_file_match:
        name = remember_name(variables, read_file_match.group("name"))
        path = read_file_match.group("path")
        return f'{indent}{name} = Path("{path}").read_text(encoding="utf-8")'

    write_file_match = WRITE_FILE_RE.match(stripped)
    if write_file_match:
        value = translate_expression(write_file_match.group("value"), variables)
        path = write_file_match.group("path")
        return f'{indent}Path("{path}").write_text(str({value}), encoding="utf-8")'

    append_file_match = APPEND_FILE_RE.match(stripped)
    if append_file_match:
        value = translate_expression(append_file_match.group("value"), variables)
        path = append_file_match.group("path")
        return f'{indent}Path("{path}").open("a", encoding="utf-8").write(str({value}))'

    web_get_match = WEB_GET_RE.match(stripped)
    if web_get_match:
        name = remember_name(variables, web_get_match.group("name"))
        url = web_get_match.group("url")
        return f'{indent}{name} = urllib.request.urlopen("{url}", timeout=30).read().decode("utf-8")'

    split_match = SPLIT_RE.match(stripped)
    if split_match:
        value = translate_expression(split_match.group("value"), variables)
        name = remember_name(variables, split_match.group("name"))
        separator = split_match.group("separator")
        return f'{indent}{name} = {value}.split("{separator}")'

    if lowered.startswith("say ") or lowered.startswith("show ") or lowered.startswith("print "):
        value = re.sub(r"^(say|show|print)\s+", "", stripped, count=1, flags=re.IGNORECASE)
        value = translate_say_expression(value, variables)
        return f"{indent}print({value})"

    remember_match = REMEMBER_RE.match(stripped)
    if remember_match:
        value = translate_expression(remember_match.group("value"), variables)
        name = remember_name(variables, remember_match.group("name"))
        return f"{indent}{name} = {value}"

    calculate_match = CALCULATE_RE.match(stripped)
    if calculate_match:
        value = translate_expression(calculate_match.group("value"), variables)
        name = remember_name(variables, calculate_match.group("name"))
        if should_print_assignment:
            return f"{indent}{name} = {value}\n{indent}print({name})"
        return f"{indent}{name} = {value}"

    calculate_print_match = CALCULATE_PRINT_RE.match(stripped)
    if calculate_print_match:
        value = translate_expression(calculate_print_match.group("value"), variables)
        return f"{indent}print({value})"

    change_match = CHANGE_RE.match(stripped)
    if change_match:
        value = translate_expression(change_match.group("value"), variables)
        name = remember_name(variables, change_match.group("name"))
        return f"{indent}{name} = {value}"

    has_compound_logic = bool(
        re.search(r"\s+(and|or)\s+", stripped, flags=re.IGNORECASE)
        or re.search(r"\s+contains\s+", stripped, flags=re.IGNORECASE)
        or re.search(r"\s+is\s+(not\s+)?in\s+", stripped, flags=re.IGNORECASE)
        or re.search(r"\s+ignoring\s+case", stripped, flags=re.IGNORECASE)
    )

    if_match = IF_RE.match(stripped)
    if if_match and not has_compound_logic:
        condition = translate_condition(
            if_match.group("left"),
            if_match.group("operator"),
            if_match.group("right"),
            variables,
        )
        return f"{indent}if {condition}:"

    if lowered.startswith("if ") and lowered.endswith(":"):
        condition = stripped[3:-1].strip()
        return f"{indent}if {translate_compound_condition(condition, variables)}:"

    if lowered == "otherwise:":
        return f"{indent}else:"

    repeat_while_match = REPEAT_WHILE_RE.match(stripped)
    if repeat_while_match:
        condition = repeat_while_match.group("condition").strip()
        return f"{indent}while {translate_compound_condition(condition, variables)}:"

    while_match = WHILE_RE.match(stripped)
    if while_match and not has_compound_logic:
        condition = translate_condition(
            while_match.group("left"),
            while_match.group("operator"),
            while_match.group("right"),
            variables,
        )
        return f"{indent}while {condition}:"

    if lowered.startswith("while ") and lowered.endswith(":"):
        condition = stripped[6:-1].strip()
        return f"{indent}while {translate_compound_condition(condition, variables)}:"

    repeat_match = REPEAT_RE.match(stripped)
    if repeat_match:
        count = translate_expression(repeat_match.group("count"), variables)
        return f"{indent}for _ in range(int({count})):"

    for_each_match = FOR_EACH_RE.match(stripped)
    if for_each_match:
        item = remember_name(variables, for_each_match.group("item"))
        items = translate_expression(for_each_match.group("items"), variables)
        return f"{indent}for {item} in {items}:"

    wait_match = WAIT_RE.match(stripped)
    if wait_match:
        seconds = translate_expression(wait_match.group("seconds"), variables)
        return f"{indent}time.sleep(float({seconds}))"

    if lowered in {"exit program", "stop everything", "stop program"}:
        return f"{indent}sys.exit(0)"

    if lowered == "clear screen":
        return f'{indent}os.system("cls" if os.name == "nt" else "clear")'

    if lowered == "stop":
        return f"{indent}break"

    if lowered == "continue":
        return f"{indent}continue"

    function_call_match = FUNCTION_CALL_RE.match(stripped)
    if function_call_match:
        name = normalize_name(function_call_match.group("name"))
        args = [
            translate_expression(argument, variables)
            for argument in split_human_args(function_call_match.group("args") or "")
        ]
        return f"{indent}{name}({', '.join(args)})"

    raise SyntaxError(f"Line {line_number}: HumanLang does not understand: {stripped}")


def expand_uses(source: str, source_path: Path | None = None, seen: set[Path] | None = None) -> str:
    seen = seen or set()
    expanded_lines = []
    base_dir = source_path.parent if source_path else Path.cwd()

    for line in source.splitlines():
        match = USE_RE.match(line.strip())
        if not match:
            expanded_lines.append(line)
            continue

        import_path = (base_dir / match.group("path")).resolve()
        if import_path in seen:
            continue

        seen.add(import_path)
        imported_source = read_source_file(import_path)
        expanded_lines.append(expand_uses(imported_source, import_path, seen))

    return "\n".join(expanded_lines)


def translate(source: str, source_path: Path | None = None) -> str:
    source = expand_uses(source, source_path)
    lines = source.splitlines()
    variables: dict[str, str] = {}
    python_lines = [translate_line(line, index + 1, variables) for index, line in enumerate(lines)]
    header = '''import datetime
import html
import json
import math
import random
import os
import sqlite3
import sys
import time
import urllib.request
from pathlib import Path


def _human_text(*values):
    return "".join(str(value) for value in values)


def _human_number_input(prompt):
    while True:
        value = input(prompt)
        try:
            return float(value)
        except ValueError:
            print("Please enter a valid number.")

_human_window = None
_human_game_screen = None
_human_turtle = None


def _human_open_window(title, width, height):
    global _human_window
    import tkinter as tk
    _human_window = tk.Tk()
    _human_window.title(title)
    _human_window.geometry(f"{int(width)}x{int(height)}")


def _human_add_text_to_window(value):
    import tkinter as tk
    if _human_window is None:
        raise RuntimeError("Open a window before adding text.")
    tk.Label(_human_window, text=str(value), padx=12, pady=8).pack()


def _human_add_button_to_window(label):
    import tkinter as tk
    if _human_window is None:
        raise RuntimeError("Open a window before adding a button.")
    tk.Button(_human_window, text=label, command=_human_window.destroy, padx=12, pady=8).pack()


def _human_show_window():
    if _human_window is None:
        raise RuntimeError("Open a window before showing it.")
    _human_window.mainloop()


def _human_web_page(title):
    return {"title": title, "body": []}


def _human_save_web_page(page, path):
    title = html.escape(str(page["title"]))
    body = "\\n".join(page["body"])
    document = f"<!doctype html>\\n<html>\\n<head><meta charset=\\"utf-8\\"><title>{title}</title></head>\\n<body>\\n{body}\\n</body>\\n</html>\\n"
    Path(path).write_text(document, encoding="utf-8")


def _human_open_game_screen(title, width, height):
    global _human_game_screen, _human_turtle
    import turtle
    _human_game_screen = turtle.Screen()
    _human_game_screen.title(title)
    _human_game_screen.setup(int(width), int(height))
    _human_turtle = turtle.Turtle()
    _human_turtle.speed(0)


def _human_draw_cube(x, y, size):
    if _human_turtle is None:
        raise RuntimeError("Open a game screen before drawing.")
    turtle = _human_turtle
    x = float(x)
    y = float(y)
    size = float(size)
    offset = size / 3
    front = [(x, y), (x + size, y), (x + size, y + size), (x, y + size), (x, y)]
    back = [(px + offset, py + offset) for px, py in front]
    turtle.penup()
    for shape in (front, back):
        turtle.goto(*shape[0])
        turtle.pendown()
        for point in shape[1:]:
            turtle.goto(*point)
        turtle.penup()
    for start, end in zip(front[:-1], back[:-1]):
        turtle.goto(*start)
        turtle.pendown()
        turtle.goto(*end)
        turtle.penup()


def _human_show_game():
    if _human_game_screen is None:
        raise RuntimeError("Open a game screen before showing it.")
    _human_game_screen.mainloop()


def _human_mobile_app(title):
    return {"title": title, "screens": []}


def _human_save_mobile_app(app, folder):
    folder_path = Path(folder)
    folder_path.mkdir(parents=True, exist_ok=True)
    title = html.escape(str(app["title"]))
    screens = "\\n".join(f"<section><h2>{html.escape(str(screen))}</h2></section>" for screen in app["screens"])
    (folder_path / "index.html").write_text(
        f"<!doctype html><html><head><meta name=\\"viewport\\" content=\\"width=device-width, initial-scale=1\\"><title>{title}</title></head><body><h1>{title}</h1>{screens}</body></html>",
        encoding="utf-8",
    )
    (folder_path / "manifest.json").write_text(
        json.dumps({"name": str(app["title"]), "display": "standalone", "start_url": "index.html"}, indent=2),
        encoding="utf-8",
    )

'''
    return header + "\n".join(python_lines) + "\n"


def read_source_file(source_path: Path) -> str:
    if not source_path.exists():
        raise FileNotFoundError(
            f"HumanLang could not find '{source_path}'. Create the file first, or run an existing file like examples\\simple.hl."
        )

    if source_path.suffix.lower() != ".hl":
        raise ValueError(f"HumanLang files should use the .hl extension: {source_path}")

    return source_path.read_text(encoding="utf-8")


def run_humanlang(source_path: Path) -> int:
    source = read_source_file(source_path)
    python_code = translate(source, source_path)
    namespace = {"__name__": "__humanlang__", "__file__": str(source_path)}
    exec(compile(python_code, str(source_path), "exec"), namespace)
    return 0


def build_humanlang(source_path: Path, output_path: Path) -> int:
    source = read_source_file(source_path)
    python_code = translate(source, source_path)
    output_path.write_text(python_code, encoding="utf-8")
    return 0


def run_cli() -> int:
    parser = argparse.ArgumentParser(description="Run or build HumanLang .hl files.")
    subparsers = parser.add_subparsers(dest="command")

    run_parser = subparsers.add_parser("run", help="Run a HumanLang file.")
    run_parser.add_argument("source", type=Path, help="Path to a .hl HumanLang file.")
    run_parser.add_argument("script_args", nargs=argparse.REMAINDER, help="Arguments passed to the HumanLang program.")

    build_parser = subparsers.add_parser("build", help="Translate a HumanLang file into Python.")
    build_parser.add_argument("source", type=Path, help="Path to a .hl HumanLang file.")
    build_parser.add_argument("--out", type=Path, required=True, help="Generated Python file path.")

    translate_parser = subparsers.add_parser("translate", help="Print generated Python.")
    translate_parser.add_argument("source", type=Path, help="Path to a .hl HumanLang file.")

    parser.add_argument("legacy_source", nargs="?", type=Path, help=argparse.SUPPRESS)
    parser.add_argument("--out", type=Path, help=argparse.SUPPRESS)
    parser.add_argument("--run", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()

    if args.command == "run":
        return run_humanlang(args.source)

    if args.command == "build":
        return build_humanlang(args.source, args.out)

    if args.command == "translate":
        source = read_source_file(args.source)
        print(translate(source, args.source), end="")
        return 0

    if args.legacy_source:
        if args.run:
            return run_humanlang(args.legacy_source)
        source = read_source_file(args.legacy_source)
        python_code = translate(source, args.legacy_source)
        if args.out:
            args.out.write_text(python_code, encoding="utf-8")
        else:
            print(python_code, end="")
        return 0

    parser.print_help()
    return 2


def main() -> int:
    try:
        return run_cli()
    except (FileNotFoundError, OSError, SyntaxError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
