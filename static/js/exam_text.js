document.addEventListener('DOMContentLoaded', function() {
const use_idea = document.getElementById('use_idea');
const loaderDiv = document.getElementById('loader-div');
const overlayDiv = document.getElementById('overlay');
let copyButtonClicked = false; // add flag variable
function copyText() {
  if (copyButtonClicked) { // check if the button was clicked
    var source = document.getElementById("idea-from-ai");
    var destination = document.getElementById("idea");
    destination.value = source.innerText;
  }
}
$(function() {
    $('#get_idea').on('click', function(e) {
        e.preventDefault();
        overlayDiv.style.display = 'block';
        loaderDiv.style.display = 'block';

        $.ajax({
            type: 'POST',
            url: '/exam-text',
            data: {
                'rawtext': $('#rawtext').val(),
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                'action': 'get_idea',
                'get_idea': 'get_idea'
            },
            success: function(data) {
                document.getElementById("copy").style.display = "block";


                loaderDiv.style.display = 'none';
                document.getElementById("overlay").style.display = "none";
                console.log('Received idea data:', data['idea']);

                 if (data['type'] === 'error') {
                    $('#idea-from-ai').text(data['error']);

            } else if (data['idea']) {
                    $('#idea-from-ai').text(data['idea']);
                }
                },
        });
    });
    $('#copy').on('click', function(e) {
        e.preventDefault();
        copyButtonClicked = true; // set the flag variable to true
        copyText();
    });
});
});