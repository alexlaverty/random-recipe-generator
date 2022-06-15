# recipe-generator
Randomly Generate Recipes 

The script reads in nutrition data from the **Australian Food Composition Database** :
https://www.foodstandards.gov.au/science/monitoringnutrients/afcd/Pages/downloadableexcelfiles.aspx

It then filters foods and micronutrients from the list as specified in the config.yml file.

Grab a random number of ingredients from the list and then generate a random amount of each ingredient in grams.

Score the recipe against a set of nutritional targets and if it reaches the minimum number of targets to hit save the recipe to a file.

To run the script :

```
pip3 install numpy pandas
python3 recipe-generator.py
```

See a list of randomly generated recipes here :

<https://alexlaverty.github.io/random-recipe-generator/recipes>