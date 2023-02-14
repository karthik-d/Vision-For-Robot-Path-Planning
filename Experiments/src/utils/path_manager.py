import os

# Append and extend path as long as there is only
# one file in the directory!
def append_linear_levels(path, stop_at_dir=True):
	if os.path.isdir(path):
		contents = os.listdir(path)
		while(len(contents)==1):
			path = os.path.join(path, contents[0])
			if not stop_at_dir or os.path.isdir(path):
				contents = os.listdir(path)
			else:
				break
	return path

