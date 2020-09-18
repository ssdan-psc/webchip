import datetime
import json
import os
from generateHeader import generate_and_add_header

class ManageIndex:
    '''This class provides an interface for modyfing index.json and the headers within data json files'''

    def __init__(self):
        # Directories to ignore
        self.ignore = set(['__pycache__', '.gitignore',])
        # Gets root of data directory
        self.data_dir = '/'.join(os.path.realpath(__file__).split("/")[:-1]) + "/"

        with open(self.data_dir + "reference.json") as json_file: 
            try:
                self.reference_dict = json.load(json_file) 
            except:
                print(f"ERROR: reference.json failed to read in")
        
        with open(self.data_dir + "index.json") as json_file: 
            try:
                self.index_list = json.load(json_file) 
            except:
                print(f"ERROR: index.json failed to read in")

    def remove_file(self, name, collection):
        '''
        Removes an entry from index.json

        Input:
            name (str): The name of the file to remove
            collection (str): The collection the file is located in
        
        Returns:
            True on sucess and False on failure.
        '''
        pass

    def insert_file(self, name, collection):
        '''
        Adds an entry to index.json

        Input:
            name (str): The name of the file to remove
            collection (str): The collection the file is located in
        
        Returns:
            True on sucess and False on failure. 
        '''
        pass

    def build_reference_dict(self):
        '''
        Builds a json file that has every file and says if it is in index.json
        While building  the reference if a file does not have a header one will be added
        Format:
            {
                "collection name":
                {
                    "file name": {
                        "in_index": bool,
                        "last_modified": str
                    }
                }
            }

        '''
        # I am making the assumption that the directories will not have a . in their name
        for i in os.listdir():
            # Goes through every directory withiout ignored words and with no dots, assumed to be files
            if i not in self.ignore and not '.' in i:
                self.build_reference_dir(i)
                break

    def build_reference_dir(self, collection):
        '''
        Goes through a directory and does actions described in build_reference_dict

        Input:
            name (str): The name of the file
        '''
        for i in os.listdir(self.data_dir + collection):
            # Calls build_reference file on all json files
            if i.split(".")[-1] == "json":
                self.build_reference_file(i, collection)
                break

    def build_reference_file(self, name, collection):
        '''
        Goes through a file and does actions described in build_reference_dict

        Input:
            name (str): The name of the file
            collection (str): The collection the file is located in
        '''
        file_location = self.data_dir + collection + "/" + name
        with open(file_location) as json_file: 
            try:
                file_data = json.load(json_file) 
            except:
                print(f"ERROR: {collection} / {name} failed to read in")
        
        has_header = self._verify_header(name, collection)

        if not has_header:
            print(f"Adding header to {collection} / {name}")
            generate_and_add_header(file_location, sas_file=False)
        
        name_no_extension = name.split(".")[0]
        found_in_index = self._find_file_index(collection, name_no_extension, 0, len(self.index_list) - 1)

        if collection not in self.reference_dict:
            self.reference_dict[collection] = {}
        
        if name_no_extension not in self.reference_dict[collection]:
            self.reference_dict[collection][name_no_extension] = {}
        
        self.reference_dict[collection][name_no_extension]["inIndex"] = found_in_index
        self.reference_dict[collection][name_no_extension]["lastUpdated"] = str(datetime.datetime.now())


    def _verify_header(self, name, collection):
        '''
        Verifies a file has a header

        Input:
            name (str): The name of the file
            collection (str): The collection the file is located in 
        
        Returns:
            True if there is a header and False if not
        '''

        return True
    
    def _find_file_index(self, collection, name, left, right):
        '''
        Finds file in index.json
        Since index is sorted we can use binary search to find items

        Input:
            collection (str): collection the in question
            name (str): name of the files
            left (int): left index of binary search
            right (int): right index of binary search
        
        Returns:
            True if found and False if not found
        '''
        if left > right:
            return False
        
        middle = (left + right) // 2
        middle_collection = self.index_list[middle]["collection"]
        middle_name = self.index_list[middle]["name"]

        if middle_collection == collection and middle_name == name:
            return True
        elif middle_collection == collection:
            if middle_name < name:
                left = middle + 1
            else:
                right = middle - 1
        elif middle_collection < collection:
            left = middle + 1
        else:
            right = middle - 1

        return self._find_file_index(collection, name, left, right)
            