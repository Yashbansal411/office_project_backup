from flask import Flask, request
from  pymongo import MongoClient

app = Flask(__name__)
#app.config["MONGO_URI"] = "mongodb://localhost:27017/Users"
connect = MongoClient('localhost',27017)
db = connect['application_data']
collection1 = db['db']
#mongo = PyMongo(app)
@app.route('/',methods=['GET'])
def home():
    #id = collection1.insert_one({'name':'yash','age':23})
    first = request.args.get('first')
    last = request.args.get('last')
    collection1.insert_one({'first': first, 'last': last, 'flag':False})
    return "user added successfully"

@app.route('/update/<name>')
def update_data(name):
    id = collection1.find_one({'first':name})
    print(id.get('_id'))
    collection1.update_one({'_id' : id.get('_id')}, {"$set":{'name':'updated_entry','lan':'python', 'flag' : True}})
    return "updated successfully"
@app.route('/find')
def find_all():
    ans = collection1.find({'$or':[{'first': 'yash'}, {'flag': True}]})
    for doc in ans:
        print(doc)
    return "dictionary"
#@app.route('/')
if __name__ == "__main__":
    app.run(debug=True)