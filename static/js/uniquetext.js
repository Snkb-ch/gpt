document.addEventListener('DOMContentLoaded', function() {
  function sendRequest() {


    $.ajax({
      url: "/infotext_result",
      type: "GET",
        data: {

            'csrfmiddlewaretoken': document.getElementsByName('csrfmiddlewaretoken')[0].value

        }
        ,



      success: function(data) {
        if (data.status == "ok") {
          // Нужный ответ получен, останавливаем отправку запросов
          document.getElementById("overlay").style.display = "none";
          loaderDiv.style.display = 'none';
          // Выводим результат в textarea
            var responseDiv = document.getElementById('rawtext');
            //clear textarea
            responseDiv.value = '';
            responseDiv.value = data['result'];


            console.log(data['result']);

          console.log("Задача выполнена!");
        } else {
          if (data.status == "wait") {
            // Нужный ответ не получен, отправляем запрос снова через 5 секунд
            setTimeout(function() {
                sendRequest(order);
            }, 5000);

          } else {
            if (data.status == "error") {
              responseDiv.textContent = data['error'];
              console.log(data['error']);

            }
          }
        }
      }
    });
  }

  // Запускаем отправку запросов


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
            console.log('ok');
            console.log(data['result']);
//          sendRequest();
          document.getElementById("overlay").style.display = "none";
          loaderDiv.style.display = 'none';
          // Выводим результат в textarea
            var responseDiv = document.getElementById('rawtext');
            //clear textarea
            responseDiv.value = '';
            responseDiv.value = data['result'];


            console.log(data['result']);

          console.log("Задача выполнена!");
        }
      })
    })
  });

