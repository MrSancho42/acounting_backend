from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import (
    user, business, bill, business_record, user_record, user_category, group_category, group_record, business_category
)

origins = [
    'http://localhost',
    'http://localhost:8000',
    'http://localhost:3000',
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(user.router)
app.include_router(business.router)
app.include_router(bill.router)
app.include_router(business_record.router)
app.include_router(user_record.router)
app.include_router(user_category.router)
app.include_router(group_category.router)
app.include_router(group_record.router)
app.include_router(business_category.router)
