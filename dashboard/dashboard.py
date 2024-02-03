from flask import Flask, render_template
import pandas as pd
import pymongo
import plotly
import plotly.express as px
from bson.son import SON

app = Flask(__name__)

client = pymongo.MongoClient('mongo_database', 27017, username="root", password="example")
database = client['Projet_Marmiton']
collection = database['Recette']
cursor = collection.find()

data = pd.read_json('/path/to/dashboard/recipes.json')

#dev
collection.insert_many(data.to_dict(orient='records'))
#dev 



DEVELOPMENT_ENV = True

@app.route('/')
def dashboard():
    return render_template('index.html', log=client.server_info())


@app.route("/table")
def service():
    heading = data.head(50)
    return render_template("table.html", tables=[heading.to_html(classes='data', header="true")])


@app.route("/ratings")
def rating_graph():
    pipeline = [
        {"$unwind": "$rating"},
        {"$group": {"_id": "$rating", "count": {"$sum": 1}}},
        {"$sort": SON([("_id", -1)])}
    ]

    data_ratings = pd.DataFrame(list(collection.aggregate(pipeline)))
    data_ratings.rename(columns={"_id": "Note", "count" : "Nombre_de_notes"}, inplace=True)

    for i in range(len(data_ratings)):
        data_ratings.loc[i, "Note"] = data_ratings.loc[i, "Note"][:-2]
    data_ratings["Note"] = data_ratings["Note"].astype(float)
    
    plot = px.scatter(data_ratings, x='Note', y="Nombre_de_notes", labels={"Note": "Notes (/5)", "Nombre_de_notes": "Nombre de notes"}, title = "Nombre de recette pour chaque nombre d'étoiles")

    return render_template('ratings.html', plot=plot.to_html())


@app.route("/prices")
def prices_graph():
    pipeline = [
    {"$unwind": "$price"},
    {"$group": {"_id": "$price", "count": {"$sum": 1}}},
    {"$sort": SON([("count", 1), ("_id", -1)])}
    ]

    data_prices = pd.DataFrame(list(collection.aggregate(pipeline)))
    data_prices.rename(columns={"_id": "Prix", "count" : "Nombre_de_recettes"}, inplace=True)

    plot = px.bar(data_prices, x='Prix', y="Nombre_de_recettes", labels={"Prix": "Prix moyen", "Nombre_de_recettes": "Nombre de recettes"}, title = "Nombre de recette par catégorie de prix")

    return render_template('prices.html', plot=plot.to_html())


@app.route("/name_occurence")
def name_graph():
    pipeline = [
    {"$project": {"title_words": {"$split": ["$title", " "]}}},
    {"$unwind": "$title_words"},
    {"$group": {"_id": "$title_words", "count": {"$sum": 1}}},
    {"$sort": SON([("count", -1), ("_id", -1)])}
    ]

    data_names = pd.DataFrame(list(collection.aggregate(pipeline)))
    data_names.rename(columns={"_id":"Titre", "count": "Ocurrence"}, inplace=True)

    plot = px.bar(data_names[0:20], x="Titre", y="Ocurrence")
    return render_template('names.html', plot=plot.to_html())


@app.route("/ingredient_occurence")
def ingredients_graph():
    pipeline = [
    {"$unwind": "$ingredients"},
    {"$group": {"_id": "$ingredients.name", "count": {"$sum": 1}}},
    {"$sort": SON([("count", -1), ("_id", -1)])}
    ]

    data_ingredient = pd.DataFrame(list(collection.aggregate(pipeline)))
    data_ingredient.rename(columns={"_id":"Ingredients", "count": "Ocurrence"}, inplace=True)

    top_20 = data_ingredient.head(20)

    autre = pd.DataFrame({
    'Ingredients': ['Autre'],
    'Ocurrence': [data_ingredient['Ocurrence'][20:].sum()]
    })

    df_combined = pd.concat([top_20, autre])

    plot = px.pie(df_combined, values="Ocurrence", names="Ingredients")
    return render_template('ingredients.html', plot=plot.to_html())


@app.route("/ustensil_occurence")
def ustensils_graph():
    pipeline = [
    {"$unwind": "$ustensils"},
    {"$group": {"_id": "$ustensils", "count": {"$sum": 1}}},
    {"$sort": SON([("count", -1), ("_id", -1)])}
    ]

    data_ustensils = pd.DataFrame(list(collection.aggregate(pipeline)))
    data_ustensils.rename(columns={"_id":"Ustensils", "count": "Ocurrence"}, inplace=True)

    top_20 = data_ustensils.head(20)

    autre = pd.DataFrame({
    'Ustensils': ['Autre'],
    'Ocurrence': [data_ustensils['Ocurrence'][20:].sum()]
    })

    df_combined = pd.concat([top_20, autre])


    plot = px.pie(df_combined, values="Ocurrence", names="Ustensils")
    return render_template('ustensils.html', plot=plot.to_html())


@app.route("/step")
def steps_graph():
    pipeline = [
    {'$unwind': '$difficulty'},
    {'$group': {'_id': {'num_steps': { '$size': '$steps' },'difficulty': '$difficulty'},'count': { '$sum': 1 }}},
    {'$group': {'_id': '$_id.num_steps','details': {'$push': {'difficulty': '$_id.difficulty','count': '$count'}}}},
    {'$sort': { '_id': 1 }}
    ]

    df = pd.json_normalize(collection.aggregate(pipeline))
    df = df.explode("details")
    df[["difficulty", "count"]] = 0
    for i in range(len(df)):
        df["difficulty"].iloc[i] = df["details"].iloc[i]["difficulty"]
        df["count"].iloc[i] = df["details"].iloc[i]["count"]
    df.drop("details", axis=1, inplace=True)
    plot = px.bar(df, x="_id", y="count", color="difficulty")
    return render_template('step.html', plot=plot.to_html())



if __name__ == "__main__":
    app.run(debug=DEVELOPMENT_ENV)