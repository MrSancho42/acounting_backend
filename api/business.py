from typing import Annotated

from io import BytesIO

import jinja2
import pdfkit
from datetime import datetime
from fastapi import APIRouter, Body, HTTPException, status
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel, Field

from services_manager import user_service, business_service, business_record_service
from domain import BusinessRecord, RecordKinds

template_env = jinja2.Environment(loader=jinja2.FileSystemLoader('./'))

month_names = {
    1: 'січень',
    2: 'лютий',
    3: 'березень',
    4: 'квітень',
    5: 'травень',
    6: 'червень',
    7: 'липень',
    8: 'серпень',
    9: 'вересень',
    10: 'жовтень',
    11: 'листопад',
    12: 'грудень'
}


router = APIRouter(
    prefix='/business-services',
    tags=['business-services'],
    responses={404: {'description': 'Not found'}},
)


class CreateBusiness(BaseModel):
    name: str
    owner_name: str
    taxpayer_account_card: str
    address: str


class Business(CreateBusiness):
    pk_business: int


@router.post('/create', status_code=status.HTTP_201_CREATED)
async def create(pk_user: Annotated[int, Body(embed=True)], business: CreateBusiness):
    business_service.create(owner=user_service.read(pk_user), **business.dict())
    

@router.get('/read/{pk_business}', response_model=Business, status_code=status.HTTP_200_OK)
async def read(pk_business: int):
    business = business_service.read(pk_business)
    return {
        'pk_business': business.pk_business,
        'name': business.name,
        'owner_name': business.owner_name,
        'taxpayer_account_card': business.taxpayer_account_card,
        'address': business.address
    }


@router.patch('/update', status_code=status.HTTP_200_OK)
async def update(business: Business):
    business_service.update(business_service.read(business.pk_business), business.dict(exclude_unset=True))


@router.get('/get-businesses', response_model=list[Business])
async def get_businesses(pk_user: int):
    return business_service.get_businesses(user_service.read(pk_user))


def create_report_list(records: list[dict]):
    report_list = {}
    for record in records:
        if record['kind'] == RecordKinds.SPENDING:
            continue
        month = record['creation_time'].month
        if not report_list or month not in report_list:
            report_list[month] = {
                "summary": 0,
                "name": month_names[month],
                "records": []
            }

        report_list[month]['records'].append({
            'date': record['creation_time'].strftime("%d.%m.%Y"),
            'amount': record['amount'],
            'description': record['description']
        })
        report_list[month]['summary'] += record['amount']
    return report_list


@router.get('/get-book-report')
async def get_book_report():  # pk_business: Annotated[int, Body(embed=True)]

    template = template_env.get_template('pdf_template.html')
    business = business_service.read(1)
    records = create_report_list(business_record_service.get_business_records(from_business=business))

    context = {
        'owner': business.owner_name,
        'address': business.address,
        'taxpayer_account_card': business.taxpayer_account_card,
        'records': records
    }
    options = {
        'encoding': 'UTF-8',
        'quiet': '',
        'enable-local-file-access': ''
    }

    config = pdfkit.configuration(wkhtmltopdf='/usr/local/bin/wkhtmltopdf')

    pdf_buffer = BytesIO(
        pdfkit.from_string(
            template.render(context), False, configuration=config, options=options
        )
    )
    pdf_buffer.seek(0)
    return StreamingResponse(pdf_buffer, media_type="application/pdf")
