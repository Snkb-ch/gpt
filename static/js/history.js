
function copyText(name) {

  var preElements = document.getElementsByTagName("pre");
  for (var i = 0; i < preElements.length; i++) {
    if (preElements[i].getAttribute("name") == name) {
      var textToCopy = preElements[i].textContent;
      navigator.clipboard.writeText(textToCopy);
      break;
    }
  }
}


 const bookmarkCheckbox = document.getElementById('bookmark');



  function sendRequestToAPI(id) {


    console.log(id);
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


document.addEventListener('DOMContentLoaded', function() {

 const containers = document.querySelectorAll('.response-container3');

  // Перебираем контейнеры


  // Перебираем контейнеры
  containers.forEach(function(container) {
    // Проверяем, находится ли элемент в избранном
    if (container.dataset.favorite === 'True') {
      // id of the element
      var id = container.id;
          console.log(id);
//      get element with class 'bookmark' and data-vqlue = id
        var bookmark = document.querySelector('#bookmark[data-value="' + id + '"]');
        // Check the checkbox
        bookmark.checked = true;

    }
  });


  let showFavoritesOnly = true;

  const button = document.getElementById('filter');
  button.addEventListener('click', function() {
    // Получаем все элементы с классом 'response-container3'
    var containers = document.querySelectorAll('.response-container3');

    // Проверяем, что показывать
    if (showFavoritesOnly) {
      // Меняем текст кнопки
      button.textContent = 'Показать все';

      // Показываем только избранное
      containers.forEach(function(container) {
        if (container.dataset.favorite !== 'True') {
          container.style.display = 'none';
        } else {
          container.style.display = 'flex';
        }
      });
    } else {
      // Меняем текст кнопки обратно
      button.textContent = 'Показать избранное';

      // Показываем все элементы
      containers.forEach(function(container) {
        container.style.display = 'flex';
      });
    }

    // Переключаем состояние
    showFavoritesOnly = !showFavoritesOnly;
  });

});

