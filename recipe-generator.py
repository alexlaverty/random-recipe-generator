import datetime
import numpy as np
import os
import pandas as pd
import random
import common
import scoring
from dataclasses import dataclass
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
pd.options.mode.chained_assignment = None 

pd.set_option('display.max_colwidth',200)
recipe_folder_path = 'recipes'
nutrition_spreadsheet_path = "Release 2 - Nutrient file.xlsx"

rename_column_dict = { 
    'Available carbohydrate, without sugar alcohols (g)': 'carbs',
    # 'Energy with dietary fibre, equated (kJ)': 'kilojoules'
    }


@dataclass
class Recipe:
    ingredients: pd.DataFrame
    score: int = 0


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
    recipe_generation_attempts = config['recipe_generation_attempts']
    for i in range(recipe_generation_attempts):
        number_of_ingredients_min = config['number_of_ingredients']["min"]
        number_of_ingredients_max = config['number_of_ingredients']["max"]
        number_of_ingredients = random.randint(number_of_ingredients_min, number_of_ingredients_max)
        ingredients_df = list_of_ingredients.sample(n = number_of_ingredients)
        ingredients_df.insert(1,'Amount (g)', 0)
        ingredients_df.insert(2,'Calories', 0)
        ingredients_df['Amount (g)'] = ingredients_df['Amount (g)'].apply(lambda x: np.random.randint(config['ingredient_max_grams']))
        ingredients_df[config['included_micronutrients']] = ingredients_df[config['included_micronutrients']].apply(lambda x: multiply_columns(x, (ingredients_df['Amount (g)'] / 100) ))
        ingredients_df['Calories'] = round(ingredients_df['Energy with dietary fibre, equated (kJ)'] / 4.184, 0)
        ingredients_df = ingredients_df.append(ingredients_df.sum(numeric_only=True), ignore_index=True)
        ingredients_df.index += 1 
        recipe_score = scoring.score_recipe(ingredients_df)


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