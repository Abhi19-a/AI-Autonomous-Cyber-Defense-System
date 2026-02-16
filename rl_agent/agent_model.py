from stable_baselines3 import PPO, DQN
from stable_baselines3.common.env_util import make_vec_env
import os

class RLAgent:
    def __init__(self, env, algo='PPO', model_path="models/ppo_cyber_defense"):
        self.env = env
        self.algo = algo
        self.model_path = model_path
        self.model = None

    def train(self, total_timesteps=10000):
        if self.algo == 'PPO':
            self.model = PPO("MlpPolicy", self.env, verbose=1)
        elif self.algo == 'DQN':
            self.model = DQN("MlpPolicy", self.env, verbose=1)
        
        print(f"Training {self.algo} agent for {total_timesteps} steps...")
        self.model.learn(total_timesteps=total_timesteps)
        print("Training complete.")

    def save(self):
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        self.model.save(self.model_path)
        print(f"Model saved to {self.model_path}")

    def load(self):
        if self.algo == 'PPO':
            self.model = PPO.load(self.model_path)
        elif self.algo == 'DQN':
            self.model = DQN.load(self.model_path)
        print(f"Model loaded from {self.model_path}")

    def predict(self, observation):
        action, _states = self.model.predict(observation)
        return action
