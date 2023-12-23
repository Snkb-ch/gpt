import json
import traceback
import  threading
import asyncio

from asgiref.sync import sync_to_async
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from openai_async import openai_async
from urllib.parse import quote, urlencode
from .prompts import *

from django.contrib import messages
import urllib

import openai
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import FormView

from .forms import *

from yookassa import Configuration, Payment, Refund
from django.http import HttpResponse, FileResponse, HttpResponseRedirect
from django.http import JsonResponse

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *

from django.shortcuts import render, redirect


@login_required(login_url='login')
def history(request):

    uniquetexts = UniqueText.objects.filter(user=request.user).order_by('-created_at')

    examtexts = ExamText.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'basegpt/history.html', {'uniquetexts': uniquetexts, 'examtexts': examtexts})






   
@login_required(login_url='login')
def audio(request):
    transcript = "Здесь будет расшифровка"
    if request.method == 'POST':
        openai.api_key = settings.OPENAI_API_KEY
        audio_file = request.FILES.get('audio_file')

        transcript = openai.Audio.transcribe(
            model="whisper-1",
            file=audio_file,

        )



    return render(request, 'basegpt/audio.html', {'transcript': transcript})


def error(request):
    return render(request, 'basegpt/error.html')


def get_objects(request):
    my_objects = UniqueText.objects.all()
    data = [{'rawfile': obj.rawfile.name, 'responsefile': obj.responsefile.name} for obj in my_objects]
    return JsonResponse({'data': data})


def refund(order):
    Configuration.account_id = settings.YOOKASSA_SHOP_ID
    Configuration.secret_key = settings.YOOKASSA_SECRET_KEY
    Refund.create({
        "amount": {
            "value": order.price,
            "currency": "RUB"
        },
        "payment_id": order.transaction_id
    })
    order.refund = True
    order.save()
    if order.type == 'unique_text' or order.type == 'unique_file':
        unique_text = UniqueText.objects.get(order=order)
        unique_text.delete()
    elif order.type == 'exam_text':
        exam_text = ExamText.objects.get(order=order)
        exam_text.delete()

    # return redirect('error')
    # return JsonResponse({'type': 'error', 'error': 'error payment canceled'})



def cloud(request):
    return render(request, 'basegpt/cloud.html')

def home(request):
    # utm_source = request.GET.get('utm_source')
    #
    # utm_campaign = request.GET.get('utm_campaign')
    # phrase_id = request.GET.get('phrase_id')
    #
    # device_type = request.GET.get('device_type')

    #
    # ad_id = request.GET.get('ad_id')

    if request.session.get('utm_source') == None:
        request.session['utm_source'] = request.GET.get('utm_source')
        request.session['utm_campaign'] = request.GET.get('utm_campaign')
        request.session['gbid'] = request.GET.get('gbid')



    utm_source = request.session.get('utm_source')
    utm_campaign = request.session.get('utm_campaign')
    gbid = request.session.get('gbid')



    value = request.GET.get('type')

    if not value:
            value = 'text'

    context = {
        'utm_source': utm_source,

        'utm_campaign': utm_campaign,
        'gbid': gbid,

        'type': value,

    }
    print(context['type'])

    # values of contex < 64
    print(context.values().__len__() )
    if context.values().__len__() > 58:
        context = {
            'utm_source': utm_source,

            'utm_campaign': utm_campaign,
            'gbid': None,

            'device_type': None,


            'ad_id': None,
        }




    print(context)


    return render(request, 'basegpt/homev5.html', context)

def unique(request):
    return render(request, 'basegpt/home.html')

def split_text_on_parts(text, max_length):
    sentences =  text.split(". ")
    current_part = None
    parts = []
    for sentence in sentences:
        if current_part is None:
            current_part = sentence + ". "
        elif len(current_part) + len(sentence) + 2 <= max_length:  # 2 for period and space
            current_part += sentence + ". "
        else:
            parts.append(current_part.strip())
            current_part = sentence + ". "
    if current_part is not None and current_part != '. ':
        parts.append(current_part.strip())
    return parts


def red1_for_unique_text(text):
    parts =  split_text_on_parts(text, 1500)

    for i in range(len(parts)):
        print(parts[i])


        openai.api_key = settings.OPENAI_API_KEY

        ans = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": Prompts.red1
                },

                {"role": "user",
                 "content": parts[i]},
            ],
            temperature=1,
            max_tokens=2048,
        )
        parts[i] = ans.choices[0]['message']['content']
        print(ans)

    response_text = ''.join(parts)

    return response_text


def red2_for_unique_text(text):
    parts = split_text_on_parts(text, 1500)
    for i in range(len(parts)):


        openai.api_key = settings.OPENAI_API_KEY

        ans =  openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": Prompts.red2
                },

                {"role": "user",
                 "content": parts[i]},
            ],
            temperature=1,
            max_tokens=2048,
        )
        parts[i] = ans.choices[0]['message']['content']

    response_text = ''.join(parts)

    return response_text


def red3_for_unique_text(text):
    parts = split_text_on_parts(text, 1500)
    for i in range(len(parts)):


        openai.api_key  = settings.OPENAI_API_KEY

        ans = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": Prompts.red3
                },

                {"role": "user",
                 "content": parts[i]},
            ],
            temperature=1,
            max_tokens=2048,
        )
        parts[i] = ans.choices[0]['message']['content']

    response_text = ''.join(parts)

    return response_text


def exam_text_result(text, idea):


    openai.api_key = settings.OPENAI_API_KEY
    answer = idea + '\n'

    red2 =  openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": 'Идея текста:' + idea + Prompts.red2_for_exam_text },

            {"role": "user",
             "content": text},
        ],
        temperature=0.45,
        max_tokens=1000,
    )

    red2 = red2.choices[0]['message']['content']

    # red3 = openai.ChatCompletion.create(
    #     model="gpt-3.5-turbo",
    #     messages=[
    #         {
    #             "role": "system",
    #             "content": 'Перепиши текст.Не используй слова которые были использованы в предыдущем предложении'
    #         },
    #
    #         {"role": "user",
    #          "content": red2},
    #     ],
    #     temperature=0.4,
    #     max_tokens=2048,
    # )

    # red3 = red3.choices[0]['message']['content']

    answer += (red2 + '\n')

    red4 =  openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": 'Идея текста:' + idea + Prompts.red4_for_exam_text
            },

            {"role": "user",
             "content": text},
        ],
        temperature=0.3,
        max_tokens=738,
    )

    red4 = red4.choices[0]['message']['content']

    red5 =  openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": Prompts.red5_for_exam_text
            },

            {"role": "user",
             "content": red4},
        ],
        temperature=0.4,
        max_tokens=2048,
    )

    red5 = red5.choices[0]['message']['content']

    answer += (red5 + '\n')

    red6 =  openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": 'Идея текста:' + idea + Prompts.red6_for_exam_text
            },

            {"role": "user",
             "content": text},
        ],
        temperature=0.4,
        max_tokens=1020,
    )

    red6 = red6.choices[0]['message']['content']

    answer += (red6 + '\n')

    red7 =  openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": 'Идея текста:' + idea + Prompts.red7_for_exam_text
            },

            {"role": "user",
             "content": red6},
        ],
        temperature=0.4,
        max_tokens=2048,
    )

    red7 = red7.choices[0]['message']['content']


    answer += (red7 + '\n')

    # additional = openai.ChatCompletion.create(
    #     model="gpt-3.5-turbo",
    #     messages=[
    #         {
    #             "role": "system",
    #             "content": 'Наполни текст синонимами. Сохрани суть, а главное структуру текста по абзацам!'
    #         },
    #
    #         {"role": "user",
    #          "content": answer},
    #     ],
    #     temperature=0.4,
    #     max_tokens=2048,
    # ).choices[0]['message']['content']

    return answer


def getresultfromtext(text, type, order):
    try:



        if type == 'red1':
            response_text =  red1_for_unique_text(text)
        elif type == 'red2':
            response_text =  red2_for_unique_text(text)
        elif type == 'red3':
            response_text =  red3_for_unique_text(text)
        elif type == 'exam_text':
            response_text =   exam_text_result(text, order.idea)

        if  moderation(response_text) == True:
            raise Exception('moderation error')
        else:

            return response_text






    except Exception as e:
        # if runtime error, say try later
        # if token error, do it again but with a different limits
        print(e)
        response = 'error except'

        return response


def success_unique_text(request, order):
    result_obj = UniqueText.objects.get(user=order.user, rawtext=order.rawtext, order=order)
    result_obj.complete = True
    result_obj.save()
    response_text =  getresultfromtext(order.rawtext, order.type2, order)



    obj = UniqueText.objects.get(user=order.user, order=order)
    if response_text == 'error' and obj.complete == False:

        refund(order)
        response = ({'type': 'error', 'error': 'К сожалению произошла ошибка, попробуйте позже. Платеж будет возвращен. Приносим свои извинения'})




    elif response_text != 'error':

        result_obj.responsetext = response_text

        result_obj.save()
        order.result = True
        order.save()

        response = ({'type': 'text', 'response_text': response_text})

    return response


def get_file_contetnt(request, order):
    file_content = order.rawfile.read().decode('utf-8')
    obj = UniqueText.objects.get(user=order.user, order=order)
    obj.complete = True

    obj.save()
    return file_content


def check_complete(order):
    obj = UniqueText.objects.get(user=order.user, order=order)
    if obj.complete == True:
        return True
    else:
        return False


def create_file(order, response_file_text):
    obj = UniqueText.objects.get(user=order.user, order=order)
    # random string uuid

    obj.responsefile.name = 'responsefiles/responsefile' + str(uuid.uuid4()) + '.txt'

    obj.save()

    with open(obj.responsefile.path, 'w') as f:
        f.write(response_file_text)

    delete_old_objects(UniqueText, 10, order.user)
    order.result = True
    order.save()
    file_url = obj.responsefile.url
    response = ({'type': 'file', 'file_url': file_url})
    return response

def success_unique_file(request, order):
    print('success_unique_file')
    file_content =  get_file_contetnt(request, order)

    response_file_text =  getresultfromtext(file_content, order.type2, order)

    if  response_file_text == 'error' and  check_complete(order) == False:

        refund(order)
        response = ({'type': 'error', 'error': 'К сожалению произошла ошибка, попробуйте позже. Платеж будет возвращен. Приносим свои извинения'})

        return response


    elif response_file_text != 'error':
        try:
            # UniqueText.objects.get_or_create(user=order.user, rawfile=order.rawfile, order=order)
            response =  create_file(order, response_file_text)
            return response
        except Exception as e:
            response = ({'type': 'error', 'error': e})
            return response





def success_exam_text(request, order):
    result_obj = ExamText.objects.get(user=order.user, rawtext=order.rawtext, order=order)
    result_obj.complete = True
    result_obj.save()
    response_text =  getresultfromtext(order.rawtext, order.type, order)
    obj = ExamText.objects.get(user=order.user, order=order)
    if response_text == 'error' and obj.complete == False:

        refund(order)
        response = ({'type': 'error', 'error': 'К сожалению произошла ошибка, попробуйте позже. Платеж будет возвращен. Приносим свои извинения'})




    elif response_text != 'error':

        result_obj.responsetext = response_text

        result_obj.save()
        order.result = True
        order.save()

        response = ({'type': 'text', 'response_text': response_text})

    return response


def get_order(button_value, request):
    order = Order.objects.get(id=button_value, user=request.user)
    return order

def success_result(request):
    if request.method == 'POST':


        button_value = request.POST.get('order')




        order = get_order(button_value, request)
        if order.result == True:
            if order.type == 'unique_text':
                obj = UniqueText.objects.get(user=order.user, order=order)
                response_text = obj.responsetext
                response = ({'type': 'text', 'response_text': response_text, 'status': 'ok'})
                return JsonResponse(response)

            elif order.type == 'unique_file':
                obj = UniqueText.objects.get(user=order.user, order=order)
                file_url = obj.responsefile.url
                response = ({'type': 'file', 'file_url': file_url, 'status': 'ok'})
                return JsonResponse(response)

            elif order.type == 'exam_text':
                obj = ExamText.objects.get(user=order.user, order=order)
                response_text = obj.responsetext
                response = ({'type': 'text', 'response_text': response_text, 'status': 'ok'})
                return JsonResponse(response)
        elif order.refund == True:
            response = ({'type': 'error', 'error': 'К сожалению произошла ошибка во время обработки заказа, попробуйте позже. Платеж будет возвращен. Приносим свои извинения', 'status': 'error'})
            return JsonResponse(response)
        elif order.result == False and order.refund == False:
            response = ({'type': 'wait', 'status': 'wait'})
            return JsonResponse(response)



def  success_api(request):


    if request.method == 'POST':
        data =  json.loads(request.body)
        button_value =  data.get('buttonValue')

        order = get_order(button_value, request)

        if order.type == 'unique_text':
            t = threading.Thread(target=success_unique_text, args=(request, order), daemon=True)
            t.start()

            return JsonResponse({'status':'ok'})


        elif order.type == 'unique_file':
            t = threading.Thread(target=success_unique_file, args=(request, order), daemon=True)
            t.start()

            return JsonResponse({'status':'ok'})


        elif order.type == 'exam_text':
            t = threading.Thread(target=success_exam_text, args=(request, order), daemon=True)
            t.start()

            return JsonResponse({'status':'ok'})


@login_required(login_url='/login/')
def success(request):


    objects =  UniqueText.objects.filter(user=request.user, complete=False)

    exam_objects =  ExamText.objects.filter(user=request.user, complete=False)

    return  render(request, 'basegpt/success.html', {'objects': objects, 'exam_objects': exam_objects})

def delete_old_objects(model, limit, user):
    #
    count = model.objects.filter(user=user).count()

    if count > limit:
        oldest = model.objects.earliest('created_at')
        oldest.delete()
        return True
    return False




def moderation(text):
    # openai.api_key = settings.OPENAI_API_KEY
    #
    # moderation =  openai.Moderation.create(
    #     input=text,
    # )
    # output = moderation["results"][0]["flagged"]


    return False
def generate_idea(text, id):
    openai.api_key = settings.OPENAI_API_KEY
    try:

        idea = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": Prompts.idea_for_exam_text
                },

                {"role": "user",
                 "content": text},
            ],
            temperature=1,
            max_tokens=1000,
        )

        idea = idea.choices[0]['message']['content']
        task = Crawl.objects.get(pk=id)


        task.result = idea

        task.status = 'done'
        task.save()
    except:
        task = Crawl.objects.get(pk=id)
        task.status = 'error'
        task.save()

def check_idea(request, id):
    task = Crawl.objects.get(pk=id)
    if task.status == 'done':
        idea = task.result
        task.delete()

        return JsonResponse({'status': 'done', 'idea': idea})
    elif task.status == 'error':

        task.delete()
        return JsonResponse({'status': 'error'})

    else:
        return JsonResponse({'status': 'wait'})





def exam_text_get_idea(request):
    if request.method == 'POST':

        text = request.POST.get('rawtext')
        if moderation(text) == True:

            return JsonResponse({'type': 'error', 'error': 'Текст не прошел модерацию'})


        else:

            task = Crawl()
            task.save()



            t = threading.Thread(target=generate_idea, args=(text,task.id), daemon=True)
            t.start()
            return JsonResponse({'id': task.id, 'type': 'ok'})

@login_required(login_url='login')
def exam_text(request):

    if request.method == 'POST' and 'pay' in request.POST:
        idea = request.POST.get('idea')
        obj = request.POST.get('rawtext')
        code = request.POST.get('code')
        type = 'exam_text'

        if moderation(obj) == True:
            return render(request, 'basegpt/exam_text.html', {'error': 'Текст не прошел модерацию'})
        else:
            if code and is_valid_promo_code(code, request):
                promo = PromoCode.objects.get(code=code)
                discount = promo.discount
                price = 15 - (15 * discount / 100)
            else:
                price = 15

            Configuration.account_id = settings.YOOKASSA_SHOP_ID
            Configuration.secret_key = settings.YOOKASSA_SECRET_KEY
            payment = Payment.create({
                "amount": {
                    "value": price,
                    "currency": "RUB"
                },
                "confirmation": {
                    "type": "redirect",
                    "return_url": "https://brainstormai.ru/success"
                },
                "capture": True,
                "description": "сочинение егэ по русскому ",
                "receipt": {
                    "customer": {

                        "email": request.user.email,
                    },
                    "items": [
                        {
                            "description": "Cочинение егэ по русскому",
                            "quantity": "1",
                            "amount": {
                                "value": price,
                                "currency": "RUB"
                            },
                            "vat_code": 1

                        }
                    ]
                }
            }, uuid.uuid4())

            if code and is_valid_promo_code(code, request):
                Order.objects.create(user=request.user, price=price, rawtext=obj, type=type,
                                     transaction_id=payment.id, promo_code=PromoCode.objects.get(code=code), idea=idea)
            else:
                Order.objects.create(user=request.user, price=price, rawtext=obj, type=type,
                                     transaction_id=payment.id, idea=idea)
            return HttpResponseRedirect(payment.confirmation.confirmation_url)

            # create payment and redirect to payment page

    return render(request, 'basegpt/exam_text.html', {'error': ''})



#
def is_valid_promo_code(code, request):
    if PromoCode.objects.filter(code=code).exists() and PromoCodeUsage.objects.filter(user=request.user,
                                                                                      promo_code=PromoCode.objects.get(
                                                                                          code=code)).exists() == False and code != request.user.code:
        return True


def get_text_from_file(file):
    text = file.read().decode('utf-8')
    return text


def get_price_text(text, code, request, type):

    price = 0


    text = str(text)

    if code and is_valid_promo_code(code, request):
        promo = PromoCode.objects.get(code=code)
        discount = promo.discount
    else:
        promo = None
        discount = 0

    if type == 'red1':

        price = 0
        price = int(len(text) * 0.0025 * (100 - discount) / 100)
    elif type == 'red2':
        price = int(len(text) * 0.005 * (100 - discount) / 100)
    elif type == 'red3':
        price = int(len(text) * 0.0075 * (100 - discount) / 100)

    if price < 1:
        price = 1

    return price



def uniquetext(request):
    if request.method == 'POST' and 'getprice' in request.POST:
        obj = request.POST.get('rawtext')
        code = request.POST.get('code')
        type = request.POST.get('type')

        if moderation(obj) == True:
            return JsonResponse({'type': 'error', 'error': 'Текст не прошел модерацию'})
        else:

            price = str(get_price_text(obj, code, request, type))

            return JsonResponse({'price': price})

    if request.method == 'POST' and 'pay' in request.POST:
        obj = request.POST.get('rawtext')
        code = request.POST.get('code')
        type = request.POST.get('options')

        if moderation(obj) == True:
            return render(request, 'basegpt/uniquetext.html', {'error': 'Текст не прошел модерацию'})
        else:

            price = str(get_price_text(obj, code, request, type))

            Configuration.account_id = settings.YOOKASSA_SHOP_ID
            Configuration.secret_key = settings.YOOKASSA_SECRET_KEY
            payment = Payment.create({
                "amount": {
                    "value": price,
                    "currency": "RUB"
                },
                "confirmation": {
                    "type": "redirect",
                    "return_url": "https://brainstormai.ru/success"
                },
                "capture": True,
                "description": "oreder unique text " + str(type),
                "receipt": {
                    "customer": {

                        "email": request.user.email,
                    },
                    "items": [
                        {
                            "description": "Повышение уникальности" + str(type),
                            "quantity": "1",
                            "amount": {
                                "value": price,
                                "currency": "RUB"
                            },
                            "vat_code": 1

                        }
                    ]
                }

            }, uuid.uuid4())

            if code and is_valid_promo_code(code, request):
                Order.objects.create(user=request.user, price=price, rawtext=obj, type='unique_text', type2=type,
                                     transaction_id=payment.id, promo_code=PromoCode.objects.get(code=code))
            else:
                Order.objects.create(user=request.user, price=price, rawtext=obj, type='unique_text',
                                     transaction_id=payment.id, type2=type)
            return HttpResponseRedirect(payment.confirmation.confirmation_url)

            # create payment and redirect to payment page

    return render(request, 'basegpt/uniquetext.html')




def uniquefile(request):
    if request.method == 'POST' and 'getprice' in request.POST:
        obj = request.FILES['rawfile']

        # check if file format is txt
        if obj.name.split('.')[-1] != 'txt':
            return JsonResponse({'type': 'error', 'error': 'Файл должен быть в формате txt'})
        else:





            code = request.POST.get('code')

            text = get_text_from_file(obj)


            if moderation(text) == True:
                return JsonResponse({'type': 'error', 'error': 'Текст не прошел модерацию'})
            else:

                type = request.POST.get('type')



                price = str(get_price_text(text, code, request, type))




                return JsonResponse({'price': price})

    if request.method == 'POST' and 'pay' in request.POST:
        obj = request.FILES['rawfile']

        if obj.name.split('.')[-1] != 'txt':
            return render(request, 'basegpt/uniquefile.html', {'error': 'Файл должен быть в формате txt'})
        else:
            code = request.POST.get('code')
            try:
                text = get_text_from_file(obj)
            except:
                return render(request, 'basegpt/uniquefile.html', {'error': 'Ошибка чтения файла, создайте новый файл'})
            if  moderation(text) == True:
                return render(request, 'basegpt/uniquefile.html', {'error': 'Текст не прошел модерацию'})
            else:

    
                type = request.POST.get('options')

                if type == 'free':
                    # price  =0
                    # order = Order.objects.create(user=request.user, price=price, rawfile=obj, type='unique_file',
                    #                      type2=type, complete = True)
                    #
                    #
                    #
                    #
                    #
                    #
                    # UniqueText.objects.get_or_create(user=order.user, rawfile=order.rawfile, order=order,
                    #                                      type=order.type2)
                    # delete_old_objects(UniqueText, 10, order.user)
                    # return redirect('success')

                   pass

                else:

                    price = str(get_price_text(text, code, request, type))

                    Configuration.account_id = settings.YOOKASSA_SHOP_ID
                    Configuration.secret_key = settings.YOOKASSA_SECRET_KEY
                    payment = Payment.create({
                        "amount": {
                            "value": price,
                            "currency": "RUB"
                        },
                        "confirmation": {
                            "type": "redirect",
                            "return_url": "https://brainstormai.ru/success"
                        },
                        "capture": True,

                        "description": "oreder unique file "+ str(type),
                        "receipt": {
                            "customer": {

                                "email": request.user.email,
                            },
                            "items": [
                                {
                                    "description": "Повышение уникальности" + str(type),
                                    "quantity": "1",
                                    "amount": {
                                        "value": price,
                                        "currency": "RUB"
                                    },
                                    "vat_code": 1


                                }
                            ]
                        }
                    }, uuid.uuid4())
                    if code and is_valid_promo_code(code, request):
                        Order.objects.create(user=request.user, price=price, rawfile=obj, type='unique_file', type2=type,
                                             transaction_id=payment.id, promo_code=PromoCode.objects.get(code=code))
                    else:
                        Order.objects.create(user=request.user, price=price, rawfile=obj, type='unique_file',
                                             transaction_id=payment.id, type2=type)

                    return HttpResponseRedirect(payment.confirmation.confirmation_url)

    return render(request, 'basegpt/uniquefile.html')


class notifications(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        status = request.data['object']['status']

        payment_id = request.data['object']['id']

        if status == 'succeeded':

            order = Order.objects.get(transaction_id=payment_id)
            order.complete = True
            order.save()
            if order.promo_code:
                if User.objects.filter(code=PromoCode.objects.get(code=order.promo_code)).exists():
                    user = User.objects.get(code=PromoCode.objects.get(code=order.promo_code))
                    user.friends += 1
                    user.save()


                PromoCodeUsage.objects.create(user=order.user, promo_code=PromoCode.objects.get(code=order.promo_code))

            if order.type == 'unique_text':
                UniqueText.objects.get_or_create(user=order.user, rawtext=order.rawtext, order=order, type=order.type2)
                delete_old_objects(UniqueText, 10, order.user)
            if order.type == 'unique_file':
                UniqueText.objects.get_or_create(user=order.user, rawfile=order.rawfile, order=order, type=order.type2)
                delete_old_objects(UniqueText, 10, order.user)
            if order.type == 'exam_text':
                ExamText.objects.get_or_create(user=order.user, rawtext=order.rawtext, order=order)
                delete_old_objects(ExamText, 10, order.user)

        status = request.data['object']['status']

        if status == 'canceled':

            try:
                order = Order.objects.get(transaction_id=payment_id)
                order.delete()
            except:
                pass
            return Response(status=200)


        else:
            return Response(status=200)



class CustomLoginView(LoginView):
    template_name = 'basegpt/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('home')

class RegisterPage(FormView):
    template_name = 'basegpt/register.html'
    form_class = UserCreationForm

    redirect_authenticated_user = True
    success_url = reverse_lazy('home')

    def form_valid(self, form):

        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super(RegisterPage, self).get(*args, **kwargs)






def logoutUser(request):
    logout(request)
    return redirect('home')


@login_required(login_url='login')
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.user = request.user
            contact.save()

            return redirect('home')
    else:
        form = ContactForm()
    return render(request, 'basegpt/contact.html', {'form': form})


def session(request):
    if request.method == 'POST':
        ans = ''
        text = request.POST['message']
        model = request.POST['input1']
        role = request.POST['input2']
        temp = float(request.POST['input3'])
        # split texzt by $
        new_text = text.split('$')
        if model == 'gpt-3.5-turbo-1106':
            max_tokens = 4096
        elif model == 'gpt-4-vision-preview':
            max_tokens = 128000

        openai.api_key = settings.OPENAI_API_KEY
        for i in new_text:
            res = openai.ChatCompletion.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": role
                    },

                    {"role": "user",
                     "content": i},
                ],
                temperature=temp,
                max_tokens=max_tokens,
            )
            res_text = res.choices[0]['message']['content']

            ans += res_text + '\n'
        return render(request, 'basegpt/session.html', {'text': ans})

    return render(request, 'basegpt/session.html')