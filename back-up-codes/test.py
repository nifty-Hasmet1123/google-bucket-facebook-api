import json
import requests
import os

url = "https://storage.googleapis.com/hkecommercedata/shopify-orders/shopify_orders.json"

def main(filename: str, directory_path: str):
    try:
        my_list = []
        response = requests.get(url, timeout = 20)
        my_json_data = response.json()
        my_list.append(my_json_data)

        file_path = os.path.join(directory_path, filename)

        with open(file_path, "w") as file:
            file.write(json.dumps(my_list, indent = 2))
    except Exception:
        print("Error")
    else:
        print("Success")
    
main(filename="shopify_campaigns.json", directory_path="D:\python_project\json")