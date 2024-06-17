from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from pymongo import MongoClient
import socket


app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/dev"
mongo = PyMongo(app)
# db = mongo.db
# client = MongoClient(app.config["MONGO_URI"])
# print(client)
# names = client.list_database_names()
# print(jsonify(names))
@app.route("/")
def index():
    # hostname = socket.gethostname()
    names = client.list_database_names()
    return jsonify(
        databases=names
        # message="Welcome to Tasks app! I am running inside {} pod!".format(hostname)
    )
@app.route("/tasks")
def get_all_tasks():
    try:
        tasks = mongo.db.task.find()
        task_list = []
        for task in tasks:
            task_item = {
                "id": str(task["_id"]),
                "task": task["task"]
            }
            task_list.append(task_item)
        
        return jsonify(tasks=task_list)
    except Exception as e:
        return jsonify(error=str(e)), 500
@app.route("/task", methods=["POST"])
def create_task():
    data = request.get_json(force=True)
    mongo.db.task.insert_one({"task": data["task"]})
    return jsonify(
        message="Task saved successfully!"
    )
@app.route("/task/<id>", methods=["PUT"])
def update_task(id):
    data = request.get_json(force=True)["task"]
    response = mongo.db.task.update_one({"_id": ObjectId(id)}, {"$set": {"task": data}})
    if response.matched_count:
        message = "Task updated successfully!"
    else:
        message = "No Task found!"
    return jsonify(
        message=message
    )
@app.route("/task/<id>", methods=["DELETE"])
def delete_task(id):
    response = mongo.db.task.delete_one({"_id": ObjectId(id)})
    if response.deleted_count:
        message = "Task deleted successfully!"
    else:
        message = "No Task found!"
    return jsonify(
        message=message
    )
@app.route("/tasks/delete", methods=["POST"])
def delete_all_tasks():
    mongo.db.task.remove()
    return jsonify(
        message="All Tasks deleted!"
    )
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)