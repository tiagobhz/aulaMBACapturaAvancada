import os
import pickle
import json
import requests
import matplotlib.pyplot as plt
import urllib.request
from bs4 import BeautifulSoup as BS
from zipfile import ZipFile

url = 'https://www.google.com/googlebooks/uspto-patents-grants-text.html'
response = urllib.request.urlopen(url)
response.status


soup = BS(response, 'html5lib')


alguns = soup.find_all('a', href=True)


alguns2 = [l.get('href') for l in alguns if 'http' in l.get('href')]


links_gft1 = [n for n in alguns2 if 'grant_full_text' in n]


links_gft2 = [n for n in links_gft1 if '.zip' in n]


from collections import defaultdict


my_dict = defaultdict(list)


for ano in range(1997,2016):
  for link in links_gft2:
    if str(ano) in link:
      my_dict[ano].append(link)


my_dict2 = {k:sum(1 for x in v if x) for k,v in my_dict.items()}


my_dict3 = sum(my_dict2.values())


for key, value in my_dict2.items() :
    print (f'No ano de {key} haviam {value} patentes')


print(f'Quantidade total de arquivos zip: {my_dict3}')


plt.figure(figsize=(20,6))
plt.xticks(rotation=90)
plt.bar(my_dict2.keys(), my_dict2.values(), width=0.8, color='r')


if not os.path.exists('data'):
    os.mkdir('data')


def save_pickle(ob, name):
    with open(name, 'wb') as handler:
        pickle.dump(ob, handler)
    print('Salvo!!!')

save_pickle(my_dict, 'data/pyckle_my_dict')
save_pickle(my_dict2, 'data/pyckle_my_dict2')


json_object1 = json.dumps(my_dict)
json_object2 = json.dumps(my_dict2)


def save_json(ob, filename):
    with open(filename, 'w') as handler:
        json.dump(ob, handler)
    print(f'Salvo! Verifique em {filename}')


save_json(json_object1, 'data/json1.json')
save_json(json_object2, 'data/json2.json')


lista1 = list(my_dict.values())[0]


lista2 = lista1[0]


name = lista2.split('/')[6]


r = requests.get(lista2)
with open(f'data/{name}', 'wb') as handler:
    handler.write(r.content)


if not os.path.exists('temp'):
    os.mkdir('temp')


with ZipFile(f'data/{name}', 'r') as zipObj:
   zipObj.extractall('temp')


datasize = defaultdict(list)
ano = [1997, 1998]
for key, values in my_dict.items():
  if key in ano:
    for value in values:
      with urllib.request.urlopen(value) as handler:
        datasize[key].append(int(handler.getheader('Content-Length')))


datasize2 = defaultdict(list)
for key in datasize:
  datasize2[key] = [sum(datasize[key])]
print(datasize2)