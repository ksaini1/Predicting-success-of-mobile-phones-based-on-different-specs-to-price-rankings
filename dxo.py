import bs4 as bs
import urllib.request
import pandas as pd
import csv

sauce=urllib.request.urlopen('https://www.dxomark.com/category/mobile-reviews/').read()
#https://www.antutu.com/en/ranking/rank1.htm
#https://www.antutu.com/en/ranking/ios1.htm
#https://smartphonesrevealed.com/the-best-smartphones/?showall=true
#https://www.dxomark.com/category/mobile-reviews/
soup =bs.BeautifulSoup(sauce,'lxml')
#print(soup.get_text())
body=soup.body
model=[]
score=[]
fin=[]
for div in body.find_all('div', class_="deviceName sensor"):
#    print(div.text)
    model.append(div.text)

#print(model)

for div in body.find_all('div', class_="deviceScore"):
#    print(div.text)
    score.append(div.text)

def merge(list1, list2):
  merged_list = [(list1[i], list2[i]) for i in range(0, len(list1))]
  return merged_list


#print(score)
fin=merge(model,score)
print(fin)

with open('dxo.csv', 'a') as outcsv:
   #configure writer to write standard csv file
       writer = csv.writer(outcsv, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
       writer.writerow(['Phone', 'Score'])
       for item in fin:
       #Write item to outcsv
           writer.writerow([item[0], item[1]])
#writer.writerow(line.strip())
