def run_custom_code(lines):
    i = 0
    loop_start = None
    variables = {}
    skip_until = None

    while i < len(lines):
        line = lines[i].strip()

        # Remove comments
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

                    if value.startswith('"') and value.endswith('"'):
                        variables[name] = value.strip('"')
                    else:
                        variables[name] = eval(value, {}, variables)
                else:
                    name = rest.strip()
                    variables[name] = None
            except Exception as e:
                print(f"Error in variable declaration: {e}")

        # if statements
        elif line.startswith("if ") and ("==" in line or "?=" in line):
            condition_line = line[3:].strip()
            negate = "?=" in condition_line
            comparator = "!=" if negate else "=="
            parts = condition_line.split("?=" if negate else "==")

            try:
                left = parts[0].strip()
                right = parts[1].strip()

                # Evaluate op[...] if used
                if left.startswith("op[") and left.endswith("]"):
                    left = eval(left[3:-1], {}, variables)
                elif left in variables:
                    left = variables[left]
                else:
                    left = eval(left, {}, variables)

                if right.startswith("op[") and right.endswith("]"):
                    right = eval(right[3:-1], {}, variables)
                elif right in variables:
                    right = variables[right]
                else:
                    right = eval(right, {}, variables)

                condition = (left != right) if negate else (left == right)
                if not condition:
                    skip_until = 'if.end'

            except Exception as e:
                print(f"Error in if condition: {e}")
                skip_until = 'if.end'

        elif line == "if.end":
            pass  # Handled above

        # Operation: print(op[...])
        elif line.startswith("print(op[") and line.endswith("])"):
            expression = line[len("print(op["):-2].strip()
            try:
                result = eval(expression, {}, variables)
                print(result)
            except Exception as e:
                print(f"Error in op expression: {e}")

        # Regular print
        elif line.startswith('print(') and line.endswith(')'):
            to_print = line[len('print('):-1].strip()
            try:
                if to_print in variables:
                    print(variables[to_print])
                else:
                    result = eval(to_print, {}, variables)
                    print(result)
            except Exception as e:
                print(f"Error in print statement: {e}")

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
    print(" ")
    print("atom compiler 2025.0")
    print(" ")
    print("by SPACECAT")
    path = input("Enter the path to your .atom code file: ").strip()
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
