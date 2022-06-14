import datetime
import numpy as np
import os
import pandas as pd
import random
import common
import scoring

recipe_folder_path = 'recipes'
nutrition_spreadsheet_path = "Release 2 - Nutrient file.xlsx"

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

def save_recipe(df, score):
    now = datetime.datetime.now()
    timestamp = now.strftime('%m%d%y%H%M%S%f')
    df.to_csv( "recipes/" + str(score) + "_" + timestamp + ".csv")

def generate_random_recipes(list_of_ingredients):
    recipe_generation_attempts = config['recipe_generation_attempts']
    for i in range(recipe_generation_attempts):
        print(f"====== Random Recipe Number : {i} ========")
        number_of_ingredients = random.randint(5,10)
        print(f"Number of Ingredients : {number_of_ingredients}")
        ingredients_df = list_of_ingredients.sample(n = number_of_ingredients)
        ingredients_df.insert(1,'Amount (g)', 0)
        ingredients_df.insert(2,'Calories', 0)
        ingredients_df['Amount (g)'] = ingredients_df['Amount (g)'].apply(lambda x: np.random.randint(config['ingredient_max_grams']))
        ingredients_df[config['included_micronutrients']] = ingredients_df[config['included_micronutrients']].apply(lambda x: multiply_columns(x, (ingredients_df['Amount (g)'] / 100) ))
        ingredients_df['Calories'] = ingredients_df['Energy with dietary fibre, equated (kJ)'] / 4.184
        ingredients_df = ingredients_df.append(ingredients_df.sum(numeric_only=True), ignore_index=True)
        ingredients_df.index += 1 
        print(ingredients_df)
        recipe_score = scoring.score_recipe(ingredients_df)
        print(f"RECIPE SCORE : {recipe_score}")
        minimum_recipe_score = int(config['minimum_recipe_score'])
        if recipe_score >= minimum_recipe_score:
            save_recipe(ingredients_df, recipe_score)

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