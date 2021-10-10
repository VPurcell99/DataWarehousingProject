import csv
from decimal import Decimal
from os import system
import random
import datetime
from datetime import date
import math
import sqlite3
from sqlite3 import Error


def write_record(current_date, customer_number, SKU, price, left_in_stock, cases_bought, cur, conn):
    try:
        cur.execute("INSERT INTO Transactions2020 VALUES (?, ?, ?, ?, ?, ?)",
                    (current_date, customer_number, SKU, price,
                     left_in_stock, cases_bought))
    except sqlite3.OperationalError as err:
        print("insert error: %s", err)


csv.register_dialect('piper', delimiter='|', quoting=csv.QUOTE_NONE)

price_multiplier = 1.2
total_items_bought = 0
customer_count = 0

simulation_length = 365
manufacturer_list = []
product_name_list = []
size_list = []
item_type_list = []
sku_list = []
base_price_list = []
stock_list = []
cases_ordered_list = []
left_in_stock = []
cases_bought = []

milk_price = []
milk_sku = []
milk_stock = []
milk_cases = []
# 858 expected daily sales / 6 milk SKUs * 1.5 days
milk_one_and_one_half = 215

cereal_price = []
cereal_sku = []
cereal_stock = []
cereal_cases = []
# 2250 expected daily sales / 93 cereal SKUs * 3 days
cereal_three_day = 73

baby_food_price = []
baby_food_sku = []
baby_food_stock = []
baby_food_cases = []
# 3457 expected daily sales / 162 baby food SKUs * 3 days
baby_food_three_day = 65

diapers_price = []
diapers_sku = []
diapers_stock = []
diapers_cases = []
# 1911 expected daily sales / 82 diaper SKUs * 3 days
diapers_three_day = 70

bread_price = []
bread_sku = []
bread_stock = []
bread_cases = []
# 1535 expected daily sales / 48 bread SKUs * 3 days
bread_three_day = 96

peanut_butter_price = []
peanut_butter_sku = []
peanut_butter_stock = []
peanut_butter_cases = []
# 534 expected daily sales / 20 pb SKUs * 3 days
peanut_butter_three_day = 81

jelly_jam_price = []
jelly_jam_sku = []
jelly_jam_stock = []
jelly_jam_cases = []
# 234 expected daily sales / 4 jelly_jam SKUs * 3 days
jelly_jam_three_day = 176

random_item_price = []
random_item_sku = []
random_item_stock = []
random_item_cases = []
random_item_three_day = 80

all_items = []
stock_and_cases = []
stock = []

with open('Products1.txt', 'r') as csvfile:
    for row in csv.DictReader(csvfile, dialect='piper'):
        nosign = row['BasePrice']
        nosign = float(Decimal(nosign.strip('$')))
        nosign = nosign * price_multiplier
        nosign = round(nosign, 2)
        manufacturer_list.append(row.get('Manufacturer'))
        product_name_list.append(row.get('ProductName'))
        size_list.append(row.get('Size'))
        item_type_list.append(row.get('itemType'))
        sku_list.append(row.get('SKU'))
        base_price_list.append(row.get('BasePrice'))
        stock_list.append(row.get('Stock'))
        cases_ordered_list.append(row.get('CasesOrdered'))
        if row['itemType'] == 'Milk':
            milk_price.append(nosign)
            milk_sku.append(row['SKU'])
            cases = math.ceil(milk_one_and_one_half / 12)
            milk_cases.append(cases)
            milk_stock.append(cases * 12)
        elif row['itemType'] == 'Cereal':
            cereal_price.append(nosign)
            cereal_sku.append(row['SKU'])
            cases = math.ceil(cereal_three_day / 12)
            cereal_cases.append(cases)
            cereal_stock.append(cases * 12)
        elif row['itemType'] == 'Baby Food':
            baby_food_price.append(nosign)
            baby_food_sku.append(row['SKU'])
            cases = math.ceil(baby_food_three_day / 12)
            baby_food_cases.append(cases)
            baby_food_stock.append(cases * 12)
        elif row['itemType'] == 'Diapers':
            diapers_price.append(nosign)
            diapers_sku.append(row['SKU'])
            cases = math.ceil(diapers_three_day / 12)
            diapers_cases.append(cases)
            diapers_stock.append(cases * 12)
        elif row['itemType'] == 'Bread':
            bread_price.append(nosign)
            bread_sku.append(row['SKU'])
            cases = math.ceil(bread_three_day / 12)
            bread_cases.append(cases)
            bread_stock.append(cases * 12)
        elif row['itemType'] == 'Peanut Butter':
            peanut_butter_price.append(nosign)
            peanut_butter_sku.append(row['SKU'])
            cases = math.ceil(peanut_butter_three_day / 12)
            peanut_butter_cases.append(cases)
            peanut_butter_stock.append(cases * 12)
        elif row['itemType'] == 'Jelly/Jam':
            jelly_jam_price.append(nosign)
            jelly_jam_sku.append(row['SKU'])
            cases = math.ceil(jelly_jam_three_day / 12)
            jelly_jam_cases.append(cases)
            jelly_jam_stock.append(cases * 12)
        else:
            if (row['itemType'] != 'Milk' and row['itemType'] != 'Cereal' and row['itemType'] != 'Baby Food' and row[
                'itemType'] != 'Diapers' and row['itemType'] != 'Bread' and row['itemType'] != 'Peanut Butter' and row[
                'itemType'] != 'Jelly/Jam'):
                random_item_price.append(nosign)
                random_item_sku.append(row['SKU'])
                cases = math.ceil(random_item_three_day / 12)
                random_item_cases.append(cases)
                random_item_stock.append(cases * 12)

def get_milk_sku_and_price_stock_cases():
    random_index = random.randrange(len(milk_sku))
    milk_stock[random_index] = milk_stock[random_index] - 1
    if milk_stock[random_index] < 0:
        milk_stock[random_index] = 0
        return get_milk_sku_and_price_stock_cases()
    else:
        return milk_sku[random_index], milk_price[random_index], milk_stock[random_index], milk_cases[random_index]


def get_cereal_sku_and_price_stock_cases():
    random_index = random.randrange(len(cereal_sku))
    cereal_stock[random_index] = cereal_stock[random_index] - 1
    if cereal_stock[random_index] < 0:
        cereal_stock[random_index] = 0
        return get_cereal_sku_and_price_stock_cases()
    else:
        return cereal_sku[random_index], cereal_price[random_index], cereal_stock[random_index], cereal_cases[random_index]


def get_baby_food_sku_and_price_stock_cases():
    random_index = random.randrange(len(baby_food_sku))
    baby_food_stock[random_index] = baby_food_stock[random_index] - 1
    if baby_food_stock[random_index] < 0:
        baby_food_stock[random_index] = 0
        return get_baby_food_sku_and_price_stock_cases()
    else:
        return baby_food_sku[random_index], baby_food_price[random_index], baby_food_stock[random_index], baby_food_cases[random_index]


def get_diapers_sku_and_price_stock_cases():
    random_index = random.randrange(len(diapers_sku))
    diapers_stock[random_index] = diapers_stock[random_index] - 1
    if diapers_stock[random_index] < 0:
        diapers_stock[random_index] = 0
        return get_diapers_sku_and_price_stock_cases()
    else:
        return diapers_sku[random_index], diapers_price[random_index], diapers_stock[random_index], diapers_cases[random_index]


def get_bread_sku_and_price_stock_cases():
    random_index = random.randrange(len(bread_sku))
    bread_stock[random_index] = bread_stock[random_index] - 1
    if bread_stock[random_index] < 0:
        bread_stock[random_index] = 0
        return get_bread_sku_and_price_stock_cases()
    else:
        return bread_sku[random_index], bread_price[random_index], bread_stock[random_index], bread_cases[random_index]


def get_peanut_butter_sku_and_price_stock_cases():
    random_index = random.randrange(len(peanut_butter_sku))
    peanut_butter_stock[random_index] = peanut_butter_stock[random_index] - 1
    if peanut_butter_stock[random_index] < 0:
        peanut_butter_stock[random_index] = 0
        return get_peanut_butter_sku_and_price_stock_cases()
    else:
        return peanut_butter_sku[random_index], peanut_butter_price[random_index], peanut_butter_stock[random_index], peanut_butter_cases[random_index]


def get_jelly_jam_sku_and_price_stock_cases():
    random_index = random.randrange(len(jelly_jam_sku))
    jelly_jam_stock[random_index] = jelly_jam_stock[random_index] - 1
    if jelly_jam_stock[random_index] < 0:
        jelly_jam_stock[random_index] = 0
        return get_jelly_jam_sku_and_price_stock_cases()
    else:
        return jelly_jam_sku[random_index], jelly_jam_price[random_index], jelly_jam_stock[random_index], jelly_jam_cases[random_index]


def get_random_item_sku_and_price_stock_cases():
    random_index = random.randrange(len(random_item_sku))
    random_item_stock[random_index] = random_item_stock[random_index] - 1
    if random_item_stock[random_index] < 0:
        random_item_stock[random_index] = 0
        return get_random_item_sku_and_price_stock_cases()
    else:
        return random_item_sku[random_index], random_item_price[random_index], random_item_stock[random_index], random_item_cases[random_index]


def order_milk():
    for stock in range(0, len(milk_sku)):
        if milk_stock[stock] < milk_one_and_one_half:
            difference = milk_one_and_one_half - milk_stock[stock]
            cases_needed = math.ceil(difference / 12)
            milk_stock[stock] = milk_stock[stock] + cases_needed * 12
            milk_cases[stock] = milk_cases[stock] + cases_needed


def order_cereal():
    for stock in range(0, len(cereal_sku)):
        if cereal_stock[stock] < cereal_three_day:
            difference = cereal_three_day - cereal_stock[stock]
            cases_needed = math.ceil(difference / 12)
            cereal_stock[stock] = cereal_stock[stock] + cases_needed * 12
            cereal_cases[stock] = cereal_cases[stock] + cases_needed


def order_peanut_butter():
    for stock in range(0, len(peanut_butter_sku)):
        if peanut_butter_stock[stock] < peanut_butter_three_day:
            difference = peanut_butter_three_day - peanut_butter_stock[stock]
            cases_needed = math.ceil(difference / 12)
            peanut_butter_stock[stock] = peanut_butter_stock[stock] + cases_needed * 12
            peanut_butter_cases[stock] = peanut_butter_cases[stock] + cases_needed


def order_jelly():
    for stock in range(0, len(jelly_jam_sku)):
        if jelly_jam_stock[stock] < jelly_jam_three_day:
            difference = jelly_jam_three_day - jelly_jam_stock[stock]
            cases_needed = math.ceil(difference / 12)
            jelly_jam_stock[stock] = jelly_jam_stock[stock] + cases_needed * 12
            jelly_jam_cases[stock] = jelly_jam_cases[stock] + cases_needed


def order_baby_food():
    for stock in range(0, len(baby_food_sku)):
        if baby_food_stock[stock] < baby_food_three_day:
            difference = baby_food_three_day - baby_food_stock[stock]
            cases_needed = math.ceil(difference / 12)
            baby_food_stock[stock] = baby_food_stock[stock] + cases_needed * 12
            baby_food_cases[stock] = baby_food_cases[stock] + cases_needed


def order_diapers():
    for stock in range(0, len(diapers_sku)):
        if diapers_stock[stock] < diapers_three_day:
            difference = diapers_three_day - diapers_stock[stock]
            cases_needed = math.ceil(difference / 12)
            diapers_stock[stock] = diapers_stock[stock] + cases_needed * 12
            diapers_cases[stock] = diapers_cases[stock] + cases_needed


def order_bread():
    for stock in range(0, len(bread_sku)):
        if bread_stock[stock] < bread_three_day:
            difference = bread_three_day - bread_stock[stock]
            cases_needed = math.ceil(difference / 12)
            bread_stock[stock] = bread_stock[stock] + cases_needed * 12
            bread_cases[stock] = bread_cases[stock] + cases_needed


def order_random_items():
    for stock in range(0, len(random_item_sku)):
        if random_item_stock[stock] < random_item_three_day:
            difference = random_item_three_day - random_item_stock[stock]
            cases_needed = math.ceil(difference / 12)
            random_item_stock[stock] = random_item_stock[stock] + cases_needed * 12
            random_item_cases[stock] = random_item_cases[stock] + cases_needed


try:
    # if grocery.db exists connect to it, otherwise create it
    # one change i want is to have the rocery.db file write into the SQLite folder
    conn = sqlite3.connect('Grocery.db')


except Error as e:
    print("Error %s:" % e.args[0])
    system.exit(1)

finally:
    if conn:
        cur = conn.cursor()
        cur.execute("DROP TABLE IF EXISTS Transactions2020")
        cur.execute("CREATE TABLE Transactions2020 (current_date TEXT, customer_number INT, SKU TEXT, price FLOAT, "
                    "left_in_stock INT, cases_bought INT)")

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

for iday in range(0, simulation_length):
    print("Working on Day ", iday + 1)
    increase = 0
    current_date += datetime.timedelta(1)
    if current_date.weekday() >= 5:
        increase = weekend_increase

    order_milk()

    if current_date.weekday() == 1 or current_date.weekday() == 3 or current_date.weekday() == 5:
        order_cereal()
        order_baby_food()
        order_bread()
        order_diapers()
        order_jelly()
        order_peanut_butter()
        order_random_items()

    daily_customers = random.randint(customers_low + increase, customers_high + increase)
    customer_number = 1

    while customer_number <= daily_customers:
        customer_count = customer_count + 1
        my_items = random.randint(1, maximum_items)
        k = 0
        if random.randint(1, 100) <= 70:
            SKU, price, left_in_stock, cases_bought = get_milk_sku_and_price_stock_cases()
            write_record(current_date, customer_number, SKU, price, left_in_stock, cases_bought, cur, conn)
            k += 1

            if random.randint(1, 100) <= 50:
                SKU, price, left_in_stock, cases_bought = get_cereal_sku_and_price_stock_cases()
                write_record(current_date, customer_number, SKU, price, left_in_stock, cases_bought, cur, conn)
                k += 1

        else:
            if random.randint(1, 100) <= 5:
                SKU, price, left_in_stock, cases_bought = get_cereal_sku_and_price_stock_cases()
                write_record(current_date, customer_number, SKU, price, left_in_stock, cases_bought, cur, conn)
                k += 1

        if random.randint(1, 100) <= 20:
            SKU, price, left_in_stock, cases_bought = get_baby_food_sku_and_price_stock_cases()
            write_record(current_date, customer_number, SKU, price, left_in_stock, cases_bought, cur, conn)
            k += 1

            if random.randint(1, 100) <= 80:
                SKU, price, left_in_stock, cases_bought = get_diapers_sku_and_price_stock_cases()
                write_record(current_date, customer_number, SKU, price, left_in_stock, cases_bought, cur, conn)
                k += 1

        else:
            if random.randint(1, 100) <= 1:
                SKU, price, left_in_stock, cases_bought = get_diapers_sku_and_price_stock_cases()
                write_record(current_date, customer_number, SKU, price, left_in_stock, cases_bought, cur, conn)
                k += 1

        if random.randint(1, 100) <= 50:
            SKU, price, stock, cases = get_bread_sku_and_price_stock_cases()
            write_record(current_date, customer_number, SKU, price, left_in_stock, cases_bought, cur, conn)
            k += 1

        if random.randint(1, 100) <= 10:
            SKU, price, left_in_stock, cases_bought = get_peanut_butter_sku_and_price_stock_cases()
            write_record(current_date, customer_number, SKU, price, left_in_stock, cases_bought, cur, conn)
            k += 1

            if random.randint(1, 100) <= 90:
                SKU, price, left_in_stock, cases_bought = get_jelly_jam_sku_and_price_stock_cases()
                write_record(current_date, customer_number, SKU, price, left_in_stock, cases_bought, cur, conn)
                k += 1

        else:
            if random.randint(1, 100) <= 5:
                SKU, price, left_in_stock, cases_bought = get_jelly_jam_sku_and_price_stock_cases()
                write_record(current_date, customer_number, SKU, price, left_in_stock, cases_bought, cur, conn)
                k += 1

        while k < my_items:
            SKU, price, left_in_stock, cases_bought = get_random_item_sku_and_price_stock_cases()
            write_record(current_date, customer_number, SKU, price, left_in_stock, cases_bought, cur, conn)
            k += 1

        customer_number = customer_number + 1
    conn.commit()
conn.close()