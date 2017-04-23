import requests


wiki = input('Wikipedia quick search: ')
wiki_results = []

api_url = "https://en.wikipedia.org/w/api.php"

params = {
    'action': 'opensearch',
    'search': wiki,
    'format': 'json'}

raw = requests.get(api_url, params=params)
search_request = raw.json()[0]
results_match = raw.json()[1]
results_info = raw.json()[2]
results_links = raw.json()[3]
print("On a \"{}\" request found - {} - results:".format(search_request, len(results_match)))
for result in results_match:
    print('', result)
choice = input("Print results' short info? [y/n]: ")
if choice == 'y':
    for r, i, l in zip(results_match, results_info, results_links):
        wiki_results.append([r, i, l])
        print("\nFound: {}\nShort Info: {}\nLink: {}".format(r,i,l))
