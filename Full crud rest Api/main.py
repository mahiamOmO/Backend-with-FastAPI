from fastapi import Depends, FastAPI
from typing import Any
from fastapi import FastAPI, HTTPException, Request
from random import randint
from datetime import datetime, timezone
from typing import Any, List, Dict, Annotated
from sqlmodel import SQLModel, create_engine, Session, select, Field
from contextlib import asynccontextmanager
from sqlmodel import SQLModel,Session,create_engine

class Campaign(SQLModel,table=True):
    campaign_id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    due_date: datetime | None = Field(default=None,index=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc),nullable=True,index=True)

sqlite_file_name = "databse.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:  
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    with Session(engine) as session:
        if not session.exec(select(Campaign)).first():
            session.add_all([
            Campaign(name="Summer Launch", due_date=datetime.now()),
            Campaign(name="Winter Sale", due_date=datetime.now())
            ])
            session.commit()
    yield



app = FastAPI(root_path="/api/v1",lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "Hello, World!"}

data = [
    {
        "campaign_id": 1,
        "name": "Summer Launch",
        "due_date": datetime.now(),
        "created_at": datetime.now()
    },
    {
        "campaign_id": 2,
        "name": "Winter Sale",
        "due_date": datetime.now(),
        "created_at": datetime.now()
    }
    
]

"""
Campaigns
- campaign_id
- name
- due date
-created_at

"""
@app.get("/api/v1/campaigns")
async def read_campaigns():
    return {"campaigns": data}

@app.get("/campaigns/{id}")
async def read_campaign(id: int):
    for campaign in data:
        if campaign.get("campaign_id") == id:
            return {"campaign": campaign}
        
    raise HTTPException(status_code=404, detail="Campaign not found")
@app.post("/campaigns")
async  def create_campaign(body: dict[str,Any]):
    body = await request.json()

    new: Any = {
        "campaign_id": ranint(100,1000),
        "name": body.get("name"),
        "due_date": body.get("due_date"),
        "created_at": datetime.now()
    }

    data.append(new)
    return {"campaign": new}

@app.put("/campaigns/{id}")
async def update_campaign(id: int, body: dict[str, Any]):

    for index,campaign in enumerate(data):
        if campaign.get("campaign_id") == id:

           updated : Any = {
               "campaign_id": id,
               "name": body.get("name"),
               "due_date": body.get("due_date"),
               "created_at": campaign.get("created_at")
          
           }
        data[index] = updated
        return {"campaign": updated}

    raise HTTPException(status_code=404, detail="Campaign not found")