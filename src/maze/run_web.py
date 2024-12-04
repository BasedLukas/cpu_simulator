import asyncio

import js
from pyodide.ffi import create_proxy

from assembler.assembler import assemble_binary
from hardware.cpu import CPU
from maze.game import maze, CELL_SIZE, Robot, draw_web


### GLOBALS ### (imported by pyodide and used by js)
canvas = js.document.getElementById("mazeCanvas")
context = canvas.getContext('2d')
canvas.width = len(maze[0]) * CELL_SIZE
canvas.height = len(maze) * CELL_SIZE
delay = 0.0001  # Speed of the animation
cpu = None,
robot = None,
simulation_task = None


def stop_game():
    global simulation_task, cpu, robot
    if simulation_task and not simulation_task.done():
        simulation_task.cancel()
    js.document.getElementById('output').innerText = 'Simulation stopped and reset.'
    # Redraw the initial state
    cpu = None
    robot = Robot(context=context, canvas=canvas)
    draw_web(robot)

async def run_game():
    global cpu, robot, simulation_task

    # Stop any existing simulation
    stop_game()

    # Get the assembly code from the textarea
    assembly_code = js.document.getElementById("assemblyCode").value

    # Assemble the code
    binary_code = assemble_binary(code_string=assembly_code)

    # Initialize CPU and Robot
    cpu = CPU(binary_code)
    robot = Robot(context=context, canvas=canvas)
    draw_web(robot)

    js.document.getElementById('output').innerText = 'Simulation running...'

    # Define the simulation loop
    async def simulation_loop():
        while cpu.pc < len(cpu.program):
            # Execute one CPU instruction
            cpu.exec(
                input_func=robot.get_front_cell_bit,
                output_func=robot.move
            )
            draw_web(robot)
            await asyncio.sleep(delay)
        js.document.getElementById('output').innerText = 'Simulation complete!'

    # Run the simulation loop
    simulation_task = asyncio.create_task(simulation_loop())


