import gymnasium as gym
from tqdm import tqdm 

# create env 
env = gym.make("CarRacing-v3", render_mode="human", lap_complete_percent=0.2, domain_randomize=False, continuous=False)

# action space and observation space 
print(f"Action space: {env.action_space}")   # discrete 0-5 per action 
print(f"Observation space: {env.observation_space}") # value of 0 to 255, for 96x96 pixels 

# new episode 
observation, info = env.reset()
print(f"Sample action: {env.action_space.sample()}")  
print(f"Sample observation: {env.observation_space.sample()}") 


'''
From the docs: 
The reward is -0.1 every frame and +1000/N for every track tile visited, 
where N is the total number of tiles visited in the track. 
For example, if you have finished in 732 frames, your reward is 1000 - 0.1*732 = 926.8 points.
'''
episode_over = False
total_reward = 0 

while not episode_over:
    action = env.action_space.sample()  

    observation, reward, terminated, truncated, info = env.step(action)

    total_reward += reward
    episode_over = terminated or truncated

print(f"Episode finished! Total reward: {total_reward}")
env.close()


