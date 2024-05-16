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
# **text** -> <b>text</b>
bold_replace_regex = re.compile(r'[*_]{2}([^*]+)[*_]{2}')
bold_replace_func = lambda parts: "<strong>{0}</strong>".format(*parts.groups())


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

    anchors = link_replace_regex.sub(link_replace_func, source_text)
    bolded = bold_replace_regex.sub(bold_replace_func, anchors)

    output_text = bolded

    if not args.output:  # check if output flag was not raised
        print("Converted Text:\n\n" + output_text)
    else:
        print(f"Writing converted text to file '{args.output}' - WARNING this will overwrite any existing file")
        with open(args.output, 'w') as out_file:
            out_file.write(output_text)
