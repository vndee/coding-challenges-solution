import os
import io
import sys
import argparse


def count_characters(data):
    return len(data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="wc tool")
    parser.add_argument("file", nargs='?', help="file to count")
    parser.add_argument("-l", "--lines", action="store_true", help="count lines")
    parser.add_argument("-w", "--words", action="store_true", help="count words")
    parser.add_argument("-c", "--bytes", action="store_true", help="count bytes")
    parser.add_argument("-m", "--chars", action="store_true", help="count chars")
    args = parser.parse_args()

    if not (args.lines or args.words or args.bytes or args.chars):
        args.lines, args.words, args.bytes = True, True, True

    if args.file and not os.path.exists(args.file):
        print(f"wc: {args.file}: No such file or directory")
        exit(1)

    if args.file:
        try:
            file = open(args.file, "rb")
        except OSError as e:
            print(e)
            sys.exit(1)
    else:
        file = io.BytesIO()
        input_bytes = sys.stdin.read().encode()
        file.write(input_bytes)

    if args.lines:
        file.seek(0)
        print(len(file.read().decode().split("\n")), end=" ")
    if args.words:
        file.seek(0)
        print(len(file.read().decode().split()), end=" ")
    if args.bytes:
        file.seek(0)
        print(len(file.read()), end=" ")
    if args.chars:
        file.seek(0)
        print(len(file.read().decode()), end=" ")

    if args.file:
        print(args.file)
    else:
        print()
