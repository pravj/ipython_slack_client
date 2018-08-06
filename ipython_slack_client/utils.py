import re
import keyword

COLOR_CODE_REGEX = "\[0(;[0-9]+)?m"


def is_identifier(token):
    return keyword.iskeyword(token) or token in dir(__builtins__)

def replace_color_codes(text, replacement):
    return re.sub(COLOR_CODE_REGEX, replacement, text)

def get_bold_token(token):
    return "*{}*".format(token)

def get_bold_text(text):
    return list(map(lambda t: get_bold_token(t) if is_identifier(t) else t, text.split(" ")))

def get_formatted_input(input_text):
    text_lines = input_text.split("\n")

    formatted_text_lines = list(map(
        lambda l: list(map(
            lambda t: get_bold_token(t) if is_identifier(t) else t, l.split(" ")
        )), text_lines
    ))

    formatted_input = ""
    for line in formatted_text_lines:
        formatted_input += " ".join(line)
        formatted_input += "\n"

    return formatted_input
