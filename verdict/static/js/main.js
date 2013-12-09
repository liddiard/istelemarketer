$(document).ready(function(){
    $('input#phone-number').keypress(function(event){
        if (event.which == 13) // if the ENTER key is pressed
            checkPhoneNumber(event);
    });
    $('input#phone-number').mask("(999) 999-9999").focus();
});

function checkPhoneNumber(event) {
    event.preventDefault();
    var contents = $('form#check input[type=text]').val();
    try {
        var number = contents.match(/[0-9]/g).join('');
    } catch (ex) {
        var number = ""
    }
    if (number.length < 10)
        inputError("Whoops! That number is less than 10 digits.")
    else {
        $('.input.error').text('');
        ajaxPost({number: number},
                 '/api/check/',
                 showVerdict);
        $('input#phone-number').addClass('disabled').prop('disabled', true);
    }
}

function showVerdict(response) {
    var results = response.results;
    var positive_matches = []
    var negative_matches = []
    // separate results out into two arrays
    for (var i = 0; i < results.length; i++) {
        if (results[i].verdict)
            positive_matches.push(results[i]);
        else
            negative_matches.push(results[i]);
    }
    // change display of the page according to the results
    if (positive_matches.length > 0) { // this is a telemarketer
        $('body').removeClass('good').addClass('bad');
        $('#banner').attr('src', '../img/banner_invert.png');
        $('#verdict').text('Yes');
        $('#report').html(generateBadExplainerText(positive_matches));
    }
    else { // this isn't a telemarketer
        $('body').removeClass('bad').addClass('good');
        $('#banner').attr('src', '../img/invert.png');
        $('#verdict').text('No');
        $('#report').html('No complaints found; this caller probably isn&rsquo;t a telemarketer.')
    }
    $('input#phone-number').removeClass('disabled').prop('disabled', false);
}

function generateBadExplainerText(positive_matches) {
    // expects length of positive_matches to be greater than zero
    var nut = "This caller is a telemarketer according to "
    if (positive_matches.length === 1) {
        return nut + generateLink(positive_matches[0].url, positive_matches[0].name) + ".";
    }
    else if (positive_matches.length === 2) {
        return nut + generateLink(positive_matches[0].url, positive_matches[0].name) + " and " +
                     generateLink(positive_matches[1].url, positive_matches[1].name) + "."; 
    }
    else {
        var l = positive_matches.length;
        for (var i = 0; i < l-1; i++) {
            nut += generateLink(positive_matches[i].url, positive_matches[i].name) + ", ";
        }
        return nut += "and " + generateLink(positive_matches[l-1].url, positive_matches[l-1].name) + ".";
    }
}

function generateLink(href, content) {
    return "<a href='"+href+"'>"+content+"</a>";
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
