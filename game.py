from car import Car

# abstract the game state so gymnasium can train on it 
# rewards and penalties 
class Game:
    def __init__(self):
        self.car = Car(400, 500) # init the car at the start position 
        self.crashed = False
        self.finished = False

    def update(self, steering, acceleration, dt):
        self.car.update(steering, acceleration, dt)

        # Later:
        # self.check_collisions()
        # self.update_progress()

    def reset(self):
        self.__init__()

    def check_collisions(): 
        # based on the current track, whether the car pixels overlap 
    
    def update_progress(): 
        # track has 