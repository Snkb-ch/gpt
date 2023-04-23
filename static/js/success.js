document.addEventListener('DOMContentLoaded', function() {
  function sendRequest(buttonValue) {
  console.log(buttonValue);

  const order = buttonValue;
  console.log(order);


    $.ajax({
      url: "/success_result",
      type: "POST",
        data: {
            'order': order,
            'csrfmiddlewaretoken': document.getElementsByName('csrfmiddlewaretoken')[0].value

        }
        ,



      success: function(data) {
        if (data.status == "ok") {
          // Нужный ответ получен, останавливаем отправку запросов
          document.getElementById("overlay").style.display = "none";
          loaderDiv.style.display = 'none';
            responseDiv.style.display = 'block';

          if (data['type'] === 'text') {
            responseDiv.textContent = data['response_text'];
            var submitButton = document.getElementById(buttonValue);
            submitButton.disabled = true;
          } else if (data['type'] === 'file') {
            responseDiv.innerHTML = `<a href="${data['file_url']}" class = "btn-pay" style = " margin:auto; " download>Скачать результат</a>`;
            var submitButton = document.getElementById(buttonValue);
            submitButton.disabled = true;
          }
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
              var submitButton = document.getElementById(buttonValue);
              submitButton.disabled = true;
            }
          }
        }
      }
    });
  }

  // Запускаем отправку запросов
  const responseDiv = document.getElementById('response-div');
  const loaderDiv = document.getElementById('loader-div');
  const buttons = document.querySelectorAll('.submitexe');
  const overlayDiv = document.getElementById('overlay');

  // Attach an event listener to the button
  buttons.forEach(function(button) {
    button.addEventListener('click', (event) => {
      // Prevent the default form submission behavior
      event.preventDefault();

      // Get the value of the button
      const buttonValue = event.target.value;

      loaderDiv.style.display = 'block';
      responseDiv.style.display = 'none';
      overlayDiv.style.display = 'block';

      fetch('/success_api', {
        method: 'POST',
        body: JSON.stringify({ buttonValue }),
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
            console.log(buttonValue);
          sendRequest(buttonValue);
        }
      })
    })
  })
});
