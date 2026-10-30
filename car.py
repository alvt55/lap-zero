
import math

ACCEL_RATE = 1.0
MAX_SPEED = 20.0
MAX_STEERING = 0.15  # Maximum radians per update


class Car:
    def __init__(self, x, y, heading, speed=0):
        self.x = x
        self.y = y
        self.heading = heading  # Radians
        self.speed = speed

    def update(self, steering, acceleration, duration):
        # 1. Update speed
        self.speed += acceleration * ACCEL_RATE * duration

        # 2. Keep speed within valid limits
        self.speed = max(0, min(self.speed, MAX_SPEED))

        # 3. Update heading
        self.heading += steering * MAX_STEERING

        # Keep heading between -pi and pi
        self.heading = (self.heading + math.pi) % (2 * math.pi) - math.pi

        # 4. Calculate movement
        distance = self.speed * duration

        dx = distance * math.cos(self.heading)
        dy = distance * math.sin(self.heading)

        # 5. Update position
        self.x += dx
        self.y += dy

    def get_state(self):
        return {
            "x": round(self.x, 2),
            "y": round(self.y, 2),
            "heading": round(self.heading, 3),
            "speed": round(self.speed, 2)
        }



def main():
    # Create car at origin, facing right
    car = Car(x=0, y=0, heading=0)

    # Simulate 10 updates
    for step in range(10):
        # Example controls
        steering = 0.2 if step >= 5 else 0
        acceleration = 1.0

        car.update(
            steering=steering,
            acceleration=acceleration,
            duration=1.0
        )

        print(f"Step {step + 1}: {car.get_state()}")


if __name__ == "__main__":
    main()
