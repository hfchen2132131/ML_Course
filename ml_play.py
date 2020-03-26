"""
The template of the main script of the machine learning process
"""

import games.arkanoid.communication as comm
from games.arkanoid.communication import ( \
    SceneInfo, GameStatus, PlatformAction
)

def ml_loop():
    """
    The main loop of the machine learning process

    This loop is run in a separate process, and communicates with the game process.

    Note that the game process won't wait for the ml process to generate the
    GameInstruction. It is possible that the frame of the GameInstruction
    is behind of the current frame in the game process. Try to decrease the fps
    to avoid this situation.
    """

    # === Here is the execution order of the loop === #
    # 1. Put the initialization code here.
    ball_served = False
    pre_ball_posi = (0,0)

    # 2. Inform the game process that ml process is ready before start the loop.
    comm.ml_ready()

    # 3. Start an endless loop.
    while True:
        # 3.1. Receive the scene information sent from the game process.
        scene_info = comm.get_scene_info()
        isDrop = False
        # 3.2. If the game is over or passed, the game process will reset
        #      the scene and wait for ml process doing resetting job.
        if scene_info.status == GameStatus.GAME_OVER or \
            scene_info.status == GameStatus.GAME_PASS:
            # Do some stuff if needed
            ball_served = False
            pre_ball_posi = (0,0)

            # 3.2.1. Inform the game process that ml process is ready
            comm.ml_ready()
            continue

        # 3.3. Put the code here to handle the scene information
        delta = (scene_info.ball[0] - pre_ball_posi[0] , scene_info.ball[1] - pre_ball_posi[1])
        drop = 0
        if delta[1] > 0:
            isDrop = True
           # drop = scene_info.ball[0] + delta[0] * (400 - scene_info.ball[1]) / delta[1]
            drop = int(drop)
            drop = drop - (drop % 5)
                
            if drop > 275 or drop < -75:
                isDrop = False
        # 3.4. Send the instruction for this frame to the game process
        if not ball_served:
            comm.send_instruction(scene_info.frame, PlatformAction.SERVE_TO_LEFT)
            ball_served = True
        else:
            if isDrop:
                if drop > scene_info.platform[0] + 20:
                    comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
                elif drop < scene_info.platform[0] + 20:
                    comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
            else:
                if 100 > scene_info.platform[0] + 20:
                    comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
                elif 100 < scene_info.platform[0] + 20:
                    comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
        pre_ball_posi = scene_info.ball
