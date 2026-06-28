# Micron Interpreter

This repository aims to showcase the source code of this improvised interpreter, written entirely in Python. Here, you can contribute ideas, code, and your opinions, which will help me develop this language into a more complex machine. The file <b>```micron.py```</b> contains all the main code and functions of the language (including a console where you can enter different commands and language functions).

## Base installation

This interpreter, despite being so simple, requires several basic prerequisites to run it at its maximum potential and fully enjoy it.

- The interpreter can be run on any version of Python later than 3.8 or that contains the ```os``` library.
- The interpreter necessarily needs to run on Windows because it uses the ```color``` command, which is native to Windows.

If you meet these requirements, you'll be able to get the most out of this interpreter and experiment with its features.

## Structure

The language is divided into different stages where the interpreter analyzes each part of a line of code to execute it accurately (This language does not have an AST as such):

- The lexer is responsible for splitting each line of code into two parts: the arguments and the function itself (```func_token``` and ```args_tokens```) for later use. If the function uses variables (i.e., ```var:``` or ```set:```), it divides the line into three parts (```def_token```, ```def_name_token```, and ```def_value_token```). Its second function is to assign a value or type to each piece of data in an argument to organize it and prevent a number from being passed as, for example, a string.
- The parser is responsible for verifying whether the entered variables are correct or if the arguments are empty (to avoid errors in other parts of the process). It returns errors if the syntax or the entered variables are incorrect.
- The AST again arranges and organizes the formats and types of each entered value to finally execute the entered functions.
- The interpreter executes all functions based on the parameters and all previously processed data, executing everything in a straightforward manner.

## Miscellaneous

In the ```examples``` folder, there's a README file where you'll find all the functions and how to program using this language. ```CONTRIBUTTING.md``` contains some rules for collaborating on or cloning the project.

I'll be adding more functions and tasks to the language soon. Stay tuned!
