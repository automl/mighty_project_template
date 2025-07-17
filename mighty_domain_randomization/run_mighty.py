from __future__ import annotations

import time
from typing import TYPE_CHECKING

import hydra
import numpy as np
import minigrid # noqa: F401
from mighty.mighty_runners.factory import get_runner_class

if TYPE_CHECKING:
    from omegaconf import DictConfig


@hydra.main("./configs", "base", version_base=None)
def run_mighty(cfg: DictConfig) -> None:
    """Run Mighty with the given configuration."""
    runner_cls = get_runner_class(cfg.runner)
    runner = runner_cls(cfg)

    # Execute run
    start = time.time()
    train_result, eval_result = runner.run()
    end = time.time()

    # Print stats
    print("Training finished!")
    print(
        f"Reached a reward of {np.round(eval_result['mean_eval_reward'], decimals=2)} in {train_result['step']} steps and {np.round(end - start, decimals=2)}s."  # noqa: E501
    )
    return eval_result["mean_eval_reward"]


if __name__ == "__main__":
    run_mighty()
