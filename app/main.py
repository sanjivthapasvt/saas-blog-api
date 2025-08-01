from contextlib import asynccontextmanager
from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi import FastAPI
from core.database import create_db_and_tables
from auth.routes import router as auth_router
from auth.google_auth import router as google_auth_router
from blogs.routes import router as blog_router
from blogs.comment_routes import router as comment_router
from fastapi.staticfiles import StaticFiles
from users.routes import router as users_router
from fastapi.middleware.cors import CORSMiddleware


load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:8000",
    "http://localhost:3000",
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.mount("/media", StaticFiles(directory="media"), name="media")

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(google_auth_router, prefix="/auth", tags=["Auth"])
app.include_router(blog_router, prefix="/blog", tags=["Blog"])
app.include_router(comment_router, prefix="/comment", tags=["Comments"])
app.include_router(users_router, prefix="/user", tags=["Users"])