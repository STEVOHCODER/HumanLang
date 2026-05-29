from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


HUMAN_NAME = r"[A-Za-z_][A-Za-z0-9_]*(?:\s+[A-Za-z0-9_]+)*"
ASK_RE = re.compile(rf'^(?:ask|get)\s+"(?P<question>.*)"\s+and\s+remember\s+it\s+as\s+(?P<name>{HUMAN_NAME})$', re.IGNORECASE)
ASK_NUMBER_RE = re.compile(rf'^(?:ask|get|say)\s+number\s+"(?P<question>.*)"\s+and\s+remember\s+it\s+as\s+(?P<name>{HUMAN_NAME})$', re.IGNORECASE)
REMEMBER_RE = re.compile(rf"^remember\s+(?P<value>.+)\s+as\s+(?P<name>{HUMAN_NAME})$", re.IGNORECASE)
CALCULATE_RE = re.compile(rf"^calculate\s+(?P<value>.+?)\s+as\s+(?P<name>{HUMAN_NAME})$", re.IGNORECASE)
CALCULATE_PRINT_RE = re.compile(r"^calculate\s+(?P<value>.+)$", re.IGNORECASE)
CHANGE_RE = re.compile(rf"^(?:change|set)\s+(?P<name>{HUMAN_NAME})\s+to\s+(?P<value>.+)$", re.IGNORECASE)
REPEAT_RE = re.compile(r"^repeat\s+(?P<count>.+)\s+times:$", re.IGNORECASE)
IF_RE = re.compile(
    r"^if\s+(?P<left>.+?)\s+(?P<operator>is at least|is at most|is greater than|is less than|is not|is|equals|does not equal)\s+(?P<right>.+):$",
    re.IGNORECASE,
)


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


def translate_code_words(expression: str, variables: dict[str, str]) -> str:
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
    return expression


def translate_expression(expression: str, variables: dict[str, str]) -> str:
    expression = expression.strip().rstrip(",")
    lowered = expression.lower()

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

    ask_number_match = ASK_NUMBER_RE.match(stripped)
    if ask_number_match:
        question = ask_number_match.group("question")
        name = remember_name(variables, ask_number_match.group("name"))
        return f'{indent}{name} = float(input("{question} "))'

    ask_match = ASK_RE.match(stripped)
    if ask_match:
        question = ask_match.group("question")
        name = remember_name(variables, ask_match.group("name"))
        return f'{indent}{name} = input("{question} ")'

    if lowered.startswith("say ") or lowered.startswith("show ") or lowered.startswith("print "):
        value = re.sub(r"^(say|show|print)\s+", "", stripped, count=1, flags=re.IGNORECASE)
        value = translate_expression(value, variables)
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

    if_match = IF_RE.match(stripped)
    if if_match:
        condition = translate_condition(
            if_match.group("left"),
            if_match.group("operator"),
            if_match.group("right"),
            variables,
        )
        return f"{indent}if {condition}:"

    if lowered == "otherwise:":
        return f"{indent}else:"

    repeat_match = REPEAT_RE.match(stripped)
    if repeat_match:
        count = translate_expression(repeat_match.group("count"), variables)
        return f"{indent}for _ in range(int({count})):"

    if lowered == "stop":
        return f"{indent}break"

    if lowered == "continue":
        return f"{indent}continue"

    raise SyntaxError(f"Line {line_number}: HumanLang does not understand: {stripped}")


def translate(source: str) -> str:
    lines = source.splitlines()
    variables: dict[str, str] = {}
    python_lines = [translate_line(line, index + 1, variables) for index, line in enumerate(lines)]
    return "import math\n\n" + "\n".join(python_lines) + "\n"


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
    python_code = translate(source)
    namespace = {"__name__": "__humanlang__", "__file__": str(source_path)}
    exec(compile(python_code, str(source_path), "exec"), namespace)
    return 0


def build_humanlang(source_path: Path, output_path: Path) -> int:
    source = read_source_file(source_path)
    python_code = translate(source)
    output_path.write_text(python_code, encoding="utf-8")
    return 0


def run_cli() -> int:
    parser = argparse.ArgumentParser(description="Run or build HumanLang .hl files.")
    subparsers = parser.add_subparsers(dest="command")

    run_parser = subparsers.add_parser("run", help="Run a HumanLang file.")
    run_parser.add_argument("source", type=Path, help="Path to a .hl HumanLang file.")

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
        print(translate(source), end="")
        return 0

    if args.legacy_source:
        if args.run:
            return run_humanlang(args.legacy_source)
        source = read_source_file(args.legacy_source)
        python_code = translate(source)
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
