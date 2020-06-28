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
        self.way = 0
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
        path = self.car_pos[0] // 70 + 1
        for bcar in bluecar:
            if self.car_pos[1] > bcar[0][1] and self.car_pos[1] - bcar[0][1] < 100 + (self.car_vel - bcar[1])*20 and abs(self.car_pos[0] - bcar[0][0]) < 40:
                isBreak = True;
               # print(self.car_pos,bcar)
            if abs(self.car_pos[1] - bcar[0][1]) < 120:
                if (self.car_pos[0] - bcar[0][0] > 0 and self.car_pos[0] - bcar[0][0] < 75) or self.car_pos[0] < 35:
                    isLeft = False
                if (self.car_pos[0] - bcar[0][0] < 0 and self.car_pos[0] - bcar[0][0] > -75) or self.car_pos[0] > 595:
                    isRight = False
        coin_pos = [0,0,0]
        for coin in scene_info["coins"]:
            if self.car_pos[1] > coin[1]:
                if coin[0] <= path * 70 and coin[0] >= (path-1) * 70 and coin[1] > coin_pos[0]:
                    coin_pos[0] = coin[1]
                elif coin[0] >= (path-2) * 70 and coin[0] < (path-1) * 70 and coin[1] > coin_pos[1]:
                    coin_pos[1] = coin[1]
                elif coin[0] > path * 70 and coin[0] < (path+1) * 70 and coin[1] > coin_pos[2]:
                    coin_pos[2] = coin[1] 
        if self.player == "player1":
            print(self.player, coin_pos, isRight, isLeft, path)
        comm = []
        if scene_info["status"] != "ALIVE":
            return "RESET"
        if self.direction != -1:
            if self.way == 1 and self.direction > self.car_pos[0] and isRight:
                comm.append("MOVE_RIGHT")
            elif self.way == 2 and self.direction < self.car_pos[0] and isLeft:
                comm.append("MOVE_LEFT")
            else:
                self.direction = -1
                self.way = 0
        if (coin_pos[0] > 0 or coin_pos[1] > 0 or coin_pos[2] > 0) and self.way == 0:
            if coin_pos[2] > coin_pos[0] and coin_pos[2] >= coin_pos[1]:
                if isRight and self.car_pos[0] < 570:
                    self.direction = 70 * path + 35
                    self.way = 1
            if coin_pos[1] > coin_pos[0] and coin_pos[1] >= coin_pos[2]:
                if isLeft and self.car_pos[0] > 70:
                    self.direction = 70 * path - 105
                    self.way = 2
        if isBreak:
            if self.direction == -1:
                if isRight and self.car_pos[0] < 570:
                    if self.direction == -1:
                        self.direction = 70 * path + 35
                        self.way = 1
                    elif self.direction < self.car_pos[0]:
                        self.direction = self.direction + 140
                    return ["BRAKE", "MOVE_RIGHT"]
                elif isLeft and self.car_pos[0] > 70:
                    if self.direction == -1:
                        self.direction = 70 * path - 105
                        self.way = 2
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
