# PROGRAMMING

## How to execute something
- <b>1. Files</b>: Using the command ```import [filepath]``` you can open and execute the contents of files (Example: ```import examples\variables.mscript```)
- <b>2.Interpreter (Direct)</b>: Type direct code into the console and press ENTER to execute the code
- <b>3.CMD</b>: Open PowerShell and enter this command to launch a file from the Windows console: <b>```py micron1-1-1.py [filepath]```</b> or <b>```python micron1-1-1.py [filepath]```</b>
## Code

Run the default functions in the interpreter by writing to a file or in the terminal (Recommended: It is better to use files since you can run long codes or test several functions at once):

- <b>```print(any)```</b>: Prints text or any type of value to the console
- <b>```system(str)```</b>: Executes a command in the native Windows console
- <b>```manual()```</b>: Opens a basic manual covering all the basic functions
- <b>```version()```</b>: Displays the interpreter version on the
- <b>```clear()```</b>: Delete all text in the console
- <b>```py()```</b><u>[UNSTABLE]</u>: Execute Python code using the exec function

### Variables

Variables are created and modified without using functions directly. Therefore, they are slightly different:

- <b>```var: [name] = [value]```</b>: Creates a variable with a base value
- <b>```set: [name] = [newvalue]```</b>: Modifies the value of a variable to a new one
- <b>```add: [name] = [adding]```</b>: Add the income value to the original value of the variable
- <b>```sub: [name] = [subtrahend]```</b>: Subtract the income value from the original value of the variable
- <b>```mul: [name] = [multiplier]```</b>: Multiply the income value by the original value of the variable
- <b>```div: [name] = [divisor]```</b>: Divide the entered value by the original value of the variable

Variables are stored in a dictionary, so technically and at the code level they look like this: {name:value}. These variables can be called by putting their name in the arguments of a function, for example: print(myvar). If they don't exist, an error will be thrown.

## Miscellaneous

The current version of Micron is 1.1.1; sometimes this README will not be updated to the latest version.
