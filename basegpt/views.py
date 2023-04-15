import json
import traceback

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.conf import settings

from django.contrib import messages

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

    uniquetexts = UniqueText.objects.filter(user=request.user)
    examtexts = ExamText.objects.filter(user=request.user)

    return render(request, 'basegpt/history.html', {'uniquetexts': uniquetexts, 'examtexts': examtexts})






    return render(request, 'basegpt/history.html')
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

        print(transcript)

    return render(request, 'basegpt/audio.html', {'transcript': transcript})


def error(request):
    return render(request, 'basegpt/error.html')


def get_objects(request):
    my_objects = UniqueText.objects.all()
    data = [{'rawfile': obj.rawfile.name, 'responsefile': obj.responsefile.name} for obj in my_objects]
    return JsonResponse({'data': data})


def refund(order):
    Configuration.account_id = '202517'
    Configuration.secret_key = 'test_NaEt-DpTS6rVYC9KS6EmcNDbvAlXh5JNrSZUF4UvlWk'
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


def home(request):
    return render(request, 'basegpt/home.html')


def split_text_on_parts(text, max_length):
    sentences = text.split(". ")
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
    parts = split_text_on_parts(text, 1500)
    for i in range(len(parts)):
        print('hey')

        openai.api_key = settings.OPENAI_API_KEY

        ans = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": 'Очень сильно перефразируй текст. Наполни его синонимами. Добавь еще предложения и абзацы, но главное сохрани суть целого текста. Нельзя менять фамилии, даты, цифры, названия глав и произведений, а также цитаты. Будь многословным и абстрактным, но держись научного стиля. Не повторяйся. Нельзя использовать одинаковые и однокоренные слова в соседних предложениях.'
                },

                {"role": "user",
                 "content": parts[i]},
            ],
            temperature=0.7,
            max_tokens=2048,
        )
        parts[i] = ans.choices[0]['message']['content']

    response_text = ''.join(parts)
    print('end')
    return response_text


def red2_for_unique_text(text):
    parts = split_text_on_parts(text, 1500)
    for i in range(len(parts)):
        print('hey')

        openai.api_key = settings.OPENAI_API_KEY

        ans = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": 'Создай новый уникальный научный текст основываясь на этом исходном тексте. Используй научный стиль. Используй разные конструкции предложений разной длины. Используй разные неочевидные синонимы. Если в исходном тексте есть фамилии, цитаты, названия произведений, цифры, даты используй их в своем тексте. Это значит, что информация из исходного текста обязана быть в твоем в том или ином виде. Будь многословным. Не повторяйся. Не используй одинаковые и однокоренные слова в соседних предложениях.Не пиши заключение.'
                },

                {"role": "user",
                 "content": parts[i]},
            ],
            temperature=0.7,
            max_tokens=2048,
        )
        parts[i] = ans.choices[0]['message']['content']

    response_text = ''.join(parts)
    print('end')
    return response_text


def red3_for_unique_text(text):
    parts = split_text_on_parts(text, 1500)
    for i in range(len(parts)):
        print('hey')

        openai.api_key = settings.OPENAI_API_KEY

        ans = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": '.Создай новый уникальный научный текст основываясь на этом исходном тексте. Используй научный стиль. Используй разные конструкции предложений разной длины. Используй разные неочевидные синонимы. Если в исходном тексте есть фамилии, цитаты, названия произведений, цифры используй их в своем. Будь многословным. Не повторяйся. Не используй одинаковые и однокоренные слова в соседних предложениях. Не пиши заключение.'
                },

                {"role": "user",
                 "content": parts[i]},
            ],
            temperature=0.7,
            max_tokens=2048,
        )
        parts[i] = ans.choices[0]['message']['content']

    response_text = ''.join(parts)
    print('end')
    return response_text


def exam_text_result(text, idea):
    print('start exam_text_result')

    openai.api_key = settings.OPENAI_API_KEY
    answer = idea + '\n'

    red2 = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": 'Идея текста:' + idea + 'Тебе нужно привести два примера из текста подтверждающих философскую идею  текста. После каждого из  примеров напиши свой комментарий объясняющий как именно пример подтверждает философскую идею текста . В качестве примера можно использовать короткие цитаты, короткий пересказ истории, размышления автора и т.п. Приведенные примеры должны иметь логическую связь (можно их сравнить или противопоставить). После в самом конце своего текста свяжи примеры, обобщи их, расскажи как два этих примера подтверждают философскую идею текста. Нельзя использовать вводные слова и конструкции. Пиши свой текст цельно, так как будто ты пишешь сочинение на тему. Используй художественный стиль изложения. Чтобы не повторяться используй синонимы. Если хочешь написать слово или словосочетание, которое было в текст замени его на синоним. Пиши как человек. Используй разную длину предложений. Пиши ярко. Не пиши "Пример 1:" или "Пример 2:". Старайся писать по сути и немногослвоно'
            },

            {"role": "user",
             "content": text},
        ],
        temperature=0.45,
        max_tokens=1000,
    )

    red2 = red2.choices[0]['message']['content']
    print('red2')
    print(red2)

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
    # print('red3')
    # print(red3)
    answer += (red2 + '\n')

    red4 = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": 'Идея текста:' + idea + 'тебе нужно написать Отношение автора подтверждающее эту идею. Здесь нужно подвести текст к следующей части сочинения — выражение собственного мнения. Отношение автора — это его ответ на сформулированные вами вопросы, его видение проблемы. В этой части стоит изложить мысль, которая соотносится с общепринятой позицией, но не нужно вдаваться в спорные утверждения. Для выражения отношения автора также можно использовать клише, например:Позиция автора такова: он считает...Авторская позиция состоит в том, что...ПИШИ МАКСИМАЛЬНО КРАТКО. Одна максимум два коротких предложения. Свою позицию писать не надоОтвет на проблемный вопрос, данный автором текста	В начале текста обязательно используй одну из этих фраз на выборАвтор подводит читателя к выводу о том, что…Рассуждая над проблемой, автор приходит к следующему выводу…Так автор убеждает нас в том, что…'
            },

            {"role": "user",
             "content": text},
        ],
        temperature=0.3,
        max_tokens=738,
    )

    red4 = red4.choices[0]['message']['content']
    print('red4')
    print(red4)

    red5 = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": 'Сократи заметно текст замени слова на синонимы, не меняя фразы: Рассуждая над проблемой, автор приходит к следующему выводу'
            },

            {"role": "user",
             "content": red4},
        ],
        temperature=0.4,
        max_tokens=2048,
    )

    red5 = red5.choices[0]['message']['content']
    print('red5')
    print(red5)

    answer += (red5 + '\n')

    red6 = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": 'Идея текста:' + idea + 'Преврати текст в собственную позицию и добавь аргументацию этой позиции из литературы, которая не указана в тексте. Перефразируй.Текст должен быть максимум на 3-4 коротких предложения.Текст начинай со слов "Я согласен с автором"'
            },

            {"role": "user",
             "content": text},
        ],
        temperature=0.4,
        max_tokens=1020,
    )

    red6 = red6.choices[0]['message']['content']
    print('red6')
    print(red6)

    answer += (red6 + '\n')

    red7 = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": 'Идея текста:' + idea + 'Заключение. Напиши максимум 1 предложения.  В этой части постройте заключение в обратной последовательности вступительной части, начав кратко и закончив развернуто. Обобщение всего написанного должно быть кратким и емким, отражать концентрированно проблему, позицию автора и собственное мнение. Простой пересказ текста вступления не подойдет, проведите параллель с ним, поделитесь впечатлением. В заключении должна быть проведена логическая связь между всеми частями и сделан общий вывод. Сделать это помогут клише:После прочтения этого произведения становится понятно...Подводя итоги сказанного, можно сделать вывод...Этот текст заставил меня еще раз убедиться...'
            },

            {"role": "user",
             "content": red6},
        ],
        temperature=0.4,
        max_tokens=2048,
    )

    red7 = red7.choices[0]['message']['content']
    print('red7')
    print(red7)

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
            response_text = red1_for_unique_text(text)
        elif type == 'red2':
            response_text = red2_for_unique_text(text)
        elif type == 'red3':
            response_text = red3_for_unique_text(text)
        elif type == 'exam_text':
            response_text = exam_text_result(text, order.idea)

        if moderation(response_text) == True:
            raise Exception('moderation error')
        else:

            return response_text






    except Exception as e:
        # if runtime error, say try later
        # if token error, do it again but with a different limits
        print(e)
        traceback.print_exc()

        response = 'error except'
        print(response)
        return response


def success_unique_text(request, order):
    result_obj = UniqueText.objects.get(user=order.user, rawtext=order.rawtext, order=order)
    result_obj.complete = True
    result_obj.save()
    response_text = getresultfromtext(order.rawtext, order.type2, order)



    obj = UniqueText.objects.get(user=order.user, order=order)
    if response_text == 'error' and obj.complete == False:
        print('error success')
        refund(order)
        response = ({'type': 'error', 'error': 'error payment canceled'})




    elif response_text != 'error':

        result_obj.responsetext = response_text

        result_obj.save()
        order.result = True
        order.save()

        response = ({'type': 'text', 'response_text': response_text})

    return response


def success_unique_file(request, order):
    file_content = order.rawfile.read().decode('utf-8')
    obj = UniqueText.objects.get(user=order.user, order=order)
    obj.complete = True
    obj.save()
    response_file_text = getresultfromtext(file_content, order.type2, order)

    if response_file_text == 'error' and obj.complete == False:
        print('error')
        refund(order)
        response = ({'type': 'error', 'error': 'error payment canceled'})
        return response


    elif response_file_text != 'error':
        # UniqueText.objects.get_or_create(user=order.user, rawfile=order.rawfile, order=order)
        obj = UniqueText.objects.get(user=order.user, order=order)
        obj.responsefile.name = 'responsefiles/responsefile' + str(obj.order_id) + '.txt'

        obj.save()

        with open(obj.responsefile.path, 'w') as f:
            f.write(response_file_text)

        delete_old_objects(UniqueText, 10, order.user)
        order.result = True
        order.save()
        file_url = obj.responsefile.url
        response = ({'type': 'file', 'file_url': file_url})
        return response


def success_exam_text(request, order):
    result_obj = ExamText.objects.get(user=order.user, rawtext=order.rawtext, order=order)
    result_obj.complete = True
    result_obj.save()
    response_text = getresultfromtext(order.rawtext, order.type, order)
    obj = ExamText.objects.get(user=order.user, order=order)
    if response_text == 'error' and obj.complete == False:
        print('error')
        refund(order)
        response = ({'type': 'error', 'error': 'error payment canceled'})




    elif response_text != 'error':

        result_obj.responsetext = response_text

        result_obj.save()
        order.result = True
        order.save()

        response = ({'type': 'text', 'response_text': response_text})

    return response


@login_required(login_url='login')
def success(request):
    if request.method == 'POST':
        print('post')
        data = json.loads(request.body)
        button_value = data.get('buttonValue')
        order = Order.objects.get(id=button_value, user=request.user)

        if order.type == 'unique_text':
            response = success_unique_text(request, order)

            return JsonResponse(response)




        elif order.type == 'unique_file':
            response = success_unique_file(request, order)

            return JsonResponse(response)

        elif order.type == 'exam_text':
            response = success_exam_text(request, order)
            return JsonResponse(response)

    objects = UniqueText.objects.filter(user=request.user, complete=False)

    exam_objects = ExamText.objects.filter(user=request.user, complete=False)

    return render(request, 'basegpt/success.html', {'objects': objects, 'exam_objects': exam_objects})


def delete_old_objects(model, limit, user):
    #
    count = model.objects.filter(user=user).count()
    print(count)
    if count > limit:
        oldest = model.objects.earliest('created_at')
        oldest.delete()
        return True
    return False

def moderation(text):
    openai.api_key = settings.OPENAI_API_KEY

    moderation = openai.Moderation.create(
        input=text,
    )
    output = moderation["results"][0]["flagged"]


    return output

@login_required(login_url='login')
def exam_text(request):
    if request.method == 'POST' and 'get_idea' in request.POST:

        text = request.POST.get('rawtext')
        if moderation(text) == True:
            return JsonResponse({'type': 'error', 'error': 'error text is not allowed'})

        else:

            try:

                openai.api_key = settings.OPENAI_API_KEY

                idea = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {
                            "role": "system",
                            "content": 'Какая философская проблема текста которую можно считать вечной и глобальной в литературе в литературе? Не привязывайся к личности. Мысли широко. Обобщи. Не углубляясь в детали, не используя цитаты и пересказ.  Ответ должен быть максимум в 10 слов. А после напиши: "Именно над этим предлагает задуматься автор". Проблема должна быть понятна каждому человеку на планете  который сможет примерить эту идею на свою жизнь.'
                                       },

                        {"role": "user",
                         "content": text},
                    ],
                    temperature=1,
                    max_tokens=1000,
                )

                idea = idea.choices[0]['message']['content']
                print(idea)

                return JsonResponse({'idea': idea})
            except:
                return JsonResponse({'type': 'error', 'error': 'Сократите текст'})

    if request.method == 'POST' and 'pay' in request.POST:
        idea = request.POST.get('idea')
        obj = request.POST.get('rawtext')
        code = request.POST.get('code')
        type = 'exam_text'

        if moderation(obj) == True:
            return render(request, 'basegpt/exam_text.html', {'error': 'error'})
        else:
            if code and is_valid_promo_code(code, request):
                promo = PromoCode.objects.get(code=code)
                discount = promo.discount
                price = 15 - (15 * discount / 100)
            else:
                price = 15

            Configuration.account_id = '202517'
            Configuration.secret_key = 'test_NaEt-DpTS6rVYC9KS6EmcNDbvAlXh5JNrSZUF4UvlWk'
            payment = Payment.create({
                "amount": {
                    "value": price,
                    "currency": "RUB"
                },
                "confirmation": {
                    "type": "redirect",
                    "return_url": "https://127.0.0.1/success"
                },
                "capture": True,
                "description": "сочинение егэ по русскому "
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
    print(type)
    price = 0


    text = str(text)

    if code and is_valid_promo_code(code, request):
        promo = PromoCode.objects.get(code=code)
        discount = promo.discount
    else:
        promo = None
        discount = 0

    if type == 'red1':
        print('red1')
        price = int(len(text) * 0.0037 * (100 - discount) / 100)
    elif type == 'red2':
        price = int(len(text) * 0.0063 * (100 - discount) / 100)
    elif type == 'red3':
        price = int(len(text) * 0.0063 * (100 - discount) / 100)


    return price


@login_required(login_url='login')
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

            Configuration.account_id = '202517'
            Configuration.secret_key = 'test_NaEt-DpTS6rVYC9KS6EmcNDbvAlXh5JNrSZUF4UvlWk'
            payment = Payment.create({
                "amount": {
                    "value": price,
                    "currency": "RUB"
                },
                "confirmation": {
                    "type": "redirect",
                    "return_url": "https://127.0.0.1/success"
                },
                "capture": True,
                "description": "oreder unique text " + str(type)
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


@login_required(login_url='login')
def uniquefile(request):
    if request.method == 'POST' and 'getprice' in request.POST:
        obj = request.FILES['rawfile']

        # check if file format is txt
        if obj.name.split('.')[-1] != 'txt':
            return JsonResponse({'type': 'error', 'error': 'Файл должен быть в формате txt'})
        else:





            code = request.POST.get('code')

            text = get_text_from_file(obj)
            print(text)

            if moderation(text) == True:
                return JsonResponse({'type': 'error', 'error': 'Текст не прошел модерацию'})
            else:

                type = request.POST.get('type')



                price = str(get_price_text(text, code, request, type))
                print(price)

                return JsonResponse({'price': price})

    if request.method == 'POST' and 'pay' in request.POST:
        obj = request.FILES['rawfile']
        if obj.name.split('.')[-1] != 'txt':
            return render(request, 'basegpt/uniquefile.html', {'error': 'Файл должен быть в формате txt'})
        else:
            code = request.POST.get('code')
            text = get_text_from_file(obj)
            if moderation(text) == True:
                return render(request, 'basegpt/uniquefile.html', {'error': 'Текст не прошел модерацию'})
            else:

    
                type = request.POST.get('options')

                price = str(get_price_text(text, code, request, type))

                Configuration.account_id = '202517'
                Configuration.secret_key = 'test_NaEt-DpTS6rVYC9KS6EmcNDbvAlXh5JNrSZUF4UvlWk'
                payment = Payment.create({
                    "amount": {
                        "value": price,
                        "currency": "RUB"
                    },
                    "confirmation": {
                        "type": "redirect",
                        "return_url": "https://127.0.0.1/success"
                    },
                    "capture": True,

                    "description": "oreder unique file "+ str(type),
                    "receipt": {
                        "customer": {

                            "email": "snk2032@gmail.com"
                        },
                        "items": [
                            {
                                "description": "Повышение уникальности",
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
        print(status)
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
                    print('friends')

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
        print('test')
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
