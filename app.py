from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

# ----------------------------
# Enable CORS
# ----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------
# API Key
# ----------------------------
API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjI0ZjIwMDA0MTZAZHMuc3R1ZHkuaWl0bS5hYy5pbiIsImlhdCI6MTc4MzQ5ODU2NywiaXNzIjoiaHR0cHM6Ly9haXBpcGUub3JnIiwiYXVkIjoiYWlwaXBlLWFwaSIsImV4cCI6MTc4NDEwMzM2N30.eLi_41anlHD2e2bEV4DDaEKh27Nzz0eflbwguKpCoUw"

# IMPORTANT:
# Replace this with YOUR logged-in email.
EMAIL = "24f2000416@ds.study.iitm.ac.in"


# ----------------------------
# Request Models
# ----------------------------
class Event(BaseModel):
    user: str
    amount: float
    ts: int


class AnalyticsRequest(BaseModel):
    events: List[Event]


# ----------------------------
# Analytics Endpoint
# ----------------------------
@app.post("/analytics")
def analytics(
    request: AnalyticsRequest,
    x_api_key: str | None = Header(default=None)
):

    # Authentication
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized"
        )

    events = request.events

    total_events = len(events)

    unique_users = len(set(event.user for event in events))

    revenue = sum(
        event.amount
        for event in events
        if event.amount > 0
    )

    user_totals = {}

    for event in events:
        if event.amount > 0:
            user_totals[event.user] = (
                user_totals.get(event.user, 0)
                + event.amount
            )

    top_user = ""

    if user_totals:
        top_user = max(
            user_totals,
            key=user_totals.get
        )

    return {
        "email": EMAIL,
        "total_events": total_events,
        "unique_users": unique_users,
        "revenue": revenue,
        "top_user": top_user,
    }