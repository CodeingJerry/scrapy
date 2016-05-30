import pymongo
from flask import Flask,render_template
from settings import MONGO_URI,MONGO_DATABASE

app = Flask(__name__)

@app.route('/')
def hello_world():
    client = pymongo.MongoClient(MONGO_URI)
    db = client[MONGO_DATABASE]
    jokes = db['XiubaiItem'].find()
    client.close()
    return render_template("qiubai_index.html",p_jokes=jokes)

if __name__ == '__main__':
    app.run()