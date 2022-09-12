from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from db import client
app = Flask(__name__)
db = client.dbsparta


@app.route('/')
def home():
    return render_template('index.html')


@app.route("/mars", methods=["POST"])
def web_mars_post():
    name_receive = request.form['name_give']
    address_receive = request.form['address_give']
    size_receive = request.form['size_give']
    allList = list(db.mars.find({}, {'_id': False}))
    count = len(allList) + 1
    print(count)

    doc = {
        'orderId': count,
        'name': name_receive,
        'address': address_receive,
        'size': size_receive
    }
    db.mars.insert_one(doc)
    return jsonify({'msg': 'order completed'})


@app.route('/marsUpdate', methods=["POST"])
def mars_update():
    id_receive = int(request.form['id_give'])
    name_receive = request.form['name_give']
    address_receive = request.form['address_give']
    size_receive = request.form['size_give']
    db.mars.update_one({'orderId': id_receive}, {'$set': {'name': name_receive,
                                                          'address': address_receive,
                                                          'size': size_receive}})

    return jsonify({'msg': 'updated!'})


@app.route("/marsDelete", methods = ["DELETE"])
def marsDelet():
    id_receive = int(request.form['id_give'])
    db.mars.delete_one({'orderId': id_receive})
    return jsonify({'msg':'Deleted!'})

@app.route("/mars", methods=["GET"])
def web_mars_get():
    allOrders = list(db.mars.find({}, {'_id': False}))
    return jsonify({'orders': allOrders})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
