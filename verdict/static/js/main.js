$(document).ready(function(){

    var check_input = $('form#check input[type=text]');
    var check_submit = $('form#check input[type=submit]');

    check_submit.click(function(event){
        checkPhoneNumber(event);
    });
    check_submit.keypress(function(event){
        if (event.which == 13) // if the ENTER key is pressed
            checkPhoneNumber(event);
    });

    check_input.mask("(999) 999-9999").focus();
});

function checkPhoneNumber(event) {
    event.preventDefault();
    var contents = $('form#check input[type=text]').val();
    var number = contents.match(/[0-9]/g).join('');
    if (number.length < 10)
        inputError("Whoops! That number is less than 10 digits.")
    else
        ajaxPost({number: number},
                 '/api/check/',
                 function(response){ console.log(response) });
}

function inputError(msg) {
    $('.input.error').text(msg).stop().css("opacity", "1").fadeTo(10000, 0.6);
}

/* utility functions */

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function ajaxPost(params, endpoint, callback_success) {
    params.csrfmiddlewaretoken = getCookie('csrftoken');
    $.ajax({
        type: "POST",
        url: endpoint,
        data: params,
        success: callback_success,
        error: function(xhr, textStatus, errorThrown) {
            alert("Oh no! Something went wrong. Please report this error: \n"+errorThrown+xhr.status+xhr.responseText);
        }
    }); 
}
