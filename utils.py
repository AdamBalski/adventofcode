import re
import itertools

DEFAULT_PARSING_FUNCTIONS = {
        "int": int,
        "float": float,
        "str": str,
        "split": lambda line: line.split(),
        "csplit": lambda line: line.split(","),
        "list": list,
        "add": sum,
        "range": lambda el: list(range(el))
}

def get_extract_regex(extract_pattern):
    # 1. Split by {}
    # 2. Change every escaped brace ('\}' or '\{') to a brace
    # 3. Make everything that was split a regex
    # 4. Join using regex capture groups
    regex_str = '(.*)'.join([re.escape(part.replace(r"\{", "{").replace(r"\}", "}")) \
            for part in re.split("{[a-z_:*#.]*}", extract_pattern)])
    return re.compile("^" + regex_str + "$")


def get_extracted_regexes(extract_pattern):
    if extract_pattern == None:
        return None

    return [get_extract_regex(single_line_pattern) \
            for single_line_pattern in extract_pattern.split("\n")]

def get_func_by_ident(ident, functions_dict):
    if ident in functions_dict:
        return functions_dict[ident]
    if ident in DEFAULT_PARSING_FUNCTIONS:
        return DEFAULT_PARSING_FUNCTIONS[ident]
    raise Exception(f"Could not find parsing function named: {ident}")

def get_not_stacked_parsing_function(expr, functions_dict, default_func):
    if expr == "":
        return default_func
    if expr[0] == "*":
        inner = get_not_stacked_parsing_function(expr[1:], functions_dict, default_func)
        return lambda data: list(map(inner, data))
    if expr[0] == ".":
        inner = get_not_stacked_parsing_function(expr[1:], functions_dict, default_func)
        return lambda data: ''.join(map(inner, data))
    if expr[0] == "#":
        inner = get_not_stacked_parsing_function(expr[1:], functions_dict, default_func)
        return lambda data: [subelement for element in data for subelement in inner(element)]
    if expr[0] == "?":
        inner = get_not_stacked_parsing_function(expr[1:], functions_dict, default_func)
        return lambda data: list(filter(inner, data))
    return get_func_by_ident(expr, functions_dict)

def get_parsing_function(expr, functions_dict, default_func):
    funcs = [get_not_stacked_parsing_function(func, functions_dict, default_func) \
            for func in expr.split(":")]
    def parsing_function(element):
        for func in funcs:
            element = func(element)
        return element
    return parsing_function

def get_parsing_functions(pattern, functions_dict, default_func):
    result = []
    for function_identifier in re.findall("{([a-z_:*#.]*)}", pattern):
        result.append(get_parsing_function(function_identifier, functions_dict, default_func))
    return result


def input_lines(extract_pattern = None, default_func=str, line_feed_block_separator = False, \
        parsing_functions_dict = {}, filename = "/dev/stdin"):

    default_func_resolved = default_func
    if type(default_func) == str:
        default_func_resolved = get_parsing_function(default_func, parsing_functions_dict, str)
        
    extracted_regexes = get_extracted_regexes(extract_pattern)
    parsing_functions = get_parsing_functions(extract_pattern, parsing_functions_dict, default_func_resolved)

    with open(filename, "r") as file:
        for first_line in file:
            # If we don't extract anything, just flush line by line
            if extracted_regexes == None:
                yield first_line
                continue
            # Get the entire block
            curr_lines = [first_line]
            for line in itertools.islice(file, len(extracted_regexes) - 1):
                curr_lines.append(line)

            # Check whether the block is not truncated
            if len(curr_lines) != len(extracted_regexes):
                # if the last lines are all empty, then don't raise any exceptions
                if all(line == "" for line in curr_lines):
                    continue
                raise Exception("The last block may be truncated") 

            # Extract all the fields
            extracted = []
            for line, regex in zip(curr_lines, extracted_regexes):
                match = regex.match(line)
                assert match != None
                groups = match.groups()
                extracted.extend(groups)
            yield [parsing_func(extracted_field) \
                    for extracted_field, parsing_func in zip(extracted, parsing_functions)]

            # Go past the block separator
            if not line_feed_block_separator:
                continue
            for newline in itertools.islice(file, 1):
                assert newline == "\n"

def input_blocks(*extract_pattern, parsing_functions_dict = {}, \
        default_func=lambda x: str(x), filename = "/dev/stdin"):
    return input_lines('\n'.join(extract_pattern), parsing_functions_dict=parsing_functions_dict,\
            default_func=default_func, line_feed_block_separator=True, filename=filename)

