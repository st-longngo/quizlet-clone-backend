from pymongo import MongoClient

client = MongoClient('mongodb+srv://admin:12345678aA@flashcard.ubuimgf.mongodb.net/?ssl=true&ssl_cert_reqs=CERT_NONE&retryWrites=true&w=majority')

db = client['flashcard']

User = db['users']
Post = db['posts']
Class = db['classes']
Set = db['sets']
Comment = db['comments']
