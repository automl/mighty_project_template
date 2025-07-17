# This is for base PPO
python mighty_domain_randomization/run_mighty.py --config-name=hpo environment=contextual_minigrid cluster=local -m

# This is the DR version
python mighty_domain_randomization/run_mighty.py --config-name=hpo_dr environment=contextual_minigrid cluster=local -m