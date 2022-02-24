# sokoban-solver
> Agent that solves Sokoban puzzle.

## Table of contents
* [General information](#general-information)
* [How to run?](#how-to-run)
* [Limitations](#limitations)
* [Inspiration](#inspiration)

## General information
This is a bot that was made to solve Sokoban puzzles on the website https://www.sokobanonline.com/. 

## How to run?

1. Clone this repository

2. Install dependencies (the code was written and tested on Python 3.10.0): 

```
pip3 install selenium chromedriver_autoinstaller pillow numpy
```

3. Open a terminal window in the root folder of the repository and enter the following:

```
python3 main.py
```

This will launch the solver with the default example. 

You can pass any other example from https://www.sokobanonline.com/play/web-archive/marti-homs-caussa/choriban/ through command line arguments.

Example: 

```
python3 main.py https://www.sokobanonline.com/play/web-archive/marti-homs-caussa/choriban/86887_choriban-20
```

## Limitations
(to be fixed)
- it works only when blocks are 64 x 64.
- it only uses BFS.

## Inspiration
- Dawid Dieu: AI Sokoban Solver Bot - https://github.com/TheFebrin/AI-sokoban-solver-bot
