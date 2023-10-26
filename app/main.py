from fastapi import FastAPI
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl

app = FastAPI()


@app.get("/ping")
def pong():
  return {"pinafasfg": "pong!"}


#====DATA PROCESSING====#

# load data
past_orders_df = pd.read_csv("data/pastorders.csv")
stock_df = pd.read_csv("data/stock.csv")

# order dataframe by date
past_orders_df['Order Date'] = pd.to_datetime(past_orders_df['Order Date'])
past_orders_df.sort_values(by='Order Date', inplace = True)

# list of products
product_list = stock_df["SKU ID"].values
print(product_list)

# ===== plot stock graph ======
item_sku = "2573CA"
item_df = past_orders_df.loc[past_orders_df['SKU ID'] == item_sku]

# sum total purchased
total_purchased = item_df["Order Quantity"].sum()

# get item from stock
item_current = stock_df.loc[stock_df["SKU ID"] == item_sku]

# current quantity of item
quantity_current = item_current["Current Stock Quantity"].values[0]

# starting quantity
opening_quantity = total_purchased+quantity_current

# calculate stock levels
quantity_copy = opening_quantity

stock_dict = []

date_list = []
quantity_list = []

for i, row in item_df.iterrows():
  amount_bought = row["Order Quantity"]
  quantity_copy -= amount_bought
  date = row["Order Date"]

  date_list.append(date)
  quantity_list.append(quantity_copy)

stock_levels_df = pd.DataFrame({"Date": date_list, "Quantity": quantity_list})

plot = stock_levels_df.plot(x="Date", y="Quantity")

#plt.show()




