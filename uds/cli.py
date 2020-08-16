import argparse
import html
import crayons
import sys
import textwrap


import uds


def colorize(text, color, bold=False):
    """
    https://github.com/kennethreitz/crayons
    Included colors are red, green, yellow, blue, black,
    magenta, cyan, white, and normal
    """
    return eval("str(crayons.{}(text, bold=bold))".format(color))


def main():
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument(
        "word",
        help="Word to search for meaning on UrbanDictionary",
        type=str,
        nargs="+",
    )
    parser.add_argument(
        "-s", "--source", help="Which dictionary to search", type=str, default="urban",
    )
    parser.add_argument(
        "-n", "--count", help="Number of meanings to display", type=int, default=8,
    )
    args = parser.parse_args()
    word_to_search = " ".join(args.word)

    def normalize(text, padding=" " * 6):
        # NOTE unescape seems do not work as text missing `;`, e.g `&apos;` ->
        # `&apos`, thus, use dirty replace
        cleaned = html.unescape(text).replace("&apos", "'")
        cleaned = textwrap.fill(cleaned, width=120)
        cleaned = textwrap.indent(cleaned, prefix=padding).strip()
        return cleaned

    def pad_lines(text, pad=""):
        padded = "\n        ".join(
            (
                "{pad}{line}".format(line=normalize(line), pad=pad)
                for line in text.splitlines()
                if line
            )
        )
        return padded

    if args.source == "urban":
        dictionary = "UrbanDictionary"
    elif "cam" in args.source:
        dictionary = "Cambridge"
    elif "fr" in args.source:
        dictionary = "fr"

    print(
        colorize(
            "{} results for {}".format(
                dictionary, colorize(word_to_search, "yellow", bold=True)
            ),
            "blue",
            bold=True,
        )
    )

    result = uds.get_meanings(word_to_search, source=args.source)
    meanings = result["means"]
    ipa = result["ipa"]
    if not meanings:
        sys.exit(crayons.red("There are no definitions for this word."))

    print(ipa)
    for idx, _meaning in enumerate(meanings, start=1):
        result = "{:>2}{idx}.  {meaning}".format(
            "", idx=colorize(idx, "red"), meaning=pad_lines(_meaning)
        )
        print(result)
        if idx == args.count:
            break


if __name__ == "__main__":
    main()
