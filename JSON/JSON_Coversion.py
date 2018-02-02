# JSON Conversion Script
# SSDAN - Phillip Dequina
# Python 3


# TO USE:
# Assign the following vars in the TO DO
# Run the python script
# Output will be found int the [exportFilename]

# TO DO:
# filename := input .json filename
# exportFilename := export .json filename
# title := title of schema

# Import Needed Library
import json

# Create a Dictonary of Each JSON Object
# Initialize an Empty Dictonary
dic = {}
# Open and Import the JSON Data, Located in the Same Folder
filename = 'EarnEduOccVet-Pre.json'
with open(filename) as json_data:
    item = json.load(json_data)
# Store Each Key and Value in a Dictionary of Dictionaries
# Assign a One Entry Dictionary to Each Category
for k, v in item[0].items():
# Didn't Store the "Dep" Category
    if(k != 'Dep'):
        dic[k] = {v}
# Append the Dictionaries Together
for i in range(1, len(item)):
    for k, v in item[i].items():
        if k in dic:
            dic2 = {v}
            dic[k].update(dic2)
    
# Create an Export File
exportFilename = "foo.json"
fo = open(exportFilename, "w")

# Outputing the Schema
fo.write("{\n")
fo.write('      "numCats": [\n')
# "numCats":
for i in range(0, len(dic)):
    fo.write("        " + str(len(dic[list(dic.keys())[i]])) + ',\n')
fo.write("    ],\n")
fo.write('    "varCats": [\n')
# "varCats":
counter = len(dic)
for k, v in dic.items():
    fo.write("        {\n")
    fo.write('            "cats": [\n')
# "cats":
    for i in range(0, len(list(v))):
        if i == len(list(v)) - 1:
            fo.write('                "' + str(list(v)[i]) + '"\n')
        else:
            fo.write('                "' + str(list(v)[i]) + '",\n')

    fo.write("            ],\n")
# "name":
    fo.write('            "name": "' + k + '"\n')
    counter -= 1
    if(counter == 0):
        fo.write("        }\n")
    else:
        fo.write("        },\n")
# End of Schema
fo.write("    ],\n")
# Title
title = "<<placeholder_text>>"
fo.write(' "title": ' + title + '\n')
fo.write('    "numOfVars": ' + str(len(dic)) + ',\n')
fo.write('    "varNames": [\n')
# "varNames":
counter2 = len(dic)
for i in range(0, len(dic)):
    counter2 -= 1
    if(counter2 == 0):
        fo.write('        "' + str(list(dic.keys())[i]) + '"\n')
    else:
        fo.write('        "' + str(list(dic.keys())[i]) + '",\n')
# "theData":        
fo.write('    ],\n')
fo.write('  "theData": \n')

# Pretty Print the JSON Objects
for i in range(0, len(item)):
    fo.write('    {\n')
# Fill in the "Dep": // Can comment out if not needed
    fo.write('      ' + '"Dep"' + ': "' + item[i]['Dep'] + '",\n')
    counter3 = len(dic.keys())
    for key in range(0, len(dic.keys())):
        counter3 -= 1
        if(counter3 == 0):
            fo.write('      "' + str(list(dic.keys())[key]) + '": "' + str(item[i][list(dic.keys())[key]]) + '"\n')
        else:
            fo.write('      "' + str(list(dic.keys())[key]) + '": "' + str(item[i][list(dic.keys())[key]]) + '",\n')
    if(i == len(item) - 1):
        fo.write('    }\n')
    else:
        fo.write('    },\n')

# Closing Brackets
fo.write('  ]\n')
fo.write('}')
