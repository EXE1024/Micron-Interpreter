# Micron Interpreter 1.1.2

![Micron](src/resources/micron_logo.png)

Micron is a lightweight interpreter written in Python that lets you run scripts and simple commands from the terminal or a visual environment. This repository contains the main interpreter implementation in [src/micron1.1.2.py](src/micron1.1.2.py) and the visual executor in [src/mev_executor.py](src/mev_executor.py).

## Features

Micron includes a small set of built-in commands and language features:

- `print(any)`: prints text or any supported value to the console
- `system(str)`: runs a command in the native Windows console
- `manual()`: opens a basic manual for the language
- `version()`: displays the current interpreter version
- `clear()`: clears the console output

## Variables

Variables are created and updated without calling a function directly:

- `var: name = value`: creates a variable with an initial value
- `set: name = newvalue`: updates an existing variable

Variables are stored in a dictionary and can be used inside functions such as `print(myvar)`.

## Arithmetic support

Arithmetic expressions can be handled through the `math(arg)` function, making it easier to perform calculations inside variables or commands.

## How to run

From the project root, launch a script with:

- `py micron1.1.2.py [filepath]`
- `python micron1.1.2.py [filepath]`

You can also type commands directly into the interpreter for quick testing.

## Example

```text
var: x = 10
set: x = x + 5
print(x)
```

## MVE: Micron Visual Environment

Micron also includes a visual executor built with `tkinter`. It launches the interpreter as a child process, provides a graphical console, and helps you run scripts in a more visual workflow.

## Requirements

- OS: Windows
- Python version: 3.12
- Libraries: `os`, `pathlib`, `tkinter`, `subprocess`, `time`, `sys`

## Contributing

Ideas, code contributions, and feedback are welcome. Feel free to experiment with the interpreter and share your improvements.

## Notes

The current version of Micron is 1.1.2, and some documentation may lag behind the latest updates.
