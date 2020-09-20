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

        self.reference_dict = self._read_file(self.data_dir + "reference.json")
        self.index_list = self._read_file(self.data_dir + "index.json")

    def remove_entry(self, name, collection):
        '''
        Removes an entry from index.json

        Input:
            name (str): The name of the file to remove
            collection (str): The collection the file is located in
        
        Returns:
            True on sucessful removal and False on failure.
        '''
        pass

    def insert_entry(self, name, collection):
        '''
        Adds an entry to index.json

        Input:
            name (str): The name of the file to remove
            collection (str): The collection the file is located in
        
        Returns:
            True on sucessful addition and False on failure. 
        '''

        # Check if file is in reference
        name_no_extension = name.split(".")[0]
        in_index = False
        if collection in self.reference_dict:
            if name_no_extension in self.reference_dict[collection]:
                in_index = self.reference_dict[collection][name_no_extension]["inIndex"]
            else:
                # Add file to reference
                pass
        else:
            # Add collection and file to reference
            pass

        if in_index:
            print(f"{collection}/{name} is already in index")
            return False
        
        # Insert into reference function
        # Look into bisect module. Allows insertion into sorted list
        

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
        
        self._write_to_file(self.data_dir + "reference.json")
                

    def build_reference_dir(self, collection, append=False):
        '''
        Goes through a directory and does actions described in build_reference_dict

        Input:
            name (str): The name of the file
            append (bool): If true update reference at end of function
        '''
        for i in os.listdir(self.data_dir + collection):
            # Calls build_reference file on all json files
            if i.split(".")[-1] == "json":
                self.build_reference_file(i, collection)
        
        if append:
            self._write_to_file(self.data_dir + "reference.json")

    def build_reference_file(self, name, collection, append=False):
        '''
        Goes through a file and does actions described in build_reference_dict

        Input:
            name (str): The name of the file
            collection (str): The collection the file is located in
            append (bool): If true write to reference file after function
        '''
        file_location = self.data_dir + collection + "/" + name
        file_data = self._read_file(file_location)
        
        has_header = self._verify_header(name, collection)

        if not has_header:
            print(f"Adding header to {collection} / {name}")
            generate_and_add_header(file_location, sas_file=False)
        
        name_no_extension = name.split(".")[0]
        found_in_index = self._find_file_index(collection.lower(), name_no_extension.lower(), 0, len(self.index_list) - 1)

        if collection not in self.reference_dict:
            self.reference_dict[collection] = {}
        
        if name_no_extension not in self.reference_dict[collection]:
            self.reference_dict[collection][name_no_extension] = {}
        
        self.reference_dict[collection][name_no_extension]["inIndex"] = found_in_index
        self.reference_dict[collection][name_no_extension]["lastUpdated"] = str(datetime.datetime.now())
        print(f"File {collection}/{name} was added to the reference dict")

        if append:
            self._write_to_file(self.data_dir + "reference.json")


    def _verify_header(self, name, collection):
        '''
        Verifies if a file has a header

        Input:
            name (str): The name of the file
            collection (str): The collection the file is located in 
        
        Returns:
            True if there is a header with all the proper fields and False if not
        '''
        file_location = self.data_dir + collection + "/" + name
        file_data = self._read_file(file_location)
        
        expected_keys = ["numCats", "varCats", "title", "numOfVars", "varNames", "theData"]
        file_keys = set(file_data.keys())

        for k in expected_keys:
            if k not in file_keys:
                return False

        return True
    
    def _find_file_index(self, collection, name, left, right):
        '''
        Finds if file is in index.json
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
        middle_collection = self.index_list[middle]["collection"].lower()
        middle_name = self.index_list[middle]["name"].lower()

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
    
    def _read_file(self, file_path):
        '''
        Reads in file data

        Inputs:
            file_path (str): Path to the file

        Returns:
            File data if sucessful else None
        '''

        with open(file_path) as json_file: 
            try:
                return json.load(json_file) 
            except:
                print(f"ERROR: {file_path} failed to read in")

    def _write_to_file(self, file_path):
        '''
        Writes the current values to reference.json

        Inputs:
            file_path (str): Path to the file
        '''

        with open(file_path, mode='w') as json_file:
            try:
                json.dump(self.reference_dict, json_file, indent=4)
                print(f"{file_path} sucessfully added")
            except:
                print(f"ERROR: failed to add {file_path}")
        
