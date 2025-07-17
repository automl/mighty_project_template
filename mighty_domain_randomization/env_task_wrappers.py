"""Task wrapper that can select a new MiniGrid task on reset."""

from __future__ import annotations

from copy import deepcopy

import gymnasium as gym
import numpy as np
from syllabus.core import TaskWrapper
from syllabus.task_space import DiscreteTaskSpace


class VecMinigridTaskWrapper(TaskWrapper):
    """This wrapper allows you to change the task of a vectorized MiniGrid env."""

    def __init__(self, env: gym.Env):
        """Initialize the VecMinigridTaskWrapper ans set up single env spaces."""
        super().__init__(env)

        # Get the single observation space
        self.single_observation_space, self.observation_space, self.out_shape = (
            self.get_image_observation_space()
        )

        # Set up task space
        self.task_space = DiscreteTaskSpace(200)
        self.task = np.zeros(len(self.env.envs), dtype=np.int32)
        self.reset_kwargs = {}

    def change_task(self, new_task, change_positions):
        """Reset selected environments with a new task."""
        for i, pos in enumerate(change_positions):
            seed = int(new_task[i])
            self.task[pos] = seed
            self.envs[pos].reset(seed=seed, **self.reset_kwargs)

    def reset(self, new_task=None, **kwargs):
        """Resets the environment and optionally sets a new task globally."""
        # Change task if new one is provided
        self.reset_kwargs = kwargs.copy()
        if "seed" in self.reset_kwargs:
            del self.reset_kwargs["seed"]
        if new_task is not None:
            kwargs["seed"] = int(new_task)

        self.episode_return = 0
        obs, infos = self.env.reset(**kwargs)
        return self.flatten_obs(obs["image"]), infos

    def get_task(self):
        """Get the current task for each environment."""
        return self.task

    def step(self, action):
        """Step through environment and update task completion."""
        obs, rew, term, trunc, info = self.env.step(action)
        obs = self.flatten_obs(obs["image"])

        self.episode_return += rew
        info["task_completion"] = self._task_completion(obs, rew, False, False, info)  # noqa: FBT003

        return obs, rew, term, trunc, info

    def flatten_obs(self, observations):
        """Utility function to flatten the observations."""
        return deepcopy(
            np.stack(
                (
                    tuple(
                        gym.spaces.flatten(self.single_observation_space, obs)
                        for obs in iter(observations)
                    )
                ),
                axis=0,
                out=self.out_shape,
            )
        )

    def get_image_observation_space(self):
        """Get the image only observation spaces from full space."""
        single_observation_space = gym.spaces.flatten_space(
            self.env.single_observation_space.spaces["image"]
        )
        repeats = tuple(
            [len(self.env.envs)] + [1] * single_observation_space.low.ndim
        )
        low, high = (
            np.tile(single_observation_space.low, repeats),
            np.tile(single_observation_space.high, repeats),
        )
        observation_space = gym.spaces.Box(
            low=low,
            high=high,
            dtype=single_observation_space.dtype,
            seed=deepcopy(single_observation_space.np_random),
        )
        out_shape = np.zeros(
            (len(self.env.envs), *single_observation_space.shape),
            dtype=single_observation_space.dtype,
        )
        return single_observation_space, observation_space, out_shape
