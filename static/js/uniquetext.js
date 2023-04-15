document.addEventListener('DOMContentLoaded', function() {
   $(function() {
        $('#submitunique-text-price').on('click', function(e) {
            e.preventDefault(); // prevent the form from submitting normally
            // send an AJAX request to the server to get the price
            $.ajax({
                type: 'POST',
                url: '/uniquetext',
                data: {
                    'code': $('#promo_code').val(),
                    'type': $('input[name=options]:checked').val(),
                    'rawtext': $('#rawtext').val(),
                    'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                    'action': 'getprice',
                    'getprice': 'getprice'
                },
                success: function(data) {
                    // update the content of the result div with the response data

                    if (data['type'] === 'error') {
                    $('#price').text(data['error']);

            } else  {
                    $('#price').text('Цена: ' + data['price'] + '  Рублей');
                }
                },


            });
        });
    });
    });
