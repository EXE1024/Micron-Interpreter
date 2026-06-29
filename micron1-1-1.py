import os
import sys

# ╔══════════════════════════════════════╗
# ║ ▒█▀▄▀█ ▀█▀ ▒█▀▀█ ▒█▀▀█ ▒█▀▀▀█ ▒█▄░▒█ ║
# ║ ▒█▒█▒█ ▒█░ ▒█░░░ ▒█▄▄▀ ▒█░░▒█ ▒█▒█▒█ ║
# ║ ▒█░░▒█ ▄█▄ ▒█▄▄█ ▒█░▒█ ▒█▄▄▄█ ▒█░░▀█ ║
# ╚══════════════════════════════════════╝
#                1.1.1

DEBUG = False

variables = {}


def Micron(run):
    try:
        if DEBUG:
            print(f"[RASTREO] -> Función Micron recibió la línea: '{run}'")

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
                elif any(op in token for op in ["+", "-", "*", "/"]):
                    args_type_tokens.append("eval")
                elif token.isdigit():
                    args_type_tokens.append("number")
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
                    args_tokens[i] = eval(args_tokens[i])
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
                if len(args_tokens) > 0:
                    print(args_tokens[0])
            elif func_token == "version":
                print("Micron V1.1")
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
            elif func_token == "py":
                exec(args_tokens[0])
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
                    variables[def_name_token] = valor_final
                    if DEBUG: print(f"[RASTREO] -> Actualizada variable '{def_name_token}' con valor: '{valor_final}'")
            elif def_token == "add":
                if def_name_token not in variables:
                    print(def_name_token + " does not exist")
                    return
                else:
                    try:
                        variables[def_name_token] = variables[def_name_token] + int(def_value_token)
                        if DEBUG: print(f"[RASTREO] -> Actualizada variable '{def_name_token}' con valor: '{valor_final}'")
                    except ValueError:
                        print("You cannot add a number to a string")
            elif def_token == "sub":
                if def_name_token not in variables:
                    print(def_name_token + " does not exist")
                    return
                else:
                    try:
                        variables[def_name_token] = variables[def_name_token] - int(def_value_token)
                        if DEBUG: print(f"[RASTREO] -> Actualizada variable '{def_name_token}' con valor: '{valor_final}'")
                    except ValueError:
                        print("You cannot subtract a number from a string")
            elif def_token == "mul":
                if def_name_token not in variables:
                    print(def_name_token + " does not exist")
                    return
                else:
                    try:
                        variables[def_name_token] = variables[def_name_token] * int(def_value_token)
                        if DEBUG: print(f"[RASTREO] -> Actualizada variable '{def_name_token}' con valor: '{valor_final}'")
                    except ValueError:
                        print("You cannot multiply a number by a string")
            elif def_token == "div":
                if def_name_token not in variables:
                    print(def_name_token + " does not exist")
                    return
                else:
                    try:
                        try:
                            variables[def_name_token] = variables[def_name_token] / int(def_value_token)
                            if DEBUG: print(f"[RASTREO] -> Actualizada variable '{def_name_token}' con valor: '{valor_final}'")
                        except ValueError:
                            print("You cannot divide a number into a string")
                    except ZeroDivisionError:
                        print(f"'{variables[def_name_token]}'/'{def_value_token}': Zero division error")
                        variables[def_name_token] = 0
                        return
            else:
                print(def_token + " does not exist")
    except Exception as e:
        print(f"Unknown error: {e}")
                    
if len(sys.argv) > 1:
    importfile = sys.argv[1]
    print(f"Loading: '{sys.argv[1]}'")
    print("-----------------------------------------------------------------------")

    try:
        with open(importfile, "r", encoding="utf8") as main:
            content = main.read().splitlines()
        if DEBUG:
            print(f"[RASTREO 1] -> Archivo abierto con éxito. Líneas leídas: {len(content)}")
            print(f"[RASTREO 1] -> Contenido crudo leído: {content}")
    except FileNotFoundError:
        print(f"File not found: {importfile}")

    for line in content:
        line_cleaned = line.strip()
        if line_cleaned and not line_cleaned.startswith("//"):
            Micron(line_cleaned)
    sys.exit()

os.system("color 1f")

if __name__ == "__main__":
    print("Micron Interpreter V1.1.1")
    while True:
        run = input("> ").strip()
        if run.lower() == "exit":
            break

        if run.lower().startswith("import "):
            importfile = run[7:].strip().strip("'\"")
            if DEBUG: print(f"[RASTREO 1] -> Detectado comando 'import'. Buscando archivo en ruta: '{importfile}'")

            if not importfile:
                print("There are no parameters")
                continue

            try:
                with open(importfile, "r", encoding="utf8") as main:
                    content = main.read().splitlines()
                if DEBUG:
                    print(f"[RASTREO 1] -> Archivo abierto con éxito. Líneas leídas: {len(content)}")
                    print(f"[RASTREO 1] -> Contenido crudo leído: {content}")
            except FileNotFoundError:
                print(f"File not found: {importfile}")
                continue

            for line in content:
                line_cleaned = line.strip()
                if line_cleaned and not line_cleaned.startswith("//"):
                    Micron(line_cleaned)

            variables = {}
        Micron(run)
