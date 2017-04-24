import requests
import pprint as p


def seeker(dictionary, wanted):
    if isinstance(dictionary, dict):
        if wanted in dictionary.keys():
            found = dictionary[wanted]
        else:
            for key in dictionary.keys():
                found = seeker(dictionary[key], wanted)
                if found:
                    break
        return found
    else:
        return None

wiki = input('Wikipedia quick search: ')
wiki_results = list()
wiki_article = str()

api_url = "https://en.wikipedia.org/w/api.php"

search_params = {
    'action': 'opensearch',
    'search': wiki,
    'format': 'json'}

raw = requests.get(api_url, params=search_params)
search_request = raw.json()[0]
results_match = raw.json()[1]
results_info = raw.json()[2]
results_links = raw.json()[3]

print("On a \"{}\" request found - {} - results:".format(search_request, len(results_match)))
for result in results_match:
    print('', result)

choice = None
while choice != 'y' and choice != 'n':
    choice = input("Print results' short info? [y/N]: ").lower()
    if not choice:
        choice = 'n'
if choice == 'y':
    for r, i, l in zip(results_match, results_info, results_links):
        wiki_results.append([r, i, l])
        print("\nFound: {}\nShort Info: {}\nLink: {}".format(r, i, l))

article = input(
    "Do you wish to specify wiki-request? (Press \"Enter\" if not, otherwise - type a word): ")

article_params = {
    'action': 'query',
    'prop': 'extracts',
    'explaintext': '',
    'redirects': 1,
    'titles': article,
    'format': 'json'}

if article:
    specify = requests.get(api_url, params=article_params)
    print(specify.headers['Content-Type'])
    print()
    wiki_article = seeker(specify.json(), 'extract')
    print(wiki_article)
