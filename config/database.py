from pymongo import MongoClient
import certifi

ca = certifi.where()

client = MongoClient('mongodb+srv://admin:12345678aA@flashcard.ubuimgf.mongodb.net/?**ssl=true&ssl_cert_reqs=CERT_NONE**retryWrites=true&w=majority', tlsCAFile=ca)

db = client['flashcard']

User = db['users']
Post = db['posts']
Class = db['classes']
Set = db['sets']
