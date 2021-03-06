import common
import datetime
import pandas as pd

config = common.config()

css = """ <head>
    <style type="text/css">
    table, th, td {
        border: 1px solid black;
        border-collapse: collapse;
    }
    th {
        font-weight: bold;
    }
    </style>
    </head>"""

def save_recipe(html, score):
    now = datetime.datetime.now()
    timestamp = now.strftime('%m%d%y%H%M%S%f')
    recipe_file_name = str(score) + "_" + timestamp 
    print(f"Saving Recipe : {recipe_file_name}")
    text_file = open("recipes/" + recipe_file_name + ".html", "w")
    text_file.write(html)
    text_file.close()
    f = open('recipes/index.html', 'a')
    f.write(f"<a href=\"{recipe_file_name}.html\">{recipe_file_name}</a><br>")
    f.close()

def highlight_column(s, col):
    return ['background-color: #90ee90' if s.name == col else '' for v in s.index]

def get_ingredient_html(df):
    df['Amount (g)'] = df['Amount (g)'].round().astype(int)
    df['Protein (g)'] = df['Protein (g)'].round().astype(int)
    df['Fat, total (g)'] = df['Fat, total (g)'].round().astype(int)
    df['Calories'] = df['Calories'].round().astype(int)
    html = "<table style=\"border: 1px solid black; border-collapse: collapse;\">"
    html += "<tr><th>Food Name</th><th>Amount (g)</th><th>Protein (g)</th><th>Fat, total (g)</th><th>Calories</th></tr>"
    for index, row in df.iterrows():
        html += f"<tr><td>{row['Food Name']}</td><td>{row['Amount (g)']}</td><td>{row['Protein (g)']}</td><td>{row['Fat, total (g)']}</td><td>{row['Calories']}</td></tr>"
    html += "</table><br><br>"
    return html

def get_nutrient_html(df):
    html = "<table>"
    html += "<tr><th>Name</th><th>Min</th><th>Value</th><th>Max</th></tr>"
    df = df.drop(['Food Name', 'Amount (g)'], 1)
    nutrient_targets = config['nutrient_targets']
    for (columnName, columnData) in df.iteritems():
        nutrient_min = 0
        nutrient_max = 0
        
        for target in nutrient_targets:  # for name, age in dictionary.iteritems():  (for Python 2.x)
            micronutrient_target = target["micronutrient"]
            
            if micronutrient_target == columnName:
                nutrient_min = target["min"]
                nutrient_max = target["max"]
            
            td_color = "#ffffff"
            if int(columnData.values[0]) >= nutrient_min :
                if nutrient_max == 0 or int(columnData.values[0]) <= nutrient_max:
                    td_color = "#90ee90"  

        html += f"<tr><td bgcolor=\"{td_color}\">{columnName}</td><td bgcolor=\"{td_color}\">{nutrient_min}</td><td bgcolor=\"{td_color}\">{round(columnData.values[0],2)}</td><td bgcolor=\"{td_color}\">{nutrient_max}</td></tr>"
    html += "</table>"
    return html

def score_recipe(df):

    with pd.option_context('display.precision', 1):
        df_style = df.style
        df_style.hide(axis='index')

    score = 0

    for nutrient_target in config['nutrient_targets']:
        if 'min' in nutrient_target and 'max' in nutrient_target:
            micronutrient = nutrient_target["micronutrient"]
            micronutrient_total = df[micronutrient].iloc[-1]
            micronutrient_min = nutrient_target['min']
            micronutrient_max = nutrient_target['max']
            if micronutrient_total >= micronutrient_min :
                if micronutrient_max == 0 or micronutrient_total <= micronutrient_max:
                    score += 1    

    minimum_recipe_score = int(config['minimum_recipe_score'])
    # print("===============   RECIPE    =================")
    # print(df)
    # print(f"SCORE : {str(score)}")
    # print(f"SCORE MINIMUM : {str(minimum_recipe_score)}")

    if score >= minimum_recipe_score:
        ingredients = df[['Food Name',"Amount (g)","Protein (g)","Fat, total (g)","Calories"]]
        ingredients_html = get_ingredient_html(ingredients)

        recipe_totals =  df.tail(1)
        recipe_totals_html = get_nutrient_html(recipe_totals)
        #html = css + "<center>" + ingredients_html + recipe_totals_html + "<hr><b>Raw Data</b><br>"+ df.to_html() +"/<center>"
        html = css + "<center>" + ingredients_html + recipe_totals_html + "/<center>"

        if score >= minimum_recipe_score:
            save_recipe(html, score)


