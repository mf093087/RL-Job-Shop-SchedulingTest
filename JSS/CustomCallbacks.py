from typing import Dict
from ray.rllib.agents.callbacks import DefaultCallbacks
from ray.rllib.env import BaseEnv
from ray.rllib.evaluation import MultiAgentEpisode, RolloutWorker
from ray.rllib.policy import Policy
from ray.rllib.utils.typing import PolicyID
import numpy as np


class CustomCallbacks(DefaultCallbacks):

    def __init__(self, legacy_callbacks_dict: Dict[str, callable] = None):
        super(CustomCallbacks, self).__init__(legacy_callbacks_dict)

    def on_episode_start(
            self,
            *,
            worker: "RolloutWorker",
            base_env: BaseEnv,
            policies: Dict[str, Policy],
            episode: MultiAgentEpisode,
            env_index: int,
            **kwargs
    ):
        episode.user_data["mk_solution"] = float('inf')

    def on_episode_end(self, worker: "RolloutWorker", base_env: BaseEnv,
                       policies: Dict[PolicyID, Policy],
                       episode: MultiAgentEpisode, **kwargs):
        env = base_env.get_unwrapped()[0]
        if env.last_time_step != float('inf'):
            episode.custom_metrics['make_span'] = env.last_time_step
            if env.last_time_step < episode.user_data["mk_solution"]:
                episode.user_data["mk_solution"] = env.last_time_step
                with open('solution.npy', 'wb') as f:
                    np.save(f, env)