from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import user, auth, post, classes, set

app = FastAPI()
origins = [
    'http://localhost:3000',
    'https://studease.onrender.com',
    '*'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router, tags=['Users'], prefix='/api/users')
app.include_router(auth.router, tags=['Auth'], prefix='/api/auth')
app.include_router(post.router, tags=['Posts'], prefix='/api/posts')
app.include_router(classes.router, tags=['Classes'], prefix='/api/classes')
app.include_router(set.router, tags=['Sets'], prefix='/api/sets')

@app.get("/api/healthchecker")
def root():
    return {"message": "Welcome to FastAPI with MongoDB"}
