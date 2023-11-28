from pymongo import MongoClient

client = MongoClient('mongodb+srv://admin:12345678aA@flashcard.ubuimgf.mongodb.net/?retryWrites=true&w=majority')

db = client['flashcard']

User = db['users']
Post = db['posts']
Class = db['classes']
Set = db['sets']
