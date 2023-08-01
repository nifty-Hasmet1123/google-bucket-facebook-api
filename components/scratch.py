# my_dict = {"data": [{"name": "shay", "email": "shay@email.com"}], "paging": {"cursor": {"after": "blabla", "before": "blabal"}, "next": "todoList"}}

# # add 3: last name

# my_addition = {
#     "data": [{"name": "DT15", "email": "DT15@email.com"}]
# }

# for key, value in my_dict.items():
#     if key == "data":
#         value.append(my_addition.get("data"))

# print(my_dict)

# master_data
# my_list_dictionary = [
#     {"data": [{"name": "shay", "email": "shay@email.com"}], "paging": {"cursor": {"after": "blabla", "before": "blabal"}, "next": {"data": [{"name": "DT15", "email": "DT15@email.com"}]}}},
#     {"data": [{"name": "bobby", "email": "bobby@gmail.com"}], "paging": {"cursor": {"after": "blabla", "before": "balbalb"}}},
#     {"data": [{"name": "james", "email": "james@email.com"}], "paging": {"cursor": {"after": "blabla", "before": "blabal"}, "next": {"data": [{"name": "JACK15", "email": "JACK15@email.com"}]}}}
# ]

# with_next_keyword = {}
# for idx, element in enumerate(my_list_dictionary):
#     for key, value in element.items():
#         if key == "paging":
#             if "next" in value:
#                 with_next_keyword[idx] = value["next"]

# for idx, element in enumerate(my_list_dictionary):
#     for key, value in with_next_keyword.items():
#         if key == idx:
#             my_list_dictionary[idx]["data"].extend(value["data"])

# print(with_next_keyword, "\n")
# print(my_list_dictionary)


# my_list_dictionary = [
#     {"data": [{"name": "shay", "email": "shay@email.com"}], "paging": {"cursor": {"after": "blabla", "before": "blabal"}, "next": {"data": [{"name": "DT15", "email": "DT15@email.com"}], "paging": {"after": "blabla", "before": "blabla"}, "next": {"data": [{"name": "Jackal15", "email": "Jackal15@email.com"}]}}}},
#     {"data": [{"name": "bobby", "email": "bobby@gmail.com"}], "paging": {"cursor": {"after": "blabla", "before": "balbalb"}}},
#     {"data": [{"name": "james", "email": "james@email.com"}], "paging": {"cursor": {"after": "blabla", "before": "blabal"}, "next": {"data": [{"name": "JACK15", "email": "JACK15@email.com"}]}}}
# ]

# with_next_keyword = {}
# for idx, element in enumerate(my_list_dictionary):
#     for key, value in element.items():
#         if key == "paging":
#             if "next" in value:
#                 with_next_keyword[idx] = value["next"]

# for idx, element in enumerate(my_list_dictionary):
#     for key, value in with_next_keyword.items():
#         if key == idx:
#             my_list_dictionary[idx]["data"].extend(value["data"])

# print(my_list_dictionary)

x = [[{"name": "sage", "daily_budget": 5000, "campaigns": "additional"}]]
y = [[{"name": "bang", "daily_budget": 3000}]]

# print(len(x))

# print(len(y))


# print(x)
# z = [i + j for i, j in zip(x, y)]
# print(z)

# for i, j in zip(x, y):
#     i.append(j)
# print(x)

x = [[{"ad": "me"}, {"a": "test"}, {"b": "test2"}]]
y = [[{"x": "y"}, {"x": "z"}]]


combined = [datas1 + datas2 for datas1, datas2 in zip(x, y)]
print(combined)


# for datas1, datas2 in zip(x, y):
#     for data2 in datas2:
#         datas1.append(data2)
# print(x)