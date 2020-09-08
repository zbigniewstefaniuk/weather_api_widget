import json

with open('city.list.json', encoding="utf8") as f:
    data = json.load(f)


lst = {}
list_of_cities = {}
for item in data:
    state = item['country']
    city = item['name']

    if state == 'PL' and 'Powiat' not in city:

        print(state, city)
        lst['country'] = state
        lst['city'] = city
        list_of_cities.update(lst)

print(list_of_cities)
lst_json = json.dumps(list_of_cities)
