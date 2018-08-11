"""This module implement common utility functions"""
import re
import keyword
import tokenize
from io import BytesIO
import builtins
from collections import defaultdict

COLOR_CODE_REGEX = r"\[0(;[0-9]+)?m"
URL_FORMAT_REGEX = r"<(.*?)>"


def is_reserved_identifier(token):
    """Check if `token` is a reserved Python identifier.

    Args:
        token (str): String sequence with a specific definition (for parser).

    Returns:
        bool: True if `token` is a reserved identifier, False otherwise.
    """

    return keyword.iskeyword(token) or hasattr(builtins, token)

def replace_color_codes(text, replacement):
    """Replace ANSI color sequence from a given string.

    Args:
        text (str): Original string to replacement from.
        replacement (str): String to replace color codes with.

    Returns:
        str: Mutated string after the replacement.
    """

    return re.sub(COLOR_CODE_REGEX, replacement, text)

def replace_url_format(text):
    """Replace parsed URL format from a given string.
    https://api.slack.com/docs/message-formatting#linking_to_urls

    Args:
        text (str): Original string to replacement from.

    Returns:
        str: Mutated string after the replacement.
    """

    url_content_match = re.search(URL_FORMAT_REGEX, text)
    if url_content_match is None:
        return text

    url_content = url_content_match.group(1)

    return re.sub(URL_FORMAT_REGEX, url_content, text)

def get_bold_token(token):
    """Apply bold formatting to a given token.
    https://api.slack.com/docs/message-formatting#message_formatting

    Args:
        token (str): String sequence with a specific definition (for parser).

    Returns:
        str: bold formatted version of a token.
    """

    return "*{}*".format(token)

def get_italic_token(token):
    """Apply italic formatting to a given token.
    https://api.slack.com/docs/message-formatting#message_formatting

    Args:
        token (str): String sequence with a specific definition (for parser).

    Returns:
        str: bold formatted version of a token.
    """

    return "_{}_".format(token)

def get_formatted_input(input_text):
    """Format a given string as per the convention.

    - Reserved identifiers such as 'keyword', 'built-in methods', 'exceptions'
    are formatted black
    - Comments are formatted italic

    Args:
        input_text (str): Python source code to format.

    Returns:
        str: Formatted version of the source code string.
    """

    # After tokenization, generator produces 5-tuples:
    #
    # token type
    # token string
    # 2-tuple (srow, scol) of ints, the row and column where the token starts
    # 2-tuple (erow, ecol) of ints, the row and column where the token ends
    # line number where the token was found
    token_generator = tokenize.tokenize(BytesIO(input_text.encode('utf-8')).readline)

    # List of lines in input
    input_text_lines = input_text.splitlines()

    # List to hold the formatted input lines
    formatted_text_lines = []

    # Dictionary of reserved tokens and their metadata per line
    # For each line if a reserved token is found, a 4-tuple is added
    # (token_start_index, token_end_index, token_value, token_type)
    reserved_tokens_inline = defaultdict(list)

    # Iterate over all available token-tuples (token metadata)
    for tok_type, tok_val, tok_start, tok_end, _ in token_generator:
        # Check if the token is a reserved identifier
        # For example, (keywords, built-in methods, exceptions etc.)
        if tok_type == tokenize.NAME and is_reserved_identifier(tok_val):
            # Append 4-tuple for reserved token in line number (tok_start[0])
            reserved_tokens_inline[tok_start[0]].append(
                (tok_start[1], tok_end[1], tok_val, tok_type)
            )

        # Append 4-tuple for the comment token
        if tok_type == tokenize.COMMENT:
            reserved_tokens_inline[tok_start[0]].append(
                (tok_start[1], tok_end[1], tok_val, tok_type)
            )

    # Iterate over each line in input text
    for line_index, _ in enumerate(input_text_lines):
        # Add the original input line in formatted input lines
        formatted_text_lines.append(input_text_lines[line_index])

        # If there is (at least) one reserved token in this line
        if line_index + 1 in reserved_tokens_inline:
            # List of all reserved token inline
            inline_tokens = reserved_tokens_inline[line_index + 1]

            # Iterate over each token
            for token_index, _ in enumerate(inline_tokens):
                token_start, token_end, token_value, token_type = inline_tokens[token_index]

                # Replace the formatted input line based on the token index/value
                formatted_text_lines[line_index] = "{}{}{}".format(
                    formatted_text_lines[line_index][:(token_start + (2 * token_index))],
                    get_italic_token(token_value) if token_type == tokenize.COMMENT else get_bold_token(token_value),
                    formatted_text_lines[line_index][(token_end + (2 * token_index)):],
                )

    # join and return the formatted input lines
    return "\n".join(formatted_text_lines)
