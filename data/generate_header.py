import json
import os
import sys
from collections import OrderedDict

def first_entry(entry, header, cat_variables, quant_variables):
    '''
    Modifies the header for the first dicotonary entry

    Input:
        entry (dict): Entry from the data
        header (dict): The header to return summarizing the data
        cat_variables (set): The set of categorical variables
        quant_variables (set): The set of quantiative variables
    
    '''
    for i in entry:
        # Adds categoical data if not dep and not a number
        if i != "Dep" and (type(entry[i]) != int) and (type(entry[i]) != float):
            cat_variables.add(i)
            header["varCats"][i] = {entry[i]: True}
        else:
            quant_variables.add(i)
    

def subsequent_entries(entry, header, cat_variables, quant_variables):
    '''
    Modifies the header for the first dicotonary entry

    Input:
        entry (dict): Entry from the data
        header (dict): The header to return summarizing the data
        cat_variables (set): The set of categorical variables
        quant_variables (set): The set of quantiative variables
    
    '''

    found_cat_variables = set()

    for i in entry:
        # Output dictonary if variable not seen before
        if i not in cat_variables and i not in quant_variables:
            print(f"ERROR: {i} is an extra variables in dictonary\n")
            print(json.dumps(entry, indent=2))
        # Adds categorical variable value if not seen before
        elif i in cat_variables:
            found_cat_variables.add(i)
            if entry[i] not in header["varCats"][i]:
                header["varCats"][i][entry[i]] = True
    
    # Output diconary if categorical variables missing
    if len(found_cat_variables) != len(cat_variables):
        missing_vars = list(cat_variables.difference(found_cat_variables))
        print(f"ERROR: The following dictonary is missing the following categorical variables {missing_vars}")
        print(json.dumps(entry, indent=2))


def generate_header(file_path):
    '''
    Generates a header for json file with the same formatting the header for Earn_AK.json

    Input:
        file_path (str): path to the file
    
    Returns:
        Dictonary of header. Similar to that within Earn_AK.json
    '''
    
    header = OrderedDict()
    cat_variables = set()
    quant_variables = set()

    with open(file_path) as json_file: 
        try:
            data = json.load(json_file) 
        except:
            print(f"ERROR: {file_path} failed to read in")
    
    header["title"] = data["SASJSONExport"]
    header["numOfVars"] = 0
    header["varNames"] = []
    header["numCats"] = []
    header["varCats"] = {}
    
    data_list = data["SASTableData+EDUCDATA"]

    for i in range(len(data_list)):
        if i == 0:
            first_entry(data_list[i], header, cat_variables, quant_variables)
        else:
            subsequent_entries(data_list[i], header, cat_variables, quant_variables)
    
    
    # Formats header and combines data to look like example files
    header["numOfVars"] = len(header["varCats"])
    header["varNames"] = list(header["varCats"].keys())
    varcats_list = []

    for i in header["varCats"]:
        temp_dict = OrderedDict()
        header["numCats"].append(len(header["varCats"][i]))
        temp_dict["name"] = i
        temp_dict["cats"] = list(header["varCats"][i])
        varcats_list.append(temp_dict)

    header["varCats"] = varcats_list
    return header
  
def add_header(header, file_path):
    '''
    Adds a header to the specified file

    Input:
        header (dict): Header according to spec
        file_path (str): path to the file
    
    '''

    with open(file_path) as json_file: 
        data = json.load(json_file)

    for i in header:
        data[i] = header[i]

    data["theData"] = data["SASTableData+EDUCDATA"]
    del data["SASTableData+EDUCDATA"]
    del data["SASJSONExport"]

    with open(file_path, mode='w') as json_file:
        try:
            json.dump(data, json_file, indent=4)
            print(f"{file_path} sucessfully added header")
        except:
            print(f"ERROR: {file_path} failed to add header")

def generate_and_add_header(file_path):
    '''
    Combines generate header and add header functions for easy use by other python scrips

    Returns
        True on sucess and False on failure
    '''

    try:
        header = generate_header(file_path)
        add_header(header, file_path)
        True
    except:
        return False

if __name__ == "__main__": 
    if len(sys.argv) != 2:
        print(f"ERROR: Invalid number of command line arguments. Should have 2 not {len(sys.argv)}")
        exit(0)

    generate_and_add_header(sys.argv[1])