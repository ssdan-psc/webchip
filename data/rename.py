import os, sys, argparse

parser = argparse.ArgumentParser()
parser.add_argument('-r', '--replace')
parser.add_argument('-s', '--state')
args = parser.parse_args()

if args.replace:
	directory = args.replace
	for filename in os.listdir(directory):
		if not filename.endswith(".dat") and not filename.endswith('meta'):
			os.rename(os.path.join(directory, filename), os.path.join(directory, filename.split('.')[0] + ".dat"))

elif args.state:
	directory = args.state
	for filename in os.listdir(directory):
		if not filename.endswith(".dat") and not filename.endswith('meta'):
			cat, state = filename.split('.')
			os.rename(os.path.join(directory, filename), os.path.join(directory, cat + "_" + state + ".dat"))