import re
import itertools

def get_extract_regex(extract_pattern):
    # 1. Split by {}
    # 2. Change every escaped brace ('\}' or '\{') to a brace
    # 3. Make everything that was split a regex
    # 4. Join using regex capture groups
    regex_str = '(.*)'.join([re.escape(part.replace(r"\{", "{").replace(r"\}", "}")) \
            for part in extract_pattern.split("{}")])
    return re.compile("^" + regex_str + "$")

def get_extracted_regexes(extract_pattern):
    if extract_pattern == None:
        return None
    return [get_extract_regex(single_line_pattern) \
            for single_line_pattern in extract_pattern.split("\n")]

def input_lines(extract_pattern = None, filename = "/dev/stdin"):
    extracted_regexes = get_extracted_regexes(extract_pattern)

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
            first_line = first_line.removesuffix("\n")

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
            yield extracted
