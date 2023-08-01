# fetch datas and store it in a json file. 
# from pathlib import Path

from components.google_credentials import *
from components.api_request import ApiRequest, json
# from components.retrieve_data import RetrieveData
from google.oauth2.credentials import Credentials
from google.cloud import storage
from retrieveData import *
from typing import Any, Callable
import os
import pandas as pd

class FetchData():
    CREDS = Credentials.from_authorized_user_info(
        info = {
            "access_token": ACCESS_TOKEN,
            "refresh_token": REFRESH_TOKEN,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "token_uri": TOKEN_URI
        }
    )

    # bigQuery credentials
    PROJECT_ID = 'jyh-dropship-looker-studio-v1'

    def __init__(self, dataframe: pd.DataFrame):
        assert isinstance(dataframe, pd.DataFrame), "The argument should be a pandas Dataframe."
        self.dataframe = dataframe
        
        self.final_result = None
        self.all_data = []
        self.datas_with_campaigns = []
        
    
    def __call__(self) -> pd.DataFrame:
        "Invoke this using <instance_name> then add parenthesis. example: instance()"
        return self.dataframe
        
    @property
    def init_key_tokens_dictionary(self) -> dict:
        profile_id_index = self.dataframe.set_index("Profile ID")
        dictionary = profile_id_index["Access Token"].to_dict()
        
        return {
            str(key).replace(".0", ""): value
            for key, value in dictionary.items()
        }

    def extend_to_all_data(self, data: list):
        self.all_data.extend(data)

    def extend_to_datas_with_campaigns(self, data: list):
        self.datas_with_campaigns.extend(data)

    def _exception_handling(fn):
        def wrapper(self, *args, **kwargs) -> Callable[..., Any]:
            try:
                result = fn(self, *args, **kwargs)
            except IndexError:
                result = None
                print("And index error occured.")
            return result
        return wrapper
    
    @_exception_handling
    def retrieve_and_combined_data(self) -> None:
        for ids, token in self.init_key_tokens_dictionary.items():
            get_response = ApiRequest(profile_id = ids, access_token = token)
            get_response.execute_response()

            if get_response.data is not None and len(get_response.data) != 0:
                self.extend_to_all_data(get_response.data)

                if "adaccounts" in get_response.data[0]:
                    adaccounts_data = get_response[0]["adaccounts"]["data"]
                    campaigns = get_data_of_campaigns(adaccounts_data)
                    self.extend_to_datas_with_campaigns(campaigns)

    def execute_functions(self) -> None:
        copy_datas_with_campaigns = self.datas_with_campaigns.copy()
    
        # original data
        index_and_datas = get_index_position_and_data_if_next_is_found(copy_datas_with_campaigns)

        # process data that have next keyword
        next_in_next = extract_next_url_if_found_after_dictionary(index_and_datas)

        # new data
        new_data_result = overwrite_datas_after_extracted_next_url(index_and_datas, next_in_next)

        # deleting the next
        my_final_result = delete_pagings_when_done_extracting(new_data_result)

        self.final_result = my_final_result

    def _loop_validator(self, data, condition: str, combination: list = None):
        """condition choose: ('get_next' and 'reassign')"""
        data_list = []
        
        if condition == "get_next":
            for element in data:
                for idx, key in enumerate(element["adaccounts"]["data"]):
                    if "campaigns" in key:
                        target = element["adaccounts"]["data"][idx]["campaigns"]["paging"]

                        if "next" in target:
                            x_mark = element["adaccounts"]["data"][idx]["campaigns"]["paging"]
                            data_list.append(x_mark)
        
            return data_list
        
        elif condition == "reassign" and combination is not None:
            counter = 0

            for element in data:
                for idx, key in enumerate(element["adaccounts"]["data"]):
                    if "campaigns" in key:
                        target = element["adaccounts"]["data"][idx]["campaigns"]["paging"]

                        if "next" in target:
                            element["adaccounts"]["data"][idx]["campaigns"]["data"] = combination[counter]
                            counter += 1
                        
                            if counter >= len(combination):
                                break
                
                if counter >= len(combination):
                    break

    def reassignment_of_values(self) -> None:
        my_list = [value["data"] for value in self.final_result.values() if self.final_result is not None]
        all_data_copy = self.all_data.copy()
        all_data_adaccounts_campaigns_with_next_keyword = self._loop_validator(all_data_copy, "get_next")

        combined = [
            data1 + data2
            for data1, data2 in zip(all_data_adaccounts_campaigns_with_next_keyword, my_list)
        ]

        self._loop_validator(self.all_data, condition = "reassign", combination = combined)
        self._delete_pagings()

    def _delete_pagings(self) -> None:
        for element in self.all_data:
            for idx, key in enumerate(element["adaccounts"]["data"]):
                if "campaigns" in key:
                    del element["adaccounts"]["data"][idx]["campaigns"]["paging"]
                     
    def reassignment_of_values(self) -> None:
        my_list = [value["data"] for value in self.final_result.values() if self.final_result is not None]
        all_data_copy = self.all_data.copy()
        all_data_adaccounts_campaigns_with_next_keyword = []

        for element in all_data_copy:
            for idx, key in enumerate(element["adaccounts"]["data"]):
                if "campaigns" in key:
                    target = element["adaccounts"]["data"][idx]["campaigns"]["paging"]

                    if "next" in target:
                        x_mark = element["adaccounts"]["data"][idx]["campaigns"]["data"]
                        all_data_adaccounts_campaigns_with_next_keyword.append(x_mark)
        
        # (------------------------------------------------------------------------------)
        combined = [
            data1 + data2
            for data1, data2 in zip(all_data_adaccounts_campaigns_with_next_keyword, my_list)
        ]

        counter = 0
        for element in self.all_data:
            for idx, key in enumerate(element["adaccounts"]["data"]):
                if "campaigns" in key:
                    target = element["adaccounts"]["data"][idx]["campaigns"]["paging"]
                    
                    if "next" in target:
                        element["adaccounts"]["data"][idx]["campaigns"]["data"] = combined[counter]
                        counter += 1

                        if counter >= len(combined):
                            break
            
            if counter >= len(combined):
                break
        
        self._delete_pagings()

    def process_data_now(self) -> None:
        self.retrieve_and_combined_data()
        self.execute_functions()
        self.reassignment_of_values()

    def upload_to_google_storage(self, bucket_name: str, folder_name: str, filename: str) -> None:
        client = storage.Client(project = self.PROJECT_ID, credentials = self.CREDS) 
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(folder_name + '/' + filename)
        data = json.dumps(self.all_data, indent = 2)

        try:
            blob.upload_from_string(data) # only accepts a json string
            print(f"File {filename} uploaded to Google Cloud Storage.")
        except Exception as e:
            print(f"Failed to upload file to Google Cloud Storage. Error: {str(e)}")

    def upload_to_local(self, filename: str) -> None:
        if not filename.endswith(".json"):
            filename += ".json"
        
        # init the retrievefunction
        directory_path = r"C:\Users\Swazzernoodle\Desktop\Project_Python\function-fb-1-updated\json"
        directory_path2 = r"D:\python_project\json"
        directory_path3 = r"D:\test_python_project"
        
        # combined the directory path and the filename.
        file_path = os.path.join(directory_path3, filename) 

        with open(file_path, mode = "w") as file:
            file.write(json.dumps(self.all_data, indent = 2))

        print("Upload successfully on local drive: path is in json folder.")