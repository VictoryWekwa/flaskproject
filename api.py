import flask
from flask import request, jsonify,redirect, render_template
import sqlite3
app = flask.Flask(__name__)
app.config["DEBUG"] = True

# create some data in form of a list of dictionary
items = [
    {'id': 0,
     'name': 'Chocolate',
     'price': '$20'},
    {'id': 1,
     'name': 'milk',
     'price': '$50'},
    {'id': 2,
     'name': 'bread',
     'price': '$30'}
]


@app.route('/', methods=['GET'])
def home():
    return '''<h1> Managing Shopping Inventory</h1>
    <p>This site is an API for managing a shopping inventory.</p>'''


# Getting all items on my list
@app.route('/api/v1/shopping/items/all', methods=['GET'])
def api_all():
    return jsonify(items)


# Getting my item by id
@app.route('/api/v1/shopping/items', methods=['GET'])
def api_id():
    # check if id was provided as part of the url
    # if id was provided  assign it to a variable
    # if no id was provided display an error
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return "Error:No id field provided. Please specify an id."

    # Create an empty list
    results = []
    # loop through the data and match the result that fit the requested id
    # ids are unique, but other fields might return many results
    for item in items:
        if item['id'] == id:
            results.append(item)
        # using the jsonify function from flask to convert our list
        # of python dictionaries to the json format
        return jsonify(results)


# Updating my dictionary with a new item
@app.route('/api/v1/shopping/items', methods=['PUT'])
def update_item():
    item_list = [item for item in items if (item['id'] == id)]
    if 'name' in request.json:
        item_list[0]['name'] = request.json['name']
    if 'price' in request.json:
        item_list[0]['price'] = request.json['price']
    return jsonify(item_list[0])


# Creating a new item
@app.route('/api/v1/shopping/items', methods=['POST'])
def create_item():
    new_item_list = {
        'id': request.json['id'],
        'name': request.json['name'],
        'price': request.json['price']
    }
    items.append(new_item_list)
    return jsonify(new_item_list)


# Deleting an item from my list
@app.route('/api/v1/shopping/items/', methods=['DELETE'])
def delete_item():
    item_list = [item for item in items if (item['id'] == id)]
    if len(item_list) == 0:
        return "Not found", 404
    items.remove(item_list[0])
    return jsonify('Delete process complete')


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The item could not be found.</p>", 404


app.run()
