import datetime
import numpy as np
import os
import pandas as pd
import random
import common
import scoring

recipe_folder_path = 'recipes'
nutrition_spreadsheet_path = "Release 2 - Nutrient file.xlsx"

recipe_generation_attempts = 1000
rename_column_dict = { 
    'Available carbohydrate, without sugar alcohols (g)': 'carbs'
    }


def create_recipe_folder():
    if not os.path.exists(recipe_folder_path):
        os.makedirs(recipe_folder_path)

def get_nutrition_data():
    df = pd.read_excel(nutrition_spreadsheet_path, sheet_name=1)
    df.columns = [x.replace("\n", "") for x in df.columns.to_list()]
    return df


def filter_ingredient_list(df, include_ingredients, exclude_ingredients):
    df = df[df['Food Name'].str.contains("|".join(include_ingredients), case=False)]
    df = df[df["Food Name"].str.contains("|".join(exclude_ingredients), case=False)==False]
    return df


def multiply_columns(column, weights):
    return column * weights

def generate_random_recipes(list_of_ingredients):
    for i in range(recipe_generation_attempts):
        print(f"====== Random Recipe Number : {i} ========")
        number_of_ingredients = random.randint(5,10)
        print(f"Number of Ingredients : {number_of_ingredients}")
        ingredients_df = list_of_ingredients.sample(n = number_of_ingredients)
        ingredients_df["amount"] = 0
        ingredients_df['amount'] = ingredients_df['amount'].apply(lambda x: np.random.randint(config['ingredient_max_grams']))
        ingredients_df[config['included_micronutrients']] = ingredients_df[config['included_micronutrients']].apply(lambda x: multiply_columns(x, ingredients_df['amount']))
        ingredients_df = ingredients_df.append(ingredients_df.sum(numeric_only=True), ignore_index=True)
        ingredients_df.index += 1 
        print(ingredients_df)
        recipe_score = scoring.score_recipe(ingredients_df)
        print(f"RECIPE SCORE : {recipe_score}")

def rename_columns(df):
    renamed_columns = df.rename(
        columns={
            'Available carbohydrate, without sugar alcohols (g)': 'carbs' 
            }, inplace=True)
    return renamed_columns

if __name__ == "__main__":
    config = common.config()
    create_recipe_folder()
    ingredient_list = get_nutrition_data()
    filtered_ingredient_list = filter_ingredient_list(ingredient_list, config['include_ingredients'], config['exclude_ingredients'])
    filtered_ingredient_list.rename(columns=rename_column_dict, inplace=True)
    filtered_ingredient_list = filtered_ingredient_list[["Food Name"] + config['included_micronutrients']]
    generate_random_recipes(filtered_ingredient_list)