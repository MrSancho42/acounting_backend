from typing import Annotated

from io import BytesIO

import jinja2
import pdfkit
from datetime import datetime
from fastapi import APIRouter, Body, HTTPException, status
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel, Field

from services_manager import user_service, business_service, business_record_service
from domain import BusinessRecord, RecordKinds, RecordSubKinds

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

groups = {
    1: {
        'tax': 268.40,
        'limit': 1_118_900,
        'is_fixed': True
    },
    2: {
        'tax': 1340.0,
        'limit': 5_587_800,
        'is_fixed': True
    },
    3: {
        'tax': 0.05,
        'limit': 7_818_900,
        'is_fixed': False
    },
    4: {
        'tax': 0.02,
        'limit': 7_818_900,
        'is_fixed': False
    }
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


def create_report(records: list[dict], start, group):
    group = groups[group]
    month_records = {}
    for number, name in month_names.items():
        if number < start.month:
            continue
        month_records[number] = {
            'summary': 0,
            'name': name,
            'CASH': 0,
            'NON_CASH': 0,
            'FREE_RECEIVED': 0,
            'REFUND': 0,
            'esv': 1474,
            'tax': group['tax'] if group['is_fixed'] else 0.0,
            'over_normal': False
        }

    for record in records:
        if record['sub_kind'] == RecordSubKinds.GRANTS or record['sub_kind'] == RecordSubKinds.REGULAR_SPENDING:
            continue
        if record['creation_time'].year != start.year or record['creation_time'].month < start.month:
            continue
        month = record['creation_time'].month

        if record['kind'] == RecordKinds.SPENDING:
            month_records[month]['summary'] -= record['amount']
            month_records[month]['REFUND'] -= record['amount']
        else:
            month_records[month]['summary'] += record['amount']
            month_records[month][record['sub_kind'].value] += record['amount']

        if not group['is_fixed']:
            month_records[month]['tax'] = round(month_records[month]['summary'] * group['tax'], 2)

    year_summary = 0
    for month in month_records.values():
        year_summary += month['summary']
        month['over_normal'] = year_summary >= group['limit']

    quarter_to_month = {
        1: [1, 2, 3],
        2: [4, 5, 6],
        3: [7, 8, 9],
        4: [10, 11, 12]
    }

    over_normal = False
    quarters = []
    for quarter in range(1, 5):
        if not set(month_records.keys()) & set(quarter_to_month[quarter]):
            continue
        summary = 0
        CASH = 0
        NON_CASH = 0
        FREE_RECEIVED = 0
        REFUND = 0
        month_list = []
        for month in quarter_to_month[quarter]:
            if month not in month_records:
                continue
            summary += month_records[month]['summary']
            CASH += month_records[month]['CASH']
            NON_CASH += month_records[month]['NON_CASH']
            FREE_RECEIVED += month_records[month]['FREE_RECEIVED']
            REFUND += month_records[month]['REFUND']
            month_list.append(month_records[month])
            over_normal = month_records[month]['over_normal']
        quarters.append({
            'summary': summary,
            'name': quarter,
            'CASH': CASH,
            'NON_CASH': NON_CASH,
            'FREE_RECEIVED': FREE_RECEIVED,
            'REFUND': REFUND,
            'month_list': month_list,
            'tax': round(group['tax'] * len(month_list), 2) if group['is_fixed'] else round(summary * group['tax'], 2),
            'esv': 1474 * len(month_list),
            'over_normal': over_normal
        })

    year_report = {
        'summary': year_summary,
        'tax': round(group['tax'] * len(month_records), 2) if group['is_fixed'] else round(year_summary * group['tax'], 2),
        'esv': 1474 * len(month_records),
        'over_normal': over_normal
    }

    return quarters, year_report


@router.get('/get-book-report')
async def get_book_report(year, month,  group: int):  # pk_business: Annotated[int, Body(embed=True)]
    month = dict(zip(month_names.values(), month_names.keys()))[month]
    year = datetime.strptime(year, "%a %b %d %Y %H:%M:%S GMT%z").year
    template = template_env.get_template('pdf_template.html')
    business = business_service.read(1)

    quarters, year_report = create_report(
        business_record_service.get_business_records(from_business=business),
        datetime(year, month, 1),
        group
    )

    context = {
        'start': datetime(year, month, 1).strftime("%d.%m.%Y"),
        'owner': business.owner_name,
        'address': business.address,
        'taxpayer_account_card': business.taxpayer_account_card,
        'quarters': quarters,
        'year_report': year_report
    }
    options = {
        'encoding': 'UTF-8',
        'quiet': '',
        'enable-local-file-access': '',
        'orientation': 'Landscape'
    }

    config = pdfkit.configuration(wkhtmltopdf='/usr/local/bin/wkhtmltopdf')

    pdf_buffer = BytesIO(
        pdfkit.from_string(
            template.render(context), False, configuration=config, options=options
        )
    )
    pdf_buffer.seek(0)
    return StreamingResponse(pdf_buffer, media_type="application/pdf")
