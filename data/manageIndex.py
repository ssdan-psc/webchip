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

    def build_reference_file(self, name, collection):
        '''
        Goes through a file and does actions described in build_reference_dict

        Input:
            name (str): The name of the file
            collection (str): The collection the file is located in
        '''
        pass

    def _verify_header(self, name, collection):
        '''
        Verifies a file has a header

        Input:
            name (str): The name of the file
            collection (str): The collection the file is located in 
        
        Returns:
            True if there is a header and False if not
        '''
