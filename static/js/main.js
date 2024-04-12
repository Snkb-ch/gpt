//<!--      ajax get to get_balance for user-->


document.addEventListener('DOMContentLoaded', function() {
$.ajax({
    url: "/get_balance",
    type: "GET",
        data: {

            'csrfmiddlewaretoken': document.getElementsByName('csrfmiddlewaretoken')[0].value

        }
        ,
        success: function(data) {

                // get id balcance
                var balance = document.getElementById('balance');
                // set balance
                balance.innerHTML = data['balance'];

        }
    });

    $("li").mouseover(function(){
 $(this).find('.drop-down').slideDown(300);
 $(this).find(".accent").addClass("animate");
 $(this).find(".item").css("color","#FFF");
}).mouseleave(function(){
  $(this).find(".drop-down").slideUp(300);
   $(this).find(".accent").removeClass("animate");
   $(this).find(".item").css("color","#000");
});



}
);

