# accept an agent action → advance simulation → return observation, reward, and termination status.

import gymnasium as gym
from game import Game


class RacingEnvironment(gym.Env):

    def __init__(self):
        super().__init__()
        self.game = Game()

        # Define action_space and observation_space here
        # TODO: declare observation and reward here 

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        self.game.reset()

        observation = self.get_observation()

        return observation, {}

    def step(self, action):
        steering = action[0]
        acceleration = action[1]

        self.game.update(steering, acceleration, 0.1) # 0.1s increments 

        observation = self.get_observation()
        reward = self.calculate_reward()

        terminated = (
            self.game.crashed or self.game.finished
        )

        truncated = False

        return observation, reward, terminated, truncated, {}