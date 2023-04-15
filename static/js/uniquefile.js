document.addEventListener('DOMContentLoaded', function() {
$(function() {
    $('#submitunique-file-price').on('click', function(e) {
        e.preventDefault(); // prevent the form from submitting normally

        // get the file input element
        var fileInput = $('#rawfile')[0];

        // check if a file was selected
        if (fileInput.files.length > 0) {
            // create a FormData object and append the file and other form data to it
            var formData = new FormData();
            formData.append('type', $('input[name=options]:checked').val());

            formData.append('code', $('#promo_code').val());
            formData.append('rawfile', fileInput.files[0]);
            formData.append('csrfmiddlewaretoken', $('input[name=csrfmiddlewaretoken]').val());
            formData.append('action', 'getprice');
            formData.append('getprice', 'getprice');


            // send an AJAX request to the server to get the price
            $.ajax({
                type: 'POST',
                url: '/uniquefile',
                data: formData,
                processData: false, // prevent jQuery from processing the data
                contentType: false, // prevent jQuery from setting the content type
                success: function(data) {
                    // update the content of the result div with the response data
                    if (data['type'] === 'error') {
                    $('#price').text(data['error']);

            } else  {
                    $('#price').text('Цена: ' + data['price'] + '  Рублей');
                }
                },
            });
        } else {
            // display an error message if no file was selected
            alert('Please select a file.');
        }
    });
});
});


