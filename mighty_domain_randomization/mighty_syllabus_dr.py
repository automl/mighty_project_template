"""Mighty Meta Component for Domain Randomization using Syllabus."""

from __future__ import annotations

import numpy as np
from mighty.mighty_meta.mighty_component import MightyMetaComponent
from omegaconf import OmegaConf
from syllabus.curricula import BatchedDomainRandomization


class MightySyllabusDR(MightyMetaComponent):
    """Cosine LR Schedule with optional warm restarts."""

    def __init__(
        self,
        curriculum_config,
    ) -> None:
        """Domain Randomization component for Mighty using Syllabus.

        :param curriculum_config: Configuration for the curriculum.
        """
        super().__init__()
        self.curriculum = None
        self.curriculum_config = curriculum_config

        # Initialize methods for the curriculum
        # This is only done once at the very beginning
        self.pre_step_methods = [self.init]

        # Change task on reset and update curriculum after each episode
        self.pre_episode_methods = [self.change_task_on_reset]
        self.post_episode_methods = [self.batch_dr_update]

    def make_curriculum(self, env, curriculum_config):
        """Create a curriculum from the given config."""
        # Make sure the kwargs are a dictionary
        curriculum_kwargs = curriculum_config.get("curriculum_kwargs", {})
        curriculum_kwargs = OmegaConf.to_container(curriculum_kwargs, resolve=True)

        # Make curriculum
        self.curriculum = BatchedDomainRandomization(
            task_space=env.task_space, **curriculum_kwargs
        )

    def change_task_on_reset(self, metrics):
        """Change the task when the environment resets."""
        if "transition" in metrics:
            # We reset only the tasks that need a reset
            reset_at = np.where(metrics["transition"]["dones"])[0]
        else:
            # If there aren't any transitions in the metrics yet, we reset everything
            reset_at = np.arange(len(metrics["env"].envs))

        # Get curriculum tasks
        next_task = self.curriculum.sample(k=len(reset_at))

        # Change the task in the environment
        metrics["env"].change_task(next_task, reset_at)
        metrics["instance"] = next_task

    def init(self, metrics):
        """Initialize the curriculum."""
        if self.curriculum is None:
            if not hasattr(metrics["env"], "task_space"):
                raise ValueError(
                    """Not a valid contextual environment for Syllabus.
                    Use an environment with a built-in TaskSpace.
                    See Syllabus documentation for more details."""
                )
            self.make_curriculum(metrics["env"], self.curriculum_config)

        # Make sure we only do this once
        self.change_task_on_reset(metrics)
        self.pre_step_methods = []

    def batch_dr_update(self, metrics):
        """Update the curriculum based on the episode metrics."""
        # For simplicity, we ignore episode length, env name and task completion here
        self.curriculum.update_on_episode(
            metrics["episode_reward"],
            length=1,
            task=metrics["env"].get_task(),
            progress=False,
            env_id="default",
        )
