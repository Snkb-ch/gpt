import asyncio
import json

from asgiref.sync import sync_to_async
from yookassa import Configuration, Payment

from yookassa.domain.common.http_verb import HttpVerb



def payment(value, description, email):
    payment = Payment.create({

        "amount": {
            "value": value,
            "currency": "RUB"
        },
        "payment_method_data": {
            "type": "bank_card"
        },
        "receipt": {
            "customer": {
                "email": email
            },



            "items": [
                {
                    "description": description,
                    "quantity": "1.00",
                    "amount": {
                        "value": value,
                        "currency": "RUB"
                    },
                    "vat_code": "1",

                }
            ]

        },
        "confirmation": {
            "type": "redirect",
            "return_url": "www.brainstormai.ru"

        },

        "capture": True,
        "description": description
    })

    return json.loads(payment.json())


async def check_payment(payment_id):
    payment = json.loads((Payment.find_one(payment_id)).json())
    while payment['status'] == 'pending':
        payment = json.loads((Payment.find_one(payment_id)).json())
        await asyncio.sleep(3)

    if payment['status'] == 'succeeded':
        print("SUCCSESS RETURN")
        print(payment)
        return True
    else:
        print("BAD RETURN")
        print(payment)
        return False
