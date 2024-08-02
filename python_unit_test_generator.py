import sys
import locale
import re

FUNCTION_REGEX = r"((@.*\n)?\s*def (.*)\((.|\n)*?\)( -> .*?)?:(?=(.|\n)*?((@.*?)?\n(@.*\n)?\s*def)||(\s*\Z)))"
HELP = "Usage: python_unit_test_generator <file_path> <output_path> (default = output.py in cwd)>"

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print(HELP)
        sys.exit()
    if len(sys.argv) > 3:
        raise ValueError(f"Too many arguments.\n{HELP}")
    file_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) >= 3 else "output.py"

    try:
        with open(file_path) as f:
            code = f.read()
    except FileNotFoundError:
        raise ValueError(f"File {file_path} does not exist") from None
    except UnicodeDecodeError as e:
        raise Exception(f"Failed to read file {file_path} (your locale is {locale.getpreferredencoding()},"
                        f" try changing it - for windows, see https://stackoverflow.com/a/66351796/22081657):"
                        f" {e}") from None

    newcode = """import unittest


class GeneratedTests(unittest.TestCase):
"""
    matches = re.findall(FUNCTION_REGEX, code)
    if len(matches) >= 1:
        func_names = []
        for match in matches:
            if match[2] in func_names:
                addnum = 2
                while f"{match[2]}{addnum}" in func_names:
                    addnum += 1
                func_names.append(f"{match[2]}{addnum}")

                print(f"Detected that there are multiple functions named {match[2]} in different classes (or perhaps"
                      f" redefinitions of the same function), so renamed one to {match[2]}{addnum} in the generated"
                      f" test cases. Note: This tool works best on code with only one class / no function"
                      f" redefinitions, so duplicate function names can be avoided.")
            else:
                func_names.append(match[2])
        for name in func_names:
            newcode += f"""    def test_{name}(self) -> None:
        ...

"""
    else:
        newcode += """    pass
"""
    with open(output_path, "w") as f:
        f.write(newcode)
