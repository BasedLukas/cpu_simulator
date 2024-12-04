import asyncio

import js
from pyodide.ffi import create_proxy

from assembler.assembler import assemble_binary
from hardware.cpu import CPU
from maze.game import maze, CELL_SIZE, Robot, draw_web


### GLOBALS ### (imported by pyodide and used by js)

cpu = None,
robot = None,



def stop_game(canvas, context):
    global cpu, robot
    js.document.getElementById('output').innerText = 'Simulation stopped.'
    # Redraw the initial state
    cpu = None
    robot = Robot(context=context, canvas=canvas)
    draw_web(robot)


def run_game(canvas, context):
    global cpu, robot
    js.document.getElementById('errorOutput').innerText = ""
    js.document.getElementById('output').innerText = 'Simulation running...'
    assembly_code = js.document.getElementById("assemblyCode").value
    try:
        binary_code = assemble_binary(code_string=assembly_code)
        print(binary_code)
    except Exception as e:
        js.document.getElementById('errorOutput').innerText = f"Assembly Error: {str(e)}"
        js.document.getElementById('output').innerText = "Simulation complete!"
        return 
    # Initialize CPU and Robot
    cpu = CPU(binary_code)
    robot = Robot(context=context, canvas=canvas)
    draw_web(robot)

    # Define the simulation loop
    async def simulation_loop():
        while cpu.pc < len(cpu.program):
            cpu.exec(
                input_func=robot.get_front_cell_bit,
                output_func=robot.move
            )
            draw_web(robot)
            await asyncio.sleep(float(js.document.getElementById("delay").value))

    # Run the simulation loop
    return asyncio.create_task(simulation_loop())
    

  


