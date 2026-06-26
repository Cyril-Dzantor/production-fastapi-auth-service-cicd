from fastapi import FastAPI
from app.core.database import engine
from app.models import user, token, audit
from app.routes import auth, users, admin

user.Base.metadata.create_all(bind=engine)
token.Base.metadata.create_all(bind=engine)
audit.Base.metadata.create_all(bind=engine)



app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(admin.router)

@app.get('/')
def health_check():
    return {"status": "ok"}
