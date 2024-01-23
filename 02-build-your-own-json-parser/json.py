import os
import sys
import argparse


def parse_value(value_str):
    value_str = value_str.strip()
    if value_str.startswith('"'):
        end_quote = value_str.find('"', 1)
        if end_quote == -1:
            raise ValueError("Invalid JSON: Unclosed string")
        return value_str[1:end_quote], value_str[end_quote + 1:]

    elif value_str.startswith('true'):
        return True, value_str[4:]
    elif value_str.startswith('false'):
        return False, value_str[5:]
    elif value_str.startswith('null'):
        return None, value_str[4:]
    elif value_str[0].isdigit() or value_str[0] in '-+':
        for i, char in enumerate(value_str):
            if not char.isdigit() and char not in '.-+eE':
                return float(value_str[:i]), value_str[i:]
        return float(value_str), ''
    elif value_str.startswith('{'):
        obj, remaining = parse_object(value_str)
        return obj, remaining
    elif value_str.startswith('['):
        lst, remaining = parse_array(value_str)
        return lst, remaining
    else:
        raise ValueError("Invalid JSON: Unrecognized value")


def parse_object(obj_str):
    if not obj_str.startswith('{'):
        raise ValueError("Invalid JSON: Expected '{'")
    obj_str = obj_str[1:].strip()
    obj = {}
    while obj_str and not obj_str.startswith('}'):
        key, obj_str = parse_value(obj_str)
        obj_str = obj_str.strip()
        if not obj_str.startswith(':'):
            raise ValueError("Invalid JSON: Expected ':' after key")
        obj_str = obj_str[1:].strip()
        value, obj_str = parse_value(obj_str)
        obj_str = obj_str.strip()
        obj[key] = value
        if obj_str.startswith(','):
            obj_str = obj_str[1:].strip()
    if not obj_str.startswith('}'):
        raise ValueError("Invalid JSON: Expected '}'")
    return obj, obj_str[1:]


def parse_array(arr_str):
    if not arr_str.startswith('['):
        raise ValueError("Invalid JSON: Expected '['")
    arr_str = arr_str[1:].strip()
    arr = []
    while arr_str and not arr_str.startswith(']'):
        value, arr_str = parse_value(arr_str)
        arr_str = arr_str.strip()
        arr.append(value)
        if arr_str.startswith(','):
            arr_str = arr_str[1:].strip()
    if not arr_str.startswith(']'):
        raise ValueError("Invalid JSON: Expected ']'")
    return arr, arr_str[1:]


def parse(json_string: str) -> dict:

    obj, remaining = parse_object(json_string)
    if remaining.strip():
        raise ValueError("Invalid JSON: Extra data after parsing")
    return obj


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="json tool")
    parser.add_argument("file", nargs='?', help="file to parse")
    args = parser.parse_args()

    if args.file and not os.path.exists(args.file):
        print(f"json: {args.file}: No such file or directory")
        exit(1)

    try:
        with open(args.file, "r") if args.file else sys.stdin as file:
            json_string = file.read()
            parsed_json = parse(json_string)
            print(parsed_json)
    except ValueError as e:
        print(e)
        sys.exit(1)
    except OSError as e:
        print(e)
        sys.exit(1)
