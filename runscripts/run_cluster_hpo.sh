# This will only work if you add your own partition name in the configs/cluster/cpu.yaml file
# The same is true if you want to run on GPU, you need to add your own partition name in the configs/cluster/gpu.yaml file
python mighty_domain_randomization/run_mighty.py --config-name=hpo environment=contextual_minigrid cluster=cpu -m

python mighty_domain_randomization/run_mighty.py --config-name=hpo_dr environment=contextual_minigrid cluster=gpu -m