import importlib
import micropip
await micropip.install('dist/cpu-0.1.0-py3-none-any.whl')
from pyodide.ffi import create_proxy
import js

from maze.game import Robot, draw_web, maze, CELL_SIZE
from maze.run_web import (
    stop_game, 
    run_game,
)


solution_code = open(importlib.resources.files("maze") / "robot.asm").read()
canvas = js.document.getElementById("mazeCanvas")
context = canvas.getContext('2d')
canvas.width = len(maze[0]) * CELL_SIZE
canvas.height = len(maze) * CELL_SIZE
robot = Robot(context=context, canvas=canvas)
draw_web(robot)

def run_game_wrapper(param):
    callback = run_game(canvas, context)
    if callback: callback.add_done_callback(stop_game_wrapper)

def stop_game_wrapper(param):
    stop_game(canvas, context)

js.document.getElementById('runButton').addEventListener('click',create_proxy(run_game_wrapper))
js.document.getElementById('stopButton').addEventListener('click',create_proxy(stop_game_wrapper))



