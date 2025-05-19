import random
import subprocess
from tkinter import Tk, filedialog

def run_custom_code(lines):
    i = 0
    loop_start = None
    variables = {}
    skip_until = None

    while i < len(lines):
        line = lines[i].strip()

        if '//' in line:
            line = line.split('//')[0].strip()
        if not line:
            i += 1
            continue

        if skip_until:
            if line == 'if.end':
                skip_until = None
            i += 1
            continue

        # Variable declaration
        if line.startswith("var "):
            try:
                _, rest = line.split("var ", 1)
                if "=" in rest:
                    name, value = rest.split("=", 1)
                    name = name.strip()
                    value = value.strip()

                    # num.random(min - max)
                    if value.startswith("num.random(") and value.endswith(")"):
                        minmax = value[len("num.random("):-1].split('-')
                        min_val = int(minmax[0].strip())
                        max_val = int(minmax[1].strip())
                        variables[name] = random.randint(min_val, max_val)

                    elif value.startswith('"') and value.endswith('"'):
                        variables[name] = value.strip('"')
                    else:
                        variables[name] = eval(value, {}, variables)
                else:
                    name = rest.strip()
                    variables[name] = None
            except Exception as e:
                print(f"Error in variable declaration: {e}")

        # if statements (== or ?=)
        elif line.startswith("if ") and ("==" in line or "?=" in line):
            condition_line = line[3:].strip()
            negate = "?=" in condition_line
            parts = condition_line.split("?=" if negate else "==")

            try:
                left = parts[0].strip()
                right = parts[1].strip()

                def eval_expr(expr):
                    if expr.startswith("op[") and expr.endswith("]"):
                        return eval(expr[3:-1], {}, variables)
                    if expr in variables:
                        return variables[expr]
                    return eval(expr, {}, variables)

                left_val = eval_expr(left)
                right_val = eval_expr(right)
                condition = (left_val != right_val) if negate else (left_val == right_val)
                if not condition:
                    skip_until = 'if.end'
            except Exception as e:
                print(f"Error in if condition: {e}")
                skip_until = 'if.end'

        elif line == "if.end":
            pass

        # start(appname)
        elif line.startswith("start(") and line.endswith(")"):
            app = line[len("start("):-1].strip().strip('"')
            try:
                subprocess.Popen(app)
            except Exception as e:
                print(f"Failed to start app: {e}")

        # print(op[...])
        elif line.startswith("print(op[") and line.endswith("])"):
            expression = line[len("print(op["):-2].strip()
            try:
                result = eval(expression, {}, variables)
                print(result)
            except Exception as e:
                print(f"Error in op expression: {e}")

        # print(...) with num.random or comparison
        elif line.startswith("print(") and line.endswith(")"):
            content = line[len("print("):-1].strip()

            if "?=" in content:
                parts = content.split("?=")
                left = parts[0].strip()
                right = parts[1].strip()
                try:
                    left_val = variables.get(left, eval(left, {}, variables))
                    right_val = variables.get(right, eval(right, {}, variables))
                    print(left_val != right_val)
                except:
                    print("False")
            else:
                try:
                    if content.startswith("num.random(") and content.endswith(")"):
                        minmax = content[len("num.random("):-1].split('-')
                        min_val = int(minmax[0].strip())
                        max_val = int(minmax[1].strip())
                        print(random.randint(min_val, max_val))
                    elif content in variables:
                        print(variables[content])
                    else:
                        print(eval(content, {}, variables))
                except Exception as e:
                    print(f"Error in print: {e}")

        elif line == 'loop':
            loop_start = i + 1

        elif line == 'loop.begin':
            if loop_start is None:
                print("Error: loop.begin without loop")
                return
            i = loop_start
            continue

        else:
            print(f"Unknown command: {line}")

        i += 1


def main():
    print("\natom compiler 2025.1\n")
    print("by SPACECAT\n")

    # File picker instead of input
    Tk().withdraw()
    path = filedialog.askopenfilename(filetypes=[("Atom Files", "*.atom"), ("All Files", "*.*")])
    if not path:
        print("No file selected.")
        return

    try:
        with open(path, 'r') as f:
            code_lines = f.readlines()
    except Exception as e:
        print(f"Could not open file: {e}")
        return

    run_custom_code(code_lines)


if __name__ == "__main__":
    main()
    input("Press Enter to exit...")
