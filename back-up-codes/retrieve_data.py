from typing import List
import requests

class RetrieveData():
    def __init__(self, data: List[dict]):
        self.data = data

    def __call__(self):
        return self.data

    def _quick_requests(self, args):
        try:
            response = requests.get(args, timeout=40)
            response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
            to_json = response.json()
        except requests.exceptions.RequestException as e:
            print(f"An error occurred during the HTTP request: {str(e)}")
            return None
        except ValueError as e:
            print(f"An error occurred while parsing the response JSON: {str(e)}")
            return None
        else:
            return to_json["data"]
    
    def check_if_data_has_adaccounts(self):
        if "adaccounts" in self.data[0]:
            return True
            # return self.data[0]["adaccounts"]["data"]
        
    def _delete_next(self, index_pos) -> None:
        if "adaccounts" in self.data[0]:
            if "paging" in self.data[0]["adaccounts"]["data"]:
                del self.data[0]["adaccounts"]["data"][index_pos]["campaigns"]["paging"]["next"]

        # if 'paging' in ad_account_validator[index_pos]['campaigns']:
        #     del ad_account_validator[index_pos]['campaigns']['paging']['next']
            

    def _decorator(fn):
        def wrapper(self, *args, **kwargs):
            index_loc, next_keyword_json = [], []
            master_data = None

            validator = self.check_if_data_has_adaccounts()
            
            if validator:
                master_data = self.data[0]["adaccounts"]["data"]

            for idx, data_items in enumerate(master_data):
                if "campaigns" in data_items:
                    target_paging = data_items["campaigns"]["paging"]
                    if "next" in target_paging:
                        next_keyword_found = target_paging["next"]
                        index_loc.append(idx)
                        next_keyword_json.append(
                            self._quick_requests(next_keyword_found)
                        )

            return fn(self, index_loc, next_keyword_json, master_data, *args, **kwargs)

        return wrapper
    
    @_decorator
    def retrieve_and_append_next_page_data(self, index_loc, next_keyword_json, master_data):
        if index_loc:
            for index_target in index_loc:
                for_extension = master_data[index_target]["campaigns"]["data"]
                combined_json = for_extension + next_keyword_json
                # self.data[0]["adaccounts"]["data"][index_target]["campaigns"]["data"] = combined_json
                if "adaccounts" in self.data[0]:
                    self.data[0]["adaccounts"]["data"][index_target]["campaigns"]["data"] = combined_json

                self._delete_next(index_target)