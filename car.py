import math

# car's state 
# given some new inputs and the existing state, returns its new state
class Car:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        # Direction the car is facing (radians)
        self.heading = math.pi

        # Current speed
        self.speed = 0


        # constants 
        self.max_speed = 250
        self.acceleration_rate = 220
        self.brake_rate = 350
        self.friction = 100
        self.turn_rate = 2.5

    # dt is time to perform this action
    def update(self, steering, acceleration, dt):
        # Update speed
        if acceleration > 0:
            self.speed += self.acceleration_rate * dt
        elif acceleration < 0:
            self.speed -= self.brake_rate * dt
        else:
            # Gradually slow down when no key is pressed
            self.speed -= self.friction * dt

        self.speed = max(0, min(self.speed, self.max_speed))

        # Update heading
        # Steering becomes more effective as the car speeds up
        speed_factor = min(self.speed / 100, 1)

        self.heading += (
            steering * self.turn_rate * speed_factor * dt
        )

        # Update position
        self.x += self.speed * math.cos(self.heading) * dt
        self.y += self.speed * math.sin(self.heading) * dt