#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 20 22:03:02 2018

@author: rakesh
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def get_item_code(item, item_list) :
    item_code = None
    for index, row in item_list.iterrows() :
        if(row["item"] == item) :
            item_code = row['item_code']
            break
    return item_code
    


order_data = pd.read_csv("output.txt",parse_dates=True,infer_datetime_format=True,delimiter="|")
print(order_data.head())
order_data["date"] = pd.to_datetime(order_data["order_date"],format='%m%d%Y')


#
# Create list of items

# generate code for each generic and attach it back to the main dataframe
item_list = order_data["general_type"]
#item_list = item_list.drop_duplicates(keep=False)
item_list = pd.DataFrame({'item_code' : np.arange(len(item_list)), 
                          'item' : item_list}).reset_index()
code_seq = []
for index, row in order_data.iterrows() :
    item_code = get_item_code(row['general_type'], item_list)
    code_seq.append(item_code)
order_data["item_code"] = pd.Series(code_seq,index=order_data.index)

# Next we determine how frequently the items are purchased
purchase_freq = {}
last_pur_days_seq = []
for index, row in order_data.iterrows() :
    generic = row['general_type']
    last_purchase_date = row['date']
    if purchase_freq.get(generic) != None :
        prev_purchase = purchase_freq[generic]['last_purchase']
        delta = last_purchase_date - prev_purchase
        purchase_freq[generic]['avg_days'].append(delta.days)
        purchase_freq[generic]['last_purchase'] = last_purchase_date
        last_pur_days_seq.append(delta.days)
    else :
        purchase_freq[generic] = dict(
                avg_days=[],
                last_purchase=last_purchase_date
                )
        last_pur_days_seq.append(0)
        
order_data["days_since_last_pur"] = pd.Series(last_pur_days_seq,index=order_data.index)

# Data Summary Below
item_data = pd.DataFrame({'item_totals' : order_data.groupby(["item_code"])['item_code'].count(), 
                          'general_type' : order_data["general_type"],
                          'avg_pur_days' : order_data.groupby(["item_code"])['days_since_last_pur'].sum()/order_data.groupby(["item_code"])['days_since_last_pur'].count()
                         })

plt.figure(1, figsize=(30, 5))
plt.xticks(rotation=90)
plt.scatter(data = item_data, x = 'general_type', y = 'avg_pur_days')


order_data.to_csv("order_data.csv",sep='|')
item_data.to_csv("item_data.csv",sep='|')
print("done...")