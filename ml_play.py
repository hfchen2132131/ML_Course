import math

class MLPlay:
    def __init__(self, player):
        self.player = player
        if self.player == "player1":
            self.player_no = 0
        elif self.player == "player2":
            self.player_no = 1
        elif self.player == "player3":
            self.player_no = 2
        elif self.player == "player4":
            self.player_no = 3
        self.car_vel = 0
        self.car_pos = ()
        self.direction = -1;
        pass

    def update(self, scene_info):
        """
        Generate the command according to the received scene information
        """
        bluecar = [];
        self.car_pos = scene_info[self.player]
        isBreak = False
        isRight = True
        isLeft = True
        for car in scene_info["cars_info"]:
            
            if car["id"]==self.player_no:
                self.car_vel = car["velocity"]
            else:
                bluecar.append([car["pos"],car["velocity"]])

        if len(self.car_pos) == 0:
            return []
        for bcar in bluecar:
            if self.car_pos[1] > bcar[0][1] and self.car_pos[1] - bcar[0][1] < 100 + (self.car_vel - bcar[1])*20 and abs(self.car_pos[0] - bcar[0][0]) < 40:
                isBreak = True;
               # print(self.car_pos,bcar)
            if abs(self.car_pos[1] - bcar[0][1]) < 120:
                if self.car_pos[0] - bcar[0][0] > 0 and self.car_pos[0] - bcar[0][0] < 71:
                    isLeft = False
                if self.car_pos[0] - bcar[0][0] < 0 and self.car_pos[0] - bcar[0][0] > -71:
                    isRight = False
        comm = []
        if scene_info["status"] != "ALIVE":
            return "RESET"
        if self.direction != -1:
            if self.direction > self.car_pos[0] and isRight:
                comm.append("MOVE_RIGHT")
            elif self.direction < self.car_pos[0] and isLeft:
                comm.append("MOVE_LEFT")
            else:
                self.direction = -1
        if isBreak:
            if self.direction == -1:
                if isRight and self.car_pos[0] < 570:
                    if self.direction == -1:
                        self.direction = self.car_pos[0] + 70
                    elif self.direction < self.car_pos[0]:
                        self.direction = self.direction + 140
                    return ["BRAKE", "MOVE_RIGHT"]
                elif isLeft and self.car_pos[0] > 70:
                    if self.direction == -1:
                        self.direction = self.car_pos[0] - 70
                    elif self.direction > self.car_pos[0]:
                        self.direction = self.direction - 140
                    return ["BRAKE", "MOVE_LEFT"]
                else:
                    comm.append("BRAKE")
                return comm
            else:
                comm.append("BRAKE")
                return comm
        else:
            comm.append("SPEED")
            return comm


    def reset(self):
        """
        Reset the status
        """
        pass
