# handles getting the Api request data and api request from next page ads if there's any.
from typing import Union
import requests
import json

class ApiRequest():
    main_fields = """
    id,name,adaccounts{id,name,currency,amount_spent,campaigns{name,insights{spend,clicks,impressions,cpc,cpm,ctr,actions},daily_budget,budget_rebalance_flag,\
        effective_status,start_time,stop_time,adsets{insights{adset_id,adset_name,date_start,date_stop},ads{name,adcreatives{body},creative{video_id{thumbnails}}},\
            targeting{geo_locations,genders,age_min,age_max,flexible_spec{interests{id,name}}},placement,destination_type,promoted_object{pixel_id}}}}"""

    def __init__(self, access_token: str, profile_id: str, fields = None):
        self._access_token = access_token.replace("\n", "")
        self._fields = fields.replace("\n", "") if fields else self.main_fields
        self.profile_id = profile_id
        self.url = "https://graph.facebook.com"
        self.data = []

    def __call__(self) -> str:
        return "For api requests, execution of response, retrieving and appending next page data"
    
    def __getitem__(self, index):
        return self.data[index] if self.data else None

    @property
    def _create_url(self) -> str:
        return f"{self.url}/v17.0/{self.profile_id}?&access_token={self._access_token}&fields={self._fields}"

    @property
    def _response(self) -> requests:
        return requests.get(self._create_url, timeout = 50)

    def _create_json(self, response: requests) -> str:
        return json.loads(response.text)
    
    def execute_response(self) -> Union[None, str]:
        if self._response.ok:
            json_data = self._create_json(response = self._response)
            self.data.append(json_data)
        else:
            return self._response.text