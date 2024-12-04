import micropip
await micropip.install('dist/cpu-0.1.0-py3-none-any.whl')
from maze.game import Robot, draw_web
from maze.run_web import (
    stop_game, 
    run_game, 
    context, 
    canvas,
    delay,
    cpu,
    simulation_task
)


robot = Robot(context=context, canvas=canvas)
draw_web(robot)


