# Minesweeper &emsp;&emsp;&emsp; [![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-349bff.svg)](https://www.gnu.org/licenses/gpl-3.0)  [![Python 3](https://img.shields.io/badge/Python-100%25-brightgreen.svg)]()

Classic game developed in Python just for fun.



## Usage

### Basic GUI (10x10, 16 mines)

- Run the interface.py file in terminal or double click on it
> **Note**: &emsp; [Kivy library](https://kivy.org/#home) is required
- The game window will open
  - **Blue tiles**: covered, left click to expose, right click to mark
  - **Orange tiles**: marked, right click to remove the flag
  - **Numbered tiles**: indicate the number of bombs in the neighborhood
  - **Red crossed tiles**: if you see one, you've lost
- Enjoy!
  - Customizable grid size coming soon

### Command line

- Open a new terminal
- Run the game by typing	`python cli.py [rows] [cols] [bombs]`	, where:
  - **rows**:	number of rows in the field
  - **cols**:  	number of columns in the field
  - **bombs**:    number of bombs to be put
- Commands are inserted through the	 `Action: ` 	prompt
  - `E [row] [col]`	exposes the inserted tile (starting from 0)
  - `M [row] [col]`	marks the selected tile
  - `q` or `quit` or `exit` to close the game at any moment
- Have fun?
  - Difficult with that interface, check out the GUI instead!



## Features

- Basic GUI
  - Fixed size field and bomb number
  - Awesome to play

- Command line interface
  - Customizable field size and bomb number
  - Nasty and painful, good for debugging



## Coming soon

- Custom games in the Kivy GUI
- Winner Winner Sweeper Dinner
- Any suggestions?

