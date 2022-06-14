import pandas as pd
import re
import random
import numpy as np
import datetime


ingredient_total_amount = 6 # x 100g
#number_of_ingredients = random.randint(5,10)
include_ingredients = '(fresh, boiled, drained|Oil, olive|Sardines)'
spreadsheet_name = "ingredients.csv"

pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', 50)


df = pd.read_csv(spreadsheet_name)
df.columns = [x.replace("\n", "") for x in df.columns.to_list()]

df = df[df['Food Name'].str.contains(include_ingredients, case=False)]

micronutrients = [
                    'Biotin (B7) (ug)',
                    'Calcium (Ca) (mg)',
                    'Chloride (Cl) (mg)',
                    'Chromium (Cr) (ug)',
                    'Cobalamin (B12) (ug)',
                    'Cobalt (Co) (ug)',
                    'Copper (Cu) (mg)',
                    'Fluoride (F) (ug)',
                    'Folic acid (ug)',
                    'Iodine (I) (ug)',
                    'Iron (Fe) (mg)',
                    'Magnesium (Mg) (mg)',
                    'Manganese (Mn) (mg)',
                    'Niacin (B3) (mg)',
                    'Pantothenic acid (B5) (mg)',
                    'Phosphorus (P) (mg)',
                    'Phosphorus (P) (mg)',
                    'Potassium (K) (mg)',
                    'Pyridoxine (B6) (mg)',
                    'Riboflavin (B2) (mg)',
                    'Selenium (Se) (ug)',
                    'Thiamin (B1) (mg)',
                    'Vitamin A retinol equivalents (ug)',
                    'Vitamin C (mg)',
                    'Vitamin D3 equivalents (ug)',
                    'Vitamin E (mg)',
                    'Zinc (Zn) (mg)'
                ]


targets = {
    "carbs": 200,
    "carbs_max": 500,
    "protein": 50,
    "protein_max": 100,
    "fat": 50,
    "fat_max": 150,
}


def multiply_columns(column, weights):
    return column * weights



for i in range(10000):
    print(f"====== Random Recipe Number : {i} ========")
    #number_of_ingredients = random.randint(0,10)
    number_of_ingredients = random.randint(5,10)
    print(f"Number of Ingredients : {number_of_ingredients}")
    ingredients_df = df.sample(n = number_of_ingredients)
    ingredients_df = ingredients_df[["Food Name","Available carbohydrate, without sugar alcohols (g)","Protein (g)","Fat, total (g)"]]
    ingredients_df["amount"] = 0
    

    ingredients_df['amount'] = ingredients_df['amount'].apply(lambda x: np.random.randint(ingredient_total_amount))
    ingredients_df[["Available carbohydrate, without sugar alcohols (g)","Protein (g)","Fat, total (g)"]] = ingredients_df[["Available carbohydrate, without sugar alcohols (g)","Protein (g)","Fat, total (g)"]].apply(lambda x: multiply_columns(x, ingredients_df['amount']))
    #print(ingredients_df)

    carb_total = ingredients_df["Available carbohydrate, without sugar alcohols (g)"].sum()
    protein_total = ingredients_df["Protein (g)"].sum()
    fat_total = ingredients_df["Fat, total (g)"].sum()
    amount = ingredients_df["amount"]
   
    score = 0

    print(ingredients_df)
    print(f"CARB : {targets['carbs']} | {carb_total} | {targets['carbs_max']} , PROTEIN : {targets['protein']} | {protein_total} | {targets['protein_max']}, FAT : {targets['fat']} | {fat_total} | {targets['fat_max']}")

    if carb_total >= targets["carbs"] <= targets["carbs_max"]:
        score += 1
    
    if protein_total >= targets["protein"] <= targets["protein_max"]:
        score += 1

    if fat_total >= targets["fat"] <= targets["fat_max"]:
        score += 1

    print(f"SCORE : {score}")
    if score == 3:
        now = datetime.datetime.now()
        recipe_name = now.strftime('%m%d%y%H%M%S')
        ingredients_df = ingredients_df.append(ingredients_df.sum(numeric_only=True), ignore_index=True)
        ingredients_df.to_csv( "recipes/" + recipe_name + ".csv")

