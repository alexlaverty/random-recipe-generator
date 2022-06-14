import common

config = common.config()

def score_recipe(df):
    print("SCORING RECIPE...")
    print(df)
    score = 0
    for nutrient_target in config['nutrient_targets']:
        if 'min' in nutrient_target and 'max' in nutrient_target:
            micronutrient = nutrient_target["micronutrient"]
            micronutrient_total = df[micronutrient].iloc[-1]
            micronutrient_min = nutrient_target['min']
            micronutrient_max = nutrient_target['max']
            if micronutrient_total >= micronutrient_min and micronutrient_total <= micronutrient_max:
                score += 1    
    return score


# print(f"SCORE : {score}")
# if score == 3:
#     now = datetime.datetime.now()
# recipe_name = now.strftime('%m%d%y%H%M%S')


# ingredients_df.to_csv( "recipes/" + recipe_name + ".csv")