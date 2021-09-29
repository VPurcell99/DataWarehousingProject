import csv
from decimal import Decimal
import random
import datetime
from datetime import date
from collections import Counter

csv.register_dialect('piper', delimiter= '|', quoting = csv.QUOTE_NONE)

price_multiplier = 1.2
total_items_bought = 0
customer_count = 0

manufacturer_list = []
product_name_list = []
size_list = []
item_type_list = []
sku_list = []
base_price_list = []

milk_price = []
milk_sku = []

cereal_price = []
cereal_sku = []

baby_food_price = []
baby_food_sku = []

diapers_price = []
diapers_sku = []

bread_price = []
bread_sku = []

peanut_butter_price = []
peanut_butter_sku = []

jelly_jam_price = []
jelly_jam_sku = []

all_items = []

with open('Products1.txt', 'r') as csvfile:
   for row in csv.DictReader(csvfile, dialect= 'piper'):
      nosign = row['BasePrice']
      nosign = float(Decimal(nosign.strip('$')))
      nosign = nosign*price_multiplier
      manufacturer_list.append(row.get('Manufacturer'))
      product_name_list.append(row.get('ProductName'))
      size_list.append(row.get('Size'))
      item_type_list.append(row.get('itemType'))
      sku_list.append(row.get('SKU'))
      base_price_list.append(row.get('BasePrice'))
      if (row['itemType'] == 'Milk'):
         milk_price.append(nosign)
         milk_sku.append(row['SKU'])     
      elif (row['itemType'] == 'Cereal'):
            cereal_price.append(nosign)
            cereal_sku.append(row['SKU'])                         
      elif (row['itemType'] == 'Baby Food'):              
            baby_food_price.append(nosign)
            baby_food_sku.append(row['SKU'])                           
      elif (row['itemType'] == 'Diapers'):
            diapers_price.append(nosign)
            diapers_sku.append(row['SKU'])                        
      elif (row['itemType'] == 'Bread'):
            bread_price.append(nosign)
            bread_sku.append(row['SKU'])                        
      elif (row['itemType'] == 'Peanut Butter'):
            peanut_butter_price.append(nosign)
            peanut_butter_sku.append(row['SKU'])
      else:
         if (row['itemType'] == 'Jelly/Jam'):
            jelly_jam_price.append(nosign)
            jelly_jam_sku.append(row['SKU'])
      
output_writer = csv.DictWriter(open('PurchaseHistory.csv', 'w'), fieldnames = ['date', 'customer_id', 'sku', 'sale_price'])
output_writer.writeheader()
                                                                       
def write_record(date_bought, customer_id, sku, sale_price):
   global total_items_bought
   global all_items
   all_items.append(sku)
   total_items_bought = total_items_bought + 1
   global output_writer
   row_to_add = {
            'date': date_bought.isoformat(),
            'customer_id': customer_id,
            'sku': sku,
            'sale_price': sale_price}
   output_writer.writerow(row_to_add)

def get_milk_sku_and_price():
   random_index = random.randrange(len(milk_sku))
   return milk_sku[random_index], milk_price[random_index]

def cereal_sku_and_price():
   random_index = random.randrange(len(cereal_sku))
   return cereal_sku[random_index], cereal_price[random_index]

def baby_food_sku_and_price():
   random_index = random.randrange(len(baby_food_sku))
   return baby_food_sku[random_index], baby_food_price[random_index]

def diapers_sku_and_price():
   random_index = random.randrange(len(diapers_sku))
   return diapers_sku[random_index], diapers_price[random_index]

def bread_sku_and_price():
   random_index = random.randrange(len(bread_sku))
   return bread_sku[random_index], bread_price[random_index]

def peanut_butter_sku_and_price():
   random_index = random.randrange(len(peanut_butter_sku))
   return peanut_butter_sku[random_index], peanut_butter_price[random_index]

def jelly_jam_sku_and_price():
   random_index = random.randrange(len(jelly_jam_sku))
   return jelly_jam_sku[random_index], jelly_jam_price[random_index]

def get_random_item_sku_and_price():
   random_index = random.randrange(len(sku_list))
   return sku_list[random_index], base_price_list[random_index]



customers_low = 1020
customers_high = 1060
weekend_increase = 50
maximum_items = 80
simulation_start_date = date(2020, 1, 1)
simulation_end_date = date(2020, 12, 31)
current_date = simulation_start_date
daily_customers = 0
my_items = 0
customer_number = 1

for iday in range(0,364):
    increase = 0
    current_date += datetime.timedelta(1)
    if current_date.weekday() >= 5:
        increase = weekend_increase

    daily_customers = random.randint(customers_low + increase, customers_high + increase)
    customer_number = 1

    while customer_number <= daily_customers:
        customer_count = customer_count + 1
        my_items = random.randint(1, maximum_items)
        k = 0
        if random.randint(1,100) <= 70:
            SKU, price = get_milk_sku_and_price()
            write_record(current_date,customer_number,SKU,price)
            k += 1

            if random.randint(1,100) <= 50:
                SKU, price = cereal_sku_and_price()
                write_record(current_date, customer_number, SKU, price)
                k += 1

        else:
            if random.randint(1,100) <= 5:
                SKU, price = cereal_sku_and_price()
                write_record(current_date, customer_number, SKU, price)
                k += 1

        if random.randint(1,100) <= 20:
            SKU, price = baby_food_sku_and_price()
            write_record(current_date,customer_number,SKU,price)
            k += 1
         
            if random.randint(1,100) <= 80:
                SKU, price = diapers_sku_and_price()
                write_record(current_date, customer_number, SKU, price)
                k += 1

        else:
            if random.randint(1,100) <= 1:
                SKU, price = diapers_sku_and_price()
                write_record(current_date, customer_number, SKU, price)
                k +=1

        if random.randint(1,100) <= 50:
            SKU, price = bread_sku_and_price()
            write_record(current_date,customer_number,SKU,price)
            k += 1

        if random.randint(1,100) <= 10:
            SKU, price = peanut_butter_sku_and_price()
            write_record(current_date,customer_number,SKU,price)
            k += 1

            if random.randint(1,100) <= 90:
                SKU, price = jelly_jam_sku_and_price()
                write_record(current_date, customer_number, SKU, price)
                k += 1

        else:
            if random.randint(1,100) <= 5:
                SKU, price = jelly_jam_sku_and_price()
                write_record(current_date, customer_number, SKU, price)
                k += 1

        while k < my_items:
            SKU, price  = get_random_item_sku_and_price()
            write_record(current_date, customer_number, SKU, price)
            k += 1

        customer_number = customer_number + 1 


print("Summary")
print("Customer count and total sales is " + str(customer_count))
print("Total items bought is " + str(total_items_bought))
c = Counter(all_items)
print("Top 10 most common SKUs is " + str(c.most_common(10)))

