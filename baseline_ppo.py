import gymnasium as gym
from tqdm import tqdm 
import gymnasium as gym
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
import os
import gymnasium as gym
import matplotlib.pyplot as plt

from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.results_plotter import load_results, ts2xy
import pandas as pd 


log_dir = "./racing/logs/"
results_dir = "./racing/results/"

# Baseline CNN + PPO 
def baseline_env(): 

    os.makedirs(log_dir, exist_ok=True)

    vec_env = make_vec_env(
        "CarRacing-v3",
        monitor_dir=log_dir,
        n_envs=4, 
        env_kwargs={"continuous": False}
    )

    model = PPO(
        "CnnPolicy",
        vec_env,
        verbose=1,
        device="mps"
    )

    model.learn(total_timesteps=250_000)
    model.save("ppo_racing")
    vec_env.close()
    print("finished training")


# visualize the agent run after training 
def trained_agent_run():

    model = PPO.load("ppo_racing")

    eval_env = gym.make(
        "CarRacing-v3",
        continuous=False,
        render_mode="human"
    )

    obs, info = eval_env.reset()

    while True:
        action, _ = model.predict(obs, deterministic=True)
        obs, reward, terminated, truncated, info = eval_env.step(action)

        if terminated or truncated:
            break

    eval_env.close()


# plot training results 
def plot_baseline_stats(): 

    os.makedirs(results_dir, exist_ok=True)

    logs = load_results(log_dir)

    timesteps, rewards = ts2xy(logs, "timesteps")

    plt.figure(figsize=(12, 6))

    plt.plot(
        timesteps,
        rewards,
        alpha=0.3,
        label="Episode Reward"
    )


    plt.xlabel("Training Timesteps")
    plt.ylabel("Episode Reward")
    plt.title("PPO CarRacing Learning Curve")
    plt.legend()
    plt.grid()
    plt.savefig(f'{results_dir}/episode_reward.png')
    plt.show()
    




baseline_env()
plot_baseline_stats()
