document.addEventListener('DOMContentLoaded', function() {


  const loaderDiv = document.getElementById('loader-div');
  const button = document.getElementById('submit-button');
  const overlayDiv = document.getElementById('overlay');

  // Attach an event listener to the button with id 'submit-button'


    button.addEventListener('click', function(event) {

      // Prevent the default form submission behavior
      event.preventDefault();
      // log






      //get id of textarea #rawtext
        var rawtext = document.getElementById('rawtext');
        var audience = document.getElementById('audience');
        var platform = document.getElementById('platform');
        if (rawtext.value === '') {

            rawtext.placeholder = 'Обязательное поле. Заполните описание вашего продукта или услуги';
            rawtext.focus();

            return;
            }

      loaderDiv.style.display = 'block';

      overlayDiv.style.display = 'block';
        // get type 'type', $('input[name=options]:checked').val()
        var type = document.querySelector('input[name=options]:checked').value;
        //log type and rawtext
        console.log('type');
        console.log(type);

        console.log(rawtext.value);

        // send

      fetch('/infotext', {
        method: 'POST',
        body: JSON.stringify({
    'rawtext': rawtext.value,
    'type': type,
    'audience': audience.value,
    'platform': platform.value
  }),
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': document.getElementsByName('csrfmiddlewaretoken')[0].value
        },
      })
      .then(response => {
        return response.json(); // This converts the response to JSON
      })
      .then(data => {
        if (data['status'] === 'ok') {

//          sendRequest();
          document.getElementById("overlay").style.display = "none";
          loaderDiv.style.display = 'none';
            var copybutton = document.getElementById('copy-button');
            copybutton.style.display = 'block';
          // Выводим результат в textarea
            var responsearea = document.getElementById('resultarea');
            var responseDiv = document.getElementById('textarea-result');
            var rating = document.getElementById('rating');

//            rating input to 0
            var ratingRadios = document.querySelectorAll('input[name="rate"]');
            ratingRadios.forEach(radio => {
                radio.checked = false;

            }
            );
            //bookmark to false
            var bookmarkCheckbox = document.getElementById('bookmark');
            bookmarkCheckbox.checked = false;


            responsearea.style.display = 'block';
            responseDiv.style.display = 'flex';
            rating.style.display = 'block';


            //clear textarea
            responsearea.value = '';
            responsearea.value = data['result'];
            responsearea.setAttribute('data-value', data['id']);



            console.log(data['result']);

          console.log("Задача выполнена!");

        }
        else {
            if (data['status'] === 'error') {
                console.log('error');
                console.log(data['result']);
                document.getElementById("overlay").style.display = "none";
                loaderDiv.style.display = 'none';

                //redirect to balance
                if (data['result'] === 'Недостаточно средств на балансе') {
                    window.location.href = '/balance';
                }

                 // Создаем элемент для сообщения
    const alertBox = document.createElement('div');
    alertBox.textContent = data['result']; // Текст сообщения
    alertBox.style.position = 'fixed'; // Фиксированное позиционирование
    alertBox.style.top = '30%'; // Отступ сверху
    alertBox.style.left = '50%'; // Отступ слева
    alertBox.style.transform = 'translate(-50%, -50%)'; // Центрирование
    alertBox.style.padding = '20px'; // Отступы внутри блока
    alertBox.style.backgroundColor = '#ff5c5c'; // Красный фон
    alertBox.style.color = 'white'; // Белый цвет текста
    alertBox.style.fontSize = '16px'; // Размер шрифта
    alertBox.style.borderRadius = '10px'; // Скругленные углы
    alertBox.style.boxShadow = '0px 0px 10px rgba(0,0,0,0.5)'; // Тень
    alertBox.style.zIndex = '1000'; // Z-индекс

    document.body.appendChild(alertBox); // Добавляем элемент в тело документа

    // Удаляем элемент через 5 секунд
    setTimeout(() => {
        document.body.removeChild(alertBox);
    }, 5000);





//                alert error

            }
        }
      })
    })

   var copyButton = document.getElementById('copy-button');

    copyButton.addEventListener('click', function(event) {
        copyText();
    }
    );
    // onclick="copyText() copy from rawtext to clipboard
   function copyText() {
  // Получаем элемент textarea
  var textArea = document.getElementById("resultarea");
  // Выделяем фон на 2 секунды и плавно возвращаем обратно

//    textArea.style.backgroundColor = 'lightgreen';
//    setTimeout(function() {
//      textArea.style.backgroundColor = 'white';
//    }, 1000);
    // внутри кнопки зеленая галочка
//    var copyButton = document.getElementById('copy-button');
//    copyButton.innerHTML = '✅ Скопировано';
//    setTimeout(function() {
//      copyButton.innerHTML = 'Копировать';
//    }, 1000);



  // Используем API буфера обмена для копирования текста
  navigator.clipboard.writeText(textArea.value)
    .then(() => {
      // После успешного копирования, можно, например, отобразить уведомление
      console.log("Текст успешно скопирован в буфер обмена");
    })
    .catch(err => {
      // В случае ошибки копирования
      console.error("Ошибка при копировании текста: ", err);
    });

  // Важно предотвратить стандартное поведение кнопки, чтобы избежать перезагрузки страницы
  event.preventDefault();
}

// Получаем элементы по их идентификаторам
var rawTextElement = document.getElementById('rawtext');
var textareaProductElement = document.getElementById('textarea-product');

// Проверяем, существуют ли эти элементы
if (rawTextElement && textareaProductElement) {
  // Добавляем обработчик события фокусировки на элемент rawtext
  rawTextElement.addEventListener('focus', function() {
    // Меняем стиль границы у элемента textarea-product при фокусе на rawtext
    textareaProductElement.style.outline = '2px solid #7D32FF';
    // scale textarea-product

  });

  // Добавляем обработчик события потери фокуса на элемент rawtext
  rawTextElement.addEventListener('blur', function() {
    // Возвращаем стиль границы у элемента textarea-product к исходному состоянию
    // или к любому другому необходимому состоянию
    textareaProductElement.style.outline = 'none';
    // scale textarea-product

  });
}

const ratingRadios = document.querySelectorAll('input[name="rate"]');
  ratingRadios.forEach(radio => {
    radio.addEventListener('change', function() {
      if (this.checked) {
        sendRatingToAPI(this.value);
      }
    });
  });

  function sendRatingToAPI(rating) {
   var responsearea = document.getElementById('resultarea');

    var id = responsearea.dataset.value;

    fetch('/user_rating', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
                  'X-CSRFToken': document.getElementsByName('csrfmiddlewaretoken')[0].value
      },
      body: JSON.stringify({
        rating: rating,
        id: id
      })
    })

  }

    const bookmarkCheckbox = document.getElementById('bookmark');

  bookmarkCheckbox.addEventListener('change', function() {
    if (this.checked) {
      sendRequestToAPI();
    }
  });

  function sendRequestToAPI() {
     var responsearea = document.getElementById('resultarea');

    var id = responsearea.dataset.value;
    fetch('/favorite', { // Replace with your actual API endpoint
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
'X-CSRFToken': document.getElementsByName('csrfmiddlewaretoken')[0].value
      },
      body: JSON.stringify({
        id: id
      })
    })

  }


  });


