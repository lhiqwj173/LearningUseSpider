# 有时候跑一次不出数据或漏出，建议多跑几次

bangumi_id_name是用pickle封装的dict

解包：
```
import pickle, pprint
with open('xxxxxx', 'rb') as file:
    d = pickle.load(file)
   
pprint.pprint(d)
```
