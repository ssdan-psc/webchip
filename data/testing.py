import json
from manageIndex import ManageIndex
from generateHeader import  generate_and_add_header

temp = ManageIndex()
#temp.insert_name("ape.json", "abc123")
#temp.remove_name("hhpov10.json", "acs10_1yr")
#temp.remove_name("popusa10.json", "acs10_1yr")

temp.insert_collection("abc123")
#temp.remove_collection("abc123")

#generate_and_add_header('abc123/employ10.json', sas_file=True)