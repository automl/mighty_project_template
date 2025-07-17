# Mighty Example Project: Syllabus Domain Randomization

This repository is an example of how to build a project with [Mighty](https://github.com/automl/Mighty). We use the curriculum learning library [Syllabus](https://github.com/RyanNavillus/Syllabus) in a new meta component that lets us compare [domain randomization](https://arxiv.org/pdf/1703.06907) to base algorithms on different MiniGrid environments.

## Installation 
You can install all dependencies by first creating a new virtual environment:

```bash
pip install uv
uv venv --python 3.11
source .venv/bin/activate
```

And then running:
```bash
make install
```

## Repository Content
This example repository mimics several relevant components of real RL projects:
- runscripts for local and parallel cluster evaluation in the 'runscripts' directory
- pre-computed results you can inspect in 'runs'
- code for the domain randomization interface in 'mighty_domain_randomization/mighty_syllabus_dr.py' and 'mighty_domain_randomization/env_task_wrapper.py'
- visualization of the results in 'mighty_domain_randomization/plots.ipynb'

Everything should immediately be runnable locally, for the parallel cluster options you'll need to complete the config files in 'mighty_domain_randomization/configs/cluster' with your partition names.

## Implementing Domain Randomization
Syllabus provides several curriculum options which need to have access to a task space object and then be updated and called during training. So to use such a curriculum in training, we have to:
1. Create an environment with a Syllabus TaskSpace
2. Initialize the curriculum
3. Query the curriculum for fresh tasks when needed
4. Update the curriculum with runtime information

The Mighty meta components can interact with most parts of the RL loop, so they're ideal for this example. After initializing the curriculum, we make sure to update to the correct task whenever one of our environments is reset:

```python
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
```

And then we implement a function to tell the curriculum about current episode statistics:

```python
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
```

The tricky part is to interface with MiniGrid. Syllabus provides an example task space we build upon, but we want to use vectorized environments with image observations. So on init, we first make sure our observation spaces work for this setting and define our task space:

```python
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
```

Then we implement how we change tasks for envs that need a reset:

```python
    def change_task(self, new_task, change_positions):
        """Reset selected environments with a new task."""
        for i, pos in enumerate(change_positions):
            seed = int(new_task[i])
            self.task[pos] = seed
            self.envs[pos].reset(seed=seed, **self.reset_kwargs)
```

## Running Experiments
If you want to run the experiments in this repo, we recommend starting with our runscripts. They show how to run hyperparameter optimization, different environments as well as baselines. 
Of course you can add your own variations on top (switching algorithms, etc.). If you want to add new environment, remember they need a task space wrapper! You can use the pre-defined ones from Syllabus, but you will need to make sure to only run a single environment at a time - or you create a vectorized version similar to our MiniGrid wrapper.