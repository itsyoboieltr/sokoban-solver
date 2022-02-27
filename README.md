# sokoban-solver

> Agent that solves Sokoban puzzle.

## Table of contents

- [General information](#general-information)
- [How to run?](#how-to-run)
- [Limitations](#limitations)
- [Inspiration](#inspiration)

## General information

This is a bot that was made to solve Sokoban puzzles on the website https://www.sokobanonline.com/.

<img width="450" src="https://i.imgur.com/G1hK0SL.gif">

## How to run?

1. Clone this repository

2. Install dependencies (the code was written and tested on Python 3.10.0):

```
pip3 install selenium chromedriver_autoinstaller pillow numpy yaspin
```

3. Open a terminal window in the root folder of the repository and enter the following:

```
python3 main.py
```

This will launch the solver with the default search method (BFS) and the default example (Choriban #20).

Command line arguments:

python3 main.py <search_method> <map_url>

Search methods supported:

- Breadth-first search: bfs
- Depth-first search: dfs
- A\* search: a_star

Map url:

You can pass any (with limitations explained later) map from https://www.sokobanonline.com/play/web-archive/marti-homs-caussa/choriban/ as the last command line argument.

Example:

```
python3 main.py a_star https://www.sokobanonline.com/play/web-archive/marti-homs-caussa/choriban/86890_choriban-24
```

## Limitations

(to be fixed)

- it works only when blocks are 64 x 64.

## Inspiration

- Dawid Dieu: AI Sokoban Solver Bot - https://github.com/TheFebrin/AI-sokoban-solver-bot
