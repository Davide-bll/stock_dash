
# salva un file da url, formato di Deafault è csv
import requests
def save_file_from_url(url, path, fname, format = '.csv'):
    res = requests.get(url, allow_redirects = True)
    file_name = ('%s' + format) % fname
    #file_name = "%s.csv" %fname
    with open(path + '/' + file_name, 'wb') as file:
        file.write(res.content)

# Dashboard functions
def get_options(list_stocks):
    """Create a dictionary from a list of character"""
    dict_list = []
    for i in list_stocks:
        dict_list.append({'label': i, 'value': i})

    return dict_list

##### implement nee function to get option