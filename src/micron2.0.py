import os
import sys
import traceback
import time
from tkinter import messagebox

# ╔══════════════════════════════════════╗
# ║ ▒█▀▄▀█ ▀█▀ ▒█▀▀█ ▒█▀▀█ ▒█▀▀▀█ ▒█▄░▒█ ║
# ║ ▒█▒█▒█ ▒█░ ▒█░░░ ▒█▄▄▀ ▒█░░▒█ ▒█▒█▒█ ║
# ║ ▒█░░▒█ ▄█▄ ▒█▄▄█ ▒█░▒█ ▒█▄▄▄█ ▒█░░▀█ ║
# ╚══════════════════════════════════════╝

# ANSI
RESET = "\033[0m"       # Reset
BOLD = "\033[1m"     # Bold
UNDERLINING = "\033[4m"   # Underlining

# Text Color
CYAN = "\033[36m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RED = "\033[31m"
WHITE = "\033[37m"
GREY = "\033[90m"

# Background
BLUE = "\033[44m"
BLACK = "\033[40m"

variables = {}
functions = {}

def math(arg):
    try:
        arg = str(arg)

        finmul = 0
        findiv = 0
        final = 0

        for name,value in variables.items():
            arg = arg.replace(name, str(value))
        arg = arg.replace(" ", "")

        newarg = arg.replace("-","+-")
        main_block = newarg.split("+")

        values = []

        for block in main_block:
            if not block.strip():
                continue

            if "*" in block:
                factors = block.split("*")
                finmul = 1

                for f in factors:
                    finmul *= float(f)

                values.append(finmul)
            elif "/" in block:
                factors = block.split("/")

                try:
                    findiv = float(factors[0])

                    for f in factors[1:]:
                        findiv /= float(f)

                    values.append(findiv)
                except ZeroDivisionError:
                    print(f"Cannot calculate: {arg} because it divides by 0")
                    return "ZeroDivisionException"
            else:
                values.append(float(block))

        final = sum(values)

        if final.is_integer():
            return int(final)

        return float(final)
    except Exception as e:
        print(f"Unknown error at math internal function: {e} ")
        return "NULL"



def Micron(run, i):
    try:
        if run.endswith(";"):

            nrun = run.split(";")
            for i in range(len(nrun)):
                Micron(nrun[i])
            return
        
        if not run or not run.strip():
            return

        if run.strip().startswith("//"):
            return
        elif run.strip().startswith("endif"):
            return

        # LEXER
        definition = False
        def_token = ""
        def_name_token = ""
        def_value_token = ""
        def_symbol = ""
        args_tokens = []
        args_type_tokens = []
        args_special = False
        args_special_main = ""
        args_special_value = ""
        func_token = ""
        
        if run.startswith("var:") or run.startswith("set:") or run.startswith("if:") or run.startswith("def:") or run.startswith("repeat:"):
            definition = True
        else:
            definition = False
        
        if definition:
            def_token = run[0:run.find(":")].strip()
            def_symbol = run[run.find("="):run.find("=")+2].strip()

            if def_symbol in ["==","=>","=<","=!"] and def_token == "if":
                expr = run[run.find(":")+1:].strip()

                for n,v in variables.items():
                    expr = expr.replace(n,str(v))

                expr = expr.replace("=>", ">=").replace("=<","<=").replace("=!","!=")

                if eval(expr):
                    return 
                else:
                    return "jumpto:end"
            elif def_symbol in ["==","=>","=<"] and not def_token in ["def","repeat"]:
                print("Syntax Error")
                return

            if def_symbol == "=f" and def_token == "def":
                def_symbol = run[run.find("="):run.find("=")+2].strip()
                def_name_token = run[run.find(":")+1:run.find("=")].strip()
                functions[def_name_token] = i + 1
                return "jumpto:end"
            elif def_symbol == "=f" and not def_token == "def":
                print("Syntax Error")
                return

            if def_symbol in ["==","=>","=<","=!"] and def_token == "repeat":
                expr = run[run.find(":")+1:].strip()

                for n,v in variables.items():
                    expr = expr.replace(n,str(v))

                expr = expr.replace("=>",">=").replace("=<","<=").replace("=!","!=")

                if not eval(expr):
                    functions['repeatmp'] = i
                    return "repeat"
                else:
                    if 'repeatmp' in functions: del functions['repeatmp']
                    return "jumpto:endrepeat"
            
            def_name_token = run[run.find(":")+1:run.find("=")].strip()
            def_value_token = run[run.find("=")+1:len(run)].strip()
        else:
            open_paren = run.find("(")
            close_paren = run.find(")")
            if open_paren == -1 or close_paren == -1 or close_paren < open_paren:
                return
            args_tokens = [token.strip() for token in run[open_paren+1:close_paren].split(",")]
            func_token = run[0:open_paren].strip()
        
        if definition:
            if def_value_token.startswith("'") and def_value_token.endswith("'"):
                def_value_type_token = "str"
            elif def_value_token.lower() == "true" or def_value_token.lower() == "false":
                def_value_type_token = "bool"
            elif any(op in def_value_token for op in ["+", "-", "*", "/"]):
                def_value_type_token = "eval"
            elif def_value_token.isdigit():
                def_value_type_token = "number"
            else:
                def_value_type_token = "variable"

        else:
            for token in args_tokens:
                if token.startswith("'") and token.endswith("'"):
                    args_type_tokens.append("str")
                elif token.lower() in ["true", "false"]:
                    args_type_tokens.append("bool")
                elif "+" in token or "-" in token or "*" in token or "/" in token:
                    args_type_tokens.append("eval")
                elif token.isdigit():
                    args_type_tokens.append("number")
                elif token.startswith("<") and token.endswith(">"):
                    indexmain = args_tokens.index(token)
                    args_type_tokens.append("special")
                    args_special = True
                    args_special_main = token[token.find("<")+1:token.find(":")]
                    args_special_value = token[token.find(":")+1:token.find(">")]
                    args_tokens.pop(indexmain)
                else:
                    args_type_tokens.append("variable")
        
        # PARSER
        if not definition:
            for i, token in enumerate(args_tokens):
                if args_type_tokens[i] == "variable":
                    if not token.strip() == "":
                        if any(c.isalpha() for c in token) and any(c.isdigit() for c in token) and token not in variables:
                            print(token + " has an incorrect format")
                            return
                        elif token not in variables:
                            print(token + " is not a variable")
                            return
        # this is not a AST LOL :-P
        if not definition:
            for i, token in enumerate(args_tokens):
                if args_type_tokens[i] == "variable":
                    args_tokens[i] = variables.get(token, "")
                elif args_type_tokens[i] == "eval":
                    args_tokens[i] = math(args_tokens[i])
                elif args_type_tokens[i] == "number":
                    args_tokens[i] = int(args_tokens[i])
                elif args_type_tokens[i] == "bool":
                    args_tokens[i] = token.lower() == "true"
                elif args_type_tokens[i] == "str":
                    args_tokens[i] = token[1:-1]

        # INTERPRETER
        if not definition:
            if func_token == "print":
                if args_special and args_special_main == "split":
                        print(*args_tokens, sep=args_special_value)
                elif not args_tokens:
                    print("There are no parameters")
                else:
                    print(*args_tokens)
            elif func_token == "version":
                print("Micron V1.1.2")
            elif func_token == "system":
                if args_tokens:
                    os.system(str(args_tokens[0]))
            elif func_token == "manual":
                print("╔═Manual════════════════════════════════════════════════════════════════╗")
                print("║ print(any) » Print any format at the terminal                         ║")
                print("║ version() » Print the interpreter version                             ║")
                print("║ system(str) » Run a command in the Windows console                    ║")
                print("║ manual() » Run this menu                                              ║")
                print("╚═══════════════════════════════════════════════════════════════════════╝")
            elif func_token == "clear":
                os.system("cls")
                os.system("color 1f")
                print("Micron Interpreter V1.1.1")
            elif func_token == "input": 
                if len(args_tokens) >= 1 and args_special_main == "out" and args_special:
                    data = input(args_tokens[0])
                    variables[args_special_value] = data
                elif args_special_main == "out":
                    print("input() doesnt have valid arguments")
                    return
            elif func_token == "power":
                if len(args_tokens) == 2 and args_special and args_special_main == "out":
                    base = args_tokens[0]
                    exponent = args_tokens[1]
                    result = base

                    while exponent != 0:
                        exponent -= 1
                        result = result*base

                    variables[args_special_value] = result
                else:
                    print("power() doesnt have valid arguments")
            elif func_token == "messagebox":
                messagebox.showinfo(args_tokens[0],args_tokens[1])
            elif func_token == "locals":
                print(variables)
            elif func_token == "localsf":
                print(functions)
            elif func_token == "exit":
                sys.exit(args_tokens[0])
            elif func_token == "printnon":
                if args_special and args_special_main == "split":
                        print(*args_tokens, sep=args_special_value, end="")
                elif not args_tokens:
                    print("There are no parameters")
                else:
                    print(*args_tokens)
            elif func_token == "exit":
                sys.exit(0)
            elif func_token in functions:
                return f"jumpline:{functions[func_token]}"
            else:
                print(func_token + " does not exist")

        else:
            if def_value_token.startswith("'") and def_value_token.endswith("'"):
                final = def_value_token[1:-1]
            elif def_value_token.isdigit():
                final = int(def_value_token)
            elif def_value_token.lower() == "true":
                final = True
            elif def_value_token.lower() == "false":
                final = False
            else:
                final = variables.get(def_value_token, def_value_token)

            if def_token == "var":
                if def_name_token not in variables:
                    variables[def_name_token] = final
                else:
                    print(def_name_token + " already exists")
            elif def_token == "set":
                if def_name_token not in variables:
                    print(def_name_token + " does not exist")
                    return
                else:
                    if def_value_type_token != "eval":
                        variables[def_name_token] = final
                    else:
                        variables[def_name_token] = math(def_value_token)
            else:
                print(def_token + " does not exist")
    except Exception as e:
        print(f"Unknown error: {e}")
        traceback.print_exc()

if len(sys.argv) > 1:
    try:

        if len(sys.argv) < 2:
            print("M i c r o n | Executor")
            print("Insert a file: 'py micron.py <filename.mscript>' or 'python micron.py <filename.mscript>'")

        importfile = sys.argv[1]

        if not os.path.exists(importfile):
            print(f"File not found: {importfile}")
        
        print(f"Loading: '{sys.argv[1]}'")
        print("-----------------------------------------------------------------------")
        with open(importfile, "r", encoding="utf8") as main:
            content = main.read().splitlines()

        i = 0
        while i != len(content):
            time.sleep(1)
            run_clean = content[i].strip()
            data = Micron(content[i],i) 
            print(data)

            if not run_clean:
                i += 1 
                continue

            if run_clean.startswith("repeat:"):
                i_loop = functions['repeatmp']

            if data == "jumpto:endif":
                while  i < len(content) and content[i].strip() != "endif":
                    i += 1 
                i += 1
                continue

            if data == "repeat":
                i_loop = functions['repeatmp']
            elif run_clean == "endrepeat":
                i = i_loop - 1
            elif data == "jumpto:endrepeat":
                while i < len(content) and content[i].strip() != "endrepeat":
                    i += 1
                i += 1
                continue

            if str(data).startswith("jumpline:"):
                i_ant = i
                i = int(data.strip().split(":")[1])
                continue
            elif run_clean == "end":
                if 'i_ant' in locals():
                    i = i_ant+1
                    del i_ant
                    continue
                else:
                    i += 1 
                    continue
            i += 1
            
    except PermissionError:
        print("The program is protected, cannot be executed.")
    except Exception as e:
        print(f"Unknown error: {e}")