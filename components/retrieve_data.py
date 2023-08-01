import requests

def get_request(url):
    response = requests.get(url , timeout = 50)
    return response.json()

def get_data_of_campaigns(adaccounts_data, key = "campaigns"):
    list_that_have_campaigns = []

    for campaigns in adaccounts_data:
        if key in campaigns.keys():
            list_that_have_campaigns.append(campaigns[key])
    
    return list_that_have_campaigns

def get_index_position_and_data_if_next_is_found(list_of_campaign_datas: list[dict], key = "paging") -> dict:
    index_and_data = {}

    for idx, element in enumerate(list_of_campaign_datas):
        target = element[key]

        if "next" in target:
            url = target["next"]
            json = get_request(url)
            index_and_data[idx] = json

    return index_and_data

def extract_next_url_if_found_after_dictionary(index_and_datas: dict) -> dict:
    new_data = {}

    for key, value in index_and_datas.items():
        if "next" in value["paging"]:
            url_link = value["paging"]["next"]
            json_data = get_request(url_link)
            new_data[key] = json_data["data"]
    
    return new_data

def overwrite_datas_after_extracted_next_url(original_dict: dict, process_dict: dict) -> dict:
    for key in original_dict.keys():
        for index_pos, data in process_dict.items():
            if index_pos == key:
                original_dict[index_pos]["data"].extend(data)
    
    return original_dict

def delete_pagings_when_done_extracting(index_and_datas: dict) -> dict:
    new_index_and_datas = {}

    for key, value in index_and_datas.items():
        value_copy = value.copy()
        del value_copy["paging"]

        new_index_and_datas[key] = value_copy

    return new_index_and_datas

# for the class 
# # because class is being ugly with iteration hhah
# def loop_validator(data, condition: str, combination: list = None):
#         """condition choose: ('get_next' and 'reassign')"""
        
#         if condition == "get_next":
#             data_list = []

#             for element in data:
#                 for idx, key in enumerate(element["adaccounts"]["data"]):
#                     if "campaigns" in key:
#                         target = element["adaccounts"]["data"][idx]["campaigns"]["paging"]

#                         if "next" in target:
#                             x_mark = element["adaccounts"]["data"][idx]["campaigns"]["data"]
#                             data_list.append(x_mark)
#             return data_list
        
#         elif condition == "reassign" and combination is not None:
#             counter = 0

#             for element in data:
#                 for idx, key in enumerate(element["adaccounts"]["data"]):
#                     if "campaigns" in key:
#                         target = element["adaccounts"]["data"][idx]["campaigns"]["paging"]

#                         if "next" in target:
#                             element["adaccounts"]["data"][idx]["campaigns"]["data"] = combination[counter]
#                             counter += 1
                        
#                             if counter >= len(combination):
#                                 break
                
#                 if counter >= len(combination):
#                     break

 # def reassignment_of_values(self):
    #     my_list = [value["data"] for value in self.final_result.values() if self.final_result is not None]
    #     all_data_copy = self.all_data.copy()

    #     all_data_adaccounts_campaigns_with_next_keyword = loop_validator(all_data_copy, condition = "get_next") # list ng dictionary

    #     combined = [
    #         data1 + data2
    #         for data1, data2 in zip(all_data_adaccounts_campaigns_with_next_keyword, my_list)
    #     ]
        
    #     loop_validator(self.all_data, condition = "reassign", combination = combined)

    #     self._delete_pagings() 


# don't delete this is the fallback code: 
# def reassignment_of_values(self) -> None:
    #     my_list = [value["data"] for value in self.final_result.values() if self.final_result is not None]
    #     all_data_copy = self.all_data.copy()
    #     all_data_adaccounts_campaigns_with_next_keyword = []

    #     for element in all_data_copy:
    #         for idx, key in enumerate(element["adaccounts"]["data"]):
    #             if "campaigns" in key:
    #                 target = element["adaccounts"]["data"][idx]["campaigns"]["paging"]

    #                 if "next" in target:
    #                     x_mark = element["adaccounts"]["data"][idx]["campaigns"]["data"]
    #                     all_data_adaccounts_campaigns_with_next_keyword.append(x_mark)
        
    #     # (------------------------------------------------------------------------------)
    #     combined = [
    #         data1 + data2
    #         for data1, data2 in zip(all_data_adaccounts_campaigns_with_next_keyword, my_list)
    #     ]

    #     counter = 0
    #     for element in self.all_data:
    #         for idx, key in enumerate(element["adaccounts"]["data"]):
    #             if "campaigns" in key:
    #                 target = element["adaccounts"]["data"][idx]["campaigns"]["paging"]
                    
    #                 if "next" in target:
    #                     element["adaccounts"]["data"][idx]["campaigns"]["data"] = combined[counter]
    #                     counter += 1

    #                     if counter >= len(combined):
    #                         break
            
    #         if counter >= len(combined):
    #             break
        
    #     self._delete_pagings()