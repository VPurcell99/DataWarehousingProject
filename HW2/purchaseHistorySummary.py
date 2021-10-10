# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% [markdown]
# # Team 5 Purchase History Summary #
# Data Warehousing - Fall 21
# 
# Team 5: Vince Purcell, Brandon Mondile

# %%
import csv
from decimal import Decimal
import random
import datetime
from datetime import date
from collections import Counter
import sqlite3 as lite

# %% [markdown]
# ## Create Table with SKUs and Item names ##
# This table will be used for item name lookup by SKU

# %%
csv.register_dialect('piper', delimiter= '|', quoting = csv.QUOTE_NONE)

con = lite.connect(r'grocery_store.db')

cur = con.cursor()

cur.execute('drop table if exists itemLookup')
cur.execute('create Table itemLookup(itemstr TEXT, sku INT)')

with open('Products1.txt', 'r') as csvfile:
    for row in csv.DictReader(csvfile, dialect= 'piper'):
        sku = int(row['SKU'])
        itemstr = str(row['Manufacturer']) + " " + str(row['Product Name']) + " (" + str(row['itemType']) + ")"
        try:
            cur.execute("INSERT INTO itemLookup VALUES (?,?)",
                        (itemstr, sku))
        except lite.OperationalError as err:
            print("insert error: %s", err)
            break

con.commit()
con.close()      

# %% [markdown]
# ## Create Table of Purchase History CSV produced from Leonchuk code ##
# SQLite database with Date, Customer ID, SKU, and Sale price for generated sales

# %%
con = lite.connect(r'grocery_store.db')

cur = con.cursor()

cur.execute('drop table if exists purchaseHistory')
cur.execute('create Table purchaseHistory(date TEXT, customer_id INT, sku INT, sale_price TEXT)')
count = 1
customer_count = 0
curr_id = '0'
with open('PurchaseHistory.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:

        prev_id = curr_id
        curr_id = row['customer_id']
        if prev_id != curr_id:
            customer_count = customer_count + 1

        if ((count % 20000)==0):
            con.commit()
        price = row['sale_price']

        if price[0] == '$':
            price = price[1:]
            
        try:
            cur.execute("INSERT INTO purchaseHistory VALUES (?,?,?,?)",
                        (str(row['date']), int(row['customer_id']), int(row['sku']), str(price)))
            count = count + 1
        except lite.OperationalError as err:
            print("insert error: %s", err)
            break

con.commit()
con.close() 

# %% [markdown]
# ## Count Total Customers and Sales ##

# %%
con = lite.connect(r'grocery_store.db')
cur = con.cursor()
s = 'select count(customer_id) from purchaseHistory'
cur.execute(s)
query = cur.fetchall()
total_items = query[0][0]
con.close()

# %% [markdown]
# ## Get count of most common SKUs and print summary ##

# %%
print("Summary\n----------------------------------------------------")
print("Customer Count and Total Sales: " + str(customer_count) + "\n")
print("Total items bought: " + str(total_items) + "\n")

con = lite.connect(r'grocery_store.db')
cur = con.cursor()
s = 'select count(sku) as cnt1, sku from purchaseHistory group by sku order by cnt1 DESC limit 10'
cur.execute(s)
rows = cur.fetchall()
print("Most Popular Items by SKU")
print('Count - SKU      - Item Name')
for row in rows:
    s = 'select itemstr from itemLookup where sku like ' + str(row[1])
    cur.execute(s)
    item = cur.fetchall()
    print(str(row[0]) + " - " + str(row[1]) + " - " + item[0][0])
con.close()


