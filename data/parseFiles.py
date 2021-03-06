import json
import os
import sys
import logging
import argparse

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

#divide array l in array of arrays of size n
def chunk(l, n):
    n = max(1, n)
    return [l[i:i + n] for i in range(0, len(l), n)]

# Writes JSON from .dat CSV 
def parse(file_name):
	logging.info('Parsing ' + file_name)
	final_object = {}
	in_file = open(file_name, "rU")
	lines = in_file.readlines()
	lines = [x.rstrip(" \n") for x in lines]
	in_file.close()
	#title of dataset, string
	title = lines[0]
	#number of variables, integer
	num_of_vars = int(lines[1])
	#name of variable, array of strings
	var_names = lines[2].split(",")
	#number of categories per variable, list of integers
	num_vars = lines[3].split(",")
	num_vars = [int(x) for x in num_vars]
	#array of objects containing name of variable and list of categories, object array
	var_categories = []
	i = 4
	for var in var_names:
		item = {"name": var, "cats": ""}
		line = lines[i]
		item["cats"] = line.split(",")
		var_categories.append(item)
		i += 1

	first_data_line_index = 4 + num_of_vars
	#lines in file made of data plus the file end signal ('*****')
	data_lines_plus_end = lines[first_data_line_index:]
	#string containing data lines with newlines included
	data_lines_raw = ''
	for ind, val in enumerate(data_lines_plus_end):
		if val == '*****':
			data_lines_raw = data_lines_plus_end[:ind]
			break

	#populate array with arrays containing data lines, 
	#with size being number of categories of last variable
	data_lines_combined = []
	for line in data_lines_raw:
		line = line.rstrip(',\n')
		data_lines_combined += line.split(',')
	line_item_count = num_vars[-1]
	data_lines_split = chunk(data_lines_combined, line_item_count)
	data_lines = []
	for line in data_lines_split:
		line = ','.join(line)
		data_lines.append(line)

	#initialize individual objects with dependent variable, "Dep"
	objects = []
	for line in data_lines:
		vals = line.split(",")
		for val in vals:
			objects.append({"Dep": val})

	#counter function that starts over at 0 if the_max is reached 
	def increment(the_max, cur):
		if(cur == the_max-1):
			return(0)
		else:
			return(cur + 1)

	#apply variable categories to each object
	def apply_label(l, var_name, labels, reset):
		m = l
		i = 0
		j = 0
		label_len = len(labels)
		current_label = labels[0]
		for k in m:
			k[var_name] = current_label
			i += 1
			if(i == reset):
				j = increment(label_len, j)
				current_label = labels[j]
				i = 0
			else:
				continue
		return m

	#work backward to apply variable values to each object
	var_names_reversed = var_names[::-1]
	var_categories_reversed = var_categories[::-1]
	num_vars_reversed = num_vars[::-1]

	branchers = num_vars_reversed[:-1]
	multiplier = 1
	multipliers = [1]
	for j in branchers:
		multiplier *= j
		multipliers.append(multiplier)

	for idx, val in enumerate(multipliers):
		objects = apply_label(objects, var_names_reversed[idx], var_categories_reversed[idx]['cats'], val)

	#establish metadata fields
	data = {}
	data["title"] = title
	data["numOfVars"] = num_of_vars
	data["varNames"] = var_names
	data["numCats"] = num_vars
	data["varCats"] = var_categories
	data["theData"] = objects

	#write object to file
	file_tokens = file_name.split("/")
	needed_tokens = file_tokens[1:]
	name = needed_tokens[1].split(".")[0] + ".json"
	group = needed_tokens[0]
	out_file_name = group + "/" + name
	with open(out_file_name, 'w') as out_file:
		logging.info("Writing " + out_file_name)
		j = json.dumps(data, indent=4)
		out_file.write(j)

#build index.json file from base directory
def build_index():
	the_index = []
	ignore = [".DS_Store", ".gitignore", "parseFiles.py", "index.json", "README.md", "rename.py"]
	for dirname, dirnames, filenames in os.walk('.'):
		for filename in filenames:
			tokens = os.path.join(dirname, filename).split("/")
			if not list(set(tokens) & set(ignore)):	#if intersection of tokens and ignore is empty
				needed_tokens = tokens[1:]
				name = needed_tokens[1].split(".")[0]
				group = needed_tokens[0]
				real_path = "data/" + "/".join(needed_tokens)
				with open("/".join(needed_tokens)) as check_title:
				 	title = check_title.readlines()[0]
				record = {"name": name, "path": real_path, "collection": group}
				if ".json" in record["path"]:
					the_index.append(record)
	with open("index.json", 'w') as out_file:
		j = json.dumps(the_index, indent=4)
		out_file.write(j)


#option to parse individual files, pass as command line arguments, 
#otherwise parse all in all subdirectories
def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-f', '--file')
	args = parser.parse_args()

	if args.file:
	 	for f in sys.argv:
	 		parse(f)
	else:
	 	for dirname, dirnames, filenames in os.walk('.'):
			for filename in filenames:
				filename = os.path.join(dirname, filename)
				if '.dat' in filename.lower():
					parse(filename)
				else:
					logging.info("Skipped parse & build JSON for " + filename)

	logging.info('Building index')
	build_index()

if __name__ == "__main__": 
	main()



