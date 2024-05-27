# Simple Markdown Converter
This project is a simple markdown to HTML converter built using python and regular expressions.

Can't promise it'll work with everything. It is simple after all.


## Replacements

- Links: following the [standard markup syntax](https://www.markdownguide.org/basic-syntax/#links)
- **Bold** and _Italics_: * and _ are the emphasis characters, two for bold one for italics
- Line breaks: either manually using the `&ltbr&gt` tag in the raw markdown or automatically with two newlines
- Headers: maximum depth of six as per HTML spec
- Unordered Lists: uses the standard markdown UL syntax **WARNING: currently does not support multi-level lists**


## TODO
- Add ordered lists
- Add support for multilevel ordered and unordered lists
- Add support for inline code blocks
- Add support for block quotes (including nested)
- Potentially add support for replacing less than and greater than symbols in code blocks to use the html sage &lt &amp &gt
- Add cleanup to remove empty lines from final output
