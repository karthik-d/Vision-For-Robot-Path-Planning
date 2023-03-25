# Download model and save it into the logs/ folder
python -m rl_zoo3.load_from_hub --algo tqc --env PandaReach-v1 -orga sb3 -f logs/
python enjoy.py --algo tqc --env PandaReach-v1  -f logs/

python train.py --algo tqc --env PandaReach-v1 -f logs/
