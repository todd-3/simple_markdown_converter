import re
import argparse


# ---------------------------------------- #
# markup seek regexes and associated replace functions
# ---------------------------------------- #

# link replacement
# [name](url) -> <a href=url>name</a>
link_replace_regex = re.compile(r'\[([^\[\]]+)]\(([^()]+)\)')
link_replace_func = lambda parts: "<a href=\"{1}\">{0}</a>".format(*parts.groups())

# bold replacement
# **text** | __text__ -> <strong>text</strong>
bold_replace_regex = re.compile(r'[*_]{2}([^*]+)[*_]{2}')
bold_replace_func = lambda parts: f"<strong>{parts.groups()[0]}</strong>"

# italics replacement
# *text* | _text_ -> <em>text</em>
italics_replace_regex = re.compile(r'[*_]([^*]+)[*_]')
italics_replace_func = lambda parts: f"<em>{parts.groups()[0]}</em>"

# header replacement
# #{n} text -> <h{n}>text</h{n}>
header_replace_regex = re.compile(r'^(#{,6}) ([^\r\n]+)$', flags=re.MULTILINE)
header_replace_func = lambda parts: f"<h{len(parts.groups()[0])}>{parts.groups()[1]}</h{len(parts.groups()[0])}>"

# paragraph wrapping
# wraps text in paragraph blocks
paragraph_wrap_regex = re.compile(r'^(?!<h\d>|\n)([\D\d]+?)(?=\n\n|\n\Z|\Z)', flags=re.MULTILINE)  # this expression needs to be improved
paragraph_wrap_func = lambda parts: f"<p>{parts.groups()[0]}</p>"


replace_ops: dict[str: tuple[re.Pattern, callable(re.Match)]] = {
    "Headers": (header_replace_regex, header_replace_func),
    "Paragraphs": (paragraph_wrap_regex, paragraph_wrap_func),
    "Links": (link_replace_regex, link_replace_func),
    "Bold": (bold_replace_regex, bold_replace_func),
    "Italics": (italics_replace_regex, italics_replace_func)
}


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="Simple Markdown Converter",
        description="A simple tool to convert markdown into html."
    )

    parser.add_argument('input', type=str)
    parser.add_argument('--text', '-t', action='store_true', default=False)
    parser.add_argument('--output', '-o', type=str, default=None)

    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()

    if args.text:  # check if the text flag was raised
        source_text: str = args.input
    else:
        try:
            print(f"Opening file '{args.input}' to retrieve text for conversion.")
            with open(args.input, 'r') as source_file:
                source_text: str = source_file.read()
        except FileNotFoundError:
            print("Could not find file " + args.input)
            exit(1)

    for op_name, tools in replace_ops.items():
        print(f"Running {op_name} Operation")
        source_text = tools[0].sub(tools[1], source_text)

    if not args.output:  # check if output flag was not raised
        print("Converted Text:\n\n" + source_text)
    else:
        print(f"Writing converted text to file '{args.output}' - WARNING this will overwrite any existing file")
        with open(args.output, 'w') as out_file:
            out_file.write(source_text)
