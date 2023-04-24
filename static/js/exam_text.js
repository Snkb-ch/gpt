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




// Function to start the crawl and periodically check on its status
function getIdea() {

  // Make AJAX request to startCrawl URL
  $.ajax({
    url: "/exam_text_get_idea",
    type: "POST",
    data: {
                'rawtext': $('#rawtext').val(),
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                'action': 'get_idea',
                'get_idea': 'get_idea'
            },
    success: function(response) {
        if (response['type'] === 'error') {
            $('#idea-from-ai').text(response['error']);
            loaderDiv.style.display = 'none';
                document.getElementById("overlay").style.display = "none";
        }
        else if (response['type'] === 'ok') {
      // Store the ID of the crawl task
      var crawlId = response.id;

      // Check on the status of the crawl every 5 seconds
      var intervalId = setInterval(function() {
        $.ajax({
          url: "/check_idea/" + crawlId + "/",
          type: "GET",

          success: function(response) {
            if (response['status'] === 'done') {
              // Stop checking for crawl status
              clearInterval(intervalId);

              // Display the result to the user
                $('#idea-from-ai').text(response['idea']);
                loaderDiv.style.display = 'none';
                document.getElementById("overlay").style.display = "none";
                document.getElementById("copy").style.display = "block";

            }
            else if (response['status'] === 'error') {

                // Stop checking for crawl status
                clearInterval(intervalId);

                // Display the error to the user
                $('#idea-from-ai').text(response['error']);
                loaderDiv.style.display = 'none';
                document.getElementById("overlay").style.display = "none";
            }
          }
        });
      }, 5000); // Check every 5 seconds
    }
    }
  });
}







$(function() {
    $('#get_idea').on('click', function(e) {
        e.preventDefault();
        overlayDiv.style.display = 'block';
        loaderDiv.style.display = 'block';
        getIdea();


    });
    $('#copy').on('click', function(e) {
        e.preventDefault();
        copyButtonClicked = true; // set the flag variable to true
        copyText();
    });
});
});