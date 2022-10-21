from flask import Flask, jsonify, request
import os
import pprint
from dotenv import load_dotenv, find_dotenv
from pymongo import MongoClient
from flask_cors import CORS
from bson import ObjectId
import json
load_dotenv(find_dotenv())


print("_______________________________________________")
print("                                                 ")


connection = os.environ.get("MONGO_CONNECTION")
client = MongoClient(connection)
production = client.production
db = production.contacts_collection

app = Flask(__name__)
CORS(app)


@app.route("/contacts", methods=["GET", "POST"])
def get_contact():

    if request.method == "GET":
        contacts = db.find()
        o = []
        for contact in contacts:
            o.append({"_ID": str(ObjectId(contact["_id"])),
                      "name": contact["name"],
                      "phone": contact["phone"]
                      })
        return jsonify(o)

    elif request.method == "POST":
        id = db.insert_one({
            "name": request.json["name"],
            "phone": request.json["phone"]
        }
        ).inserted_id
        return jsonify(str(ObjectId(id)))


@app.route("/<id>", methods=["DELETE", "PUT"])
def delete_contact(id):
    if request.method == "DELETE":
        db.delete_one({"_id": ObjectId(id)})
        return jsonify({"message": "deleted"})
    elif request.method == "PUT":
        db.update_one({"_id": ObjectId(id)}, {"$set": {
            "name": request.json["name"],
            "phone": request.json["phone"]
        }})
        # return jsonify({"message": request.json["name"]+"has been updated"})
        return jsonify({"message": "Contact updated"})

        # @app.route("/members")
        # def members():
        #     return {
        #         "contacts":
        #         [
        #             {"name": "Valiant", "phone": "0102253039"},
        #             {"name": "Billy", "phone": "0123456789   "},
        #             {"name": "Chow", "phone": "0122233434"},
        #         ]}
if __name__ == "__main__":
    app.run(debug=True)


# create_documents()

# contact API route

# print(contact_collections.find())


# # inserting database


# def create_documents():

#     doc = {
#         "name": "Valiant",
#         "phone": "0102253039"
#     }
#     contacts_collection.insert_one(doc)


# def insert_contact_doc():
#     collection = contact_db.contacts
#     contact_document = {
#         "name": "Wilson",
#         "phone": "0123646388"
#     }
#     inserted_id = collection.insert_one(contact_document).inserted_id
#     print(inserted_id)
