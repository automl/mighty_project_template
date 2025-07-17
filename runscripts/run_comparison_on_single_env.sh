python mighty_domain_randomization/run_mighty.py --config-name=base environment=contextual_minigrid seed=0,1,2,3,4 -m
python mighty_domain_randomization/run_mighty.py --config-name=dr_curriculum environment=contextual_minigrid seed=0,1,2,3,4 -m

# Switch to simpler environment
python mighty_domain_randomization/run_mighty.py --config-name=base environment=contextual_minigrid env=MiniGrid-Empty-Random-5x5-v0 seed=0,1,2,3,4 -m
python mighty_domain_randomization/run_mighty.py --config-name=dr_curriculum environment=contextual_minigrid env=MiniGrid-Empty-Random-5x5-v0 seed=0,1,2,3,4 -m

# Switch to harder environment
python mighty_domain_randomization/run_mighty.py --config-name=base environment=contextual_minigrid env=MiniGrid-RedBlueDoors-8x8-v0 seed=0,1,2,3,4 -m
python mighty_domain_randomization/run_mighty.py --config-name=dr_curriculum environment=contextual_minigrid env=MiniGrid-RedBlueDoors-8x8-v0 seed=0,1,2,3,4 -m