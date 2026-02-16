import sys
import os

# Ensure the root directory is in sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from rl_agent.environment import NetworkDefenseEnv
from rl_agent.agent_model import RLAgent
import gymnasium as gym

def main():
    print("Initializing Environment...")
    env = NetworkDefenseEnv(num_nodes=20)
    
    print("Creating Agent...")
    agent = RLAgent(env, algo='PPO', model_path="rl_agent/models/ppo_agent_v1")
    
    print("Starting Training...")
    agent.train(total_timesteps=20000)
    
    print("Saving Model...")
    agent.save()
    
    print("Evaluating...")
    obs, _ = env.reset()
    total_reward = 0
    done = False
    
    steps = 0
    while not done and steps < 100:
        action, _states = agent.model.predict(obs)
        obs, reward, terminated, truncated, info = env.step(action)
        total_reward += reward
        done = terminated or truncated
        steps += 1
        
    print(f"Total Reward over 100 steps: {total_reward}")

if __name__ == "__main__":
    main()
