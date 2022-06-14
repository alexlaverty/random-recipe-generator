import os
import pandas as pd
import yaml

recipe_folder_path = 'recipes'
nutrition_spreadsheet_path = "Release 2 - Nutrient file.xlsx"
config_file_path = "config.yml"

def create_recipe_folder():
    if not os.path.exists(recipe_folder_path):
        os.makedirs(recipe_folder_path)

def get_nutrition_data():
    df = pd.read_excel(nutrition_spreadsheet_path, sheet_name=1)
    df.columns = [x.replace("\n", "") for x in df.columns.to_list()]
    return df

def get_yaml_config():
    with open(config_file_path, 'r') as stream:
        try:
            parsed_yaml=yaml.safe_load(stream)
            #print(parsed_yaml)
        except yaml.YAMLError as exc:
            print(exc)
    return parsed_yaml

def filter_ingredient_list(df, include_ingredients, exclude_ingredients):
    df = df[df['Food Name'].str.contains("|".join(include_ingredients), case=False)]
    df = df[df["Food Name"].str.contains("|".join(exclude_ingredients), case=False)==False]
    return df

if __name__ == "__main__":
    create_recipe_folder()
    config = get_yaml_config()
    ingredient_list = get_nutrition_data()
    filtered_ingredient_list = filter_ingredient_list(ingredient_list, config['include_ingredients'], config['exclude_ingredients'])
    