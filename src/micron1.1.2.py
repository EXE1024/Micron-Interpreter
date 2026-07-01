import os
import sys

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

DEBUG = os.getenv("DEBUG", "1") == "1"

variables = {}

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

def Micron(run):
    try:

        if DEBUG:
            print(f"[RASTREO] -> Función Micron recibió la línea: '{run}'")

        if run.endswith(";"):

            nrun = run.split(";")
            for i in range(len(nrun)):
                Micron(nrun[i])
            return
        
        if not run or not run.strip():
            if DEBUG: print("[RASTREO] -> Línea vacía descartada.")
            return

        if run.strip().startswith("//"):
            if DEBUG: print("[RASTREO] -> Comentario detectado y descartado.")
            return

        # LEXER
        definition = False
        def_token = ""
        def_name_token = ""
        def_value_token = ""
        args_tokens = []
        args_type_tokens = []
        args_special = False
        args_special_main = ""
        args_special_value = ""
        func_token = ""
        
        if run.find(":") != -1 and run.find("=") != -1 and run.find("(") == -1 and run.find(")") == -1:
            definition = True
        elif run.find("(") != -1 and run.find(")") != -1:
            definition = False
        else:
            print("Syntax problem")
            if DEBUG: print("[RASTREO] -> La línea NO encajó como definición ni como función. Descartada por el Lexer.")
            return
        
        if definition:
            def_token = run[0:run.find(":")].strip()
            def_name_token = run[run.find(":")+1:run.find("=")].strip()
            def_value_token = run[run.find("=")+1:len(run)].strip()
            if DEBUG: print(f"[RASTREO] -> Lexer (Definición): token='{def_token}', variable='{def_name_token}', valor='{def_value_token}'")
        else:
            open_paren = run.find("(")
            close_paren = run.find(")")
            if open_paren == -1 or close_paren == -1 or close_paren < open_paren:
                if DEBUG: print("[RASTREO] -> Paréntesis inválidos en función.")
                return
            args_tokens = [token.strip() for token in run[open_paren+1:close_paren].split(",")]
            func_token = run[0:open_paren].strip()
            if DEBUG: print(f"[RASTREO] -> Lexer (Función): función='{func_token}', argumentos={args_tokens}")
        
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
            if DEBUG: print(f"[RASTREO] -> Tipo de valor detectado: {def_value_type_token}")
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
                    print(f"[RASTREO] -> Argumento especial: {token}")
                    args_special = True
                    args_special_main = token[token.find("<")+1:token.find(":")]
                    print(f"[RASTREO] -> Argumento especial, Nombre:{args_special_main}")
                    args_special_value = token[token.find(":")+1:token.find(">")]
                    print(f"[RASTREO] -> Argumento especial, Nombre:{args_special_value}")
                    print(f"[RASTREO] -> Argumento especial, Etiqueta: {args_special_main}, Valor: {args_special_value}")
                    args_tokens.pop(indexmain)
                else:
                    args_type_tokens.append("variable")
            if DEBUG: print(f"[RASTREO] -> Tipos de argumentos detectados: {args_type_tokens}")
        
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
        # AST
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
            if DEBUG: print(f"[RASTREO] -> Argumentos procesados por AST listos para ejecutar: {args_tokens}")

        # INTERPRETER
        if not definition:
            if DEBUG: print(f"[RASTREO] -> Intentando ejecutar función: '{func_token}'")
            if func_token == "print":
                if args_special == True and args_special_main == "split":
                        print("[RASTREO]: Argumento especial detectado en la funcion 'print'")
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
            else:
                print(func_token + " does not exist")
        else:
            if def_value_token.startswith("'") and def_value_token.endswith("'"):
                valor_final = def_value_token[1:-1]
            elif def_value_token.isdigit():
                valor_final = int(def_value_token)
            elif def_value_token.lower() == "true":
                valor_final = True
            elif def_value_token.lower() == "false":
                valor_final = False
            else:
                valor_final = variables.get(def_value_token, def_value_token)

            if def_token == "var":
                if def_name_token not in variables:
                    variables[def_name_token] = valor_final
                    if DEBUG: print(f"[RASTREO] -> Guardada variable '{def_name_token}' con valor: '{valor_final}'")
                else:
                    print(def_name_token + " already exists")
            elif def_token == "set":
                if def_name_token not in variables:
                    print(def_name_token + " does not exist")
                    return
                else:
                    if def_value_type_token != "eval":
                        variables[def_name_token] = valor_final
                        if DEBUG: print(f"[RASTREO] -> Actualizada variable '{def_name_token}' con valor: '{valor_final}'")
                    else:
                        variables[def_name_token] = math(def_value_token)
            else:
                print(def_token + " does not exist")
    except Exception as e:
        print(f"Unknown error: {e}")

open(".tmp\\sync.tmp", "w").close()

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
        if DEBUG:
            print(f"[RASTREO 1] -> Archivo abierto con éxito. Líneas leídas: {len(content)}")
            print(f"[RASTREO 1] -> Contenido crudo leído: {content}")

        for line in content:
            line_cleaned = line.strip()
            if line_cleaned and not line_cleaned.startswith("//"):
                Micron(line_cleaned)


    except PermissionError:
        print("The program is protected, cannot be executed.")
    except Exception as e:
        print(f"Unknown error: {e}")
