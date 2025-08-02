import os
from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
from dotenv import load_dotenv
from flask import render_template


load_dotenv()

client=MongoClient(os.getenv("MONGO_URI"))

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

app = Flask(__name__)

@app.route("/")
def index():
    books = []
    for doc in items.find():
        books.append({
            "id": str(doc["_id"]),
            "title": doc.get("Title", ""),
            "author": doc.get("Author", ""),
            "year": doc.get("Year", ""),
            "isbn": doc.get("ISBN", "")
        })
    return render_template("index.html", books=books)

db=client["library"]
items=db["Books"]

@app.route("/Books", methods=["POST"])
def create():
    try:
        data = request.get_json()
        result = items.insert_one(data)
        return jsonify({"_id": str(result.inserted_id)}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/Books", methods=["GET"])
def get_book():
    docs=list()
    for doc in items.find():
        doc["_id"]=str(doc["_id"])
        docs.append(doc)
    return jsonify(docs), 201

@app.route("/Books/<id>", methods=["GET"])
def getspecific(id):
    try:
        doc=items.find_one({"_id":ObjectId(id)})
        doc["_id"]=str(doc["_id"])
        return jsonify(doc),201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/Books/<id>",methods=["PUT"])
def updateBook(id):
    try:
        data=request.get_json()
        result=items.update_one({"_id":ObjectId(id)},{"$set":data})
        return jsonify({"updated":result.modified_count}),201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/Books/<id>",methods=["DELETE"])
def deleteBook(id):
    try:
        result=items.delete_one({"_id":ObjectId(id)})
        return jsonify({"deleted":True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

if __name__=="__main__":
    app.run(debug=True)


