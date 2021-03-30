$(document).ready(function () {
    $('#input_show_variants').change(function () {
        if (!this.checked) {
            $('#variants_title').hide();
            $('#variants_responses_area').hide();
        } else {
            $('#variants_title').show();
            $('#variants_responses_area').show();
        }
    });
});


$("#btn_send_message").click(function(e) {

    e.preventDefault();

    // disable input form
    $('#input_send_message').attr('disabled', 'disabled');
    // disable button send
    $('#btn_send_message').attr('disabled', 'disabled');

    // set status typing
    $("#text_status_typing").html("typing ...");

    var dialog_history_array = [];
    var count_rep_user = 0;
    var count_rep_bot = 0;

    for (var i = 1; i <= 10; i++) {
        if ($("#text_rep_user_" +  i).length) {
            dialog_history_array.push({'speaker': '0', 'text': $("#text_rep_user_" +  i)[0].text});
            count_rep_user = count_rep_user + 1;
        };
        if ($("#text_rep_bot_" +  i).length) {
            dialog_history_array.push({'speaker': '1', 'text': $("#text_rep_bot_" +  i)[0].text});
            count_rep_bot = count_rep_bot + 1;
        };
    }

    if ((count_rep_bot + count_rep_user) > 8) {
        alert("Количество реплик должно быть меньше 10! Начните заново.");
        //
        $("#text_status_typing").html("");
        // enable input form
        $('#input_send_message').removeAttr('disabled');
        // enable button send
        $('#btn_send_message').removeAttr('disabled');
        return;
    };

    var message = $("#input_send_message").val();
    var length = $("#input_length").val();
    var max_length = $("#input_max_length").val();
    var no_repeat_ngram_size = $("#input_no_repeat_ngram_size").val();
    var top_k = $("#input_top_k").val();
    var top_p = $("#input_top_p").val();
    var temperature = $("#input_temperature").val();
    var num_return = $("#input_num_return").val();

    if(document.getElementById('input_use_gpu').checked) {
        var use_gpu = true;
    } else {
        var use_gpu = false;
    }

    dialog_history_array.push({'speaker': '0', 'text': message})

    // send you message
    var user_date = new Date().toLocaleTimeString().replace(/(.*)\D\d+/, '$1');
    $("#messages_area").append(
        "<div id=\"div_rep_user_" + (count_rep_user + 1) +"\" class=\"chat-message-right pb-4\">\n" +
            "<div>\n" +
                "<img src=\"static/files/images/image_user.jpg\"\n" +
                     "class=\"rounded-circle mr-0 ml-1\" alt=\"Del\" width=\"40\"\n" +
                     "height=\"40\">" +
                "<div class=\"text-muted small text-nowrap mt-2\" style=\"text-align:center;\">"+user_date+"</div>" +
            "</div>" +
            "<div style='background-color:#DDEED8;border-radius:.90rem!important;' class=\"flex-shrink-1 rounded py-2 px-3 mr-3\">" +
                "<div class=\"font-weight-bold mb-1\">Вы</div>" +
                "<a id=\"text_rep_user_" + (count_rep_user + 1) +"\" class=\"msg_rep\">"+message+"</a>\n" +
            "</div>" +
        "</div>");

        // scroll
        $(document).ready(function() {
            $('#messages_area').animate({
                scrollTop: $('#messages_area').get(0).scrollHeight
            }, 1000);
        });

    // scroll
    // $("#page_messages_area").scrollTop(+300);;

    $.ajax({
        type: "POST",
        url: "dialog",
        data: JSON.stringify({
            "dialog_history_array": dialog_history_array,
            "params": {
                "length": length,
                "max_length": max_length,
                "no_repeat_ngram_size": no_repeat_ngram_size,
                "top_k": top_k,
                "top_p": top_p,
                "temperature": temperature,
                "num_return": num_return,
                "do_sample": true,
                "use_gpu": use_gpu
                },
        }),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function(data) {

            // alert(JSON.stringify(data));

            if (data.success == false) {
                var bot_date = new Date().toLocaleTimeString().replace(/(.*)\D\d+/, '$1');
                var message = data.msg;
                $("#div_rep_user_" + (count_rep_user + 1)).remove();
                // enable input form
                $('#input_send_message').removeAttr('disabled');
                // enable button send
                $('#btn_send_message').removeAttr('disabled');
                // set status typing
                $("#text_status_typing").html("");
                alert(JSON.stringify(message));
                return;
            };

            // send bot message
            var bot_date = new Date().toLocaleTimeString().replace(/(.*)\D\d+/, '$1');
            var message = data.response;
            $("#messages_area").append(
                "<div class=\"chat-message-left pb-4\">\n" +
                    "<div>\n" +
                        "<img src=\"static/files/images/image_bot.jpg\"\n" +
                             "class=\"rounded-circle mr-1 ml-1\" alt=\"Sonny\" width=\"40\"\n" +
                             "height=\"40\">" +
                        "<div class=\"text-muted small text-nowrap mt-2\" style=\"text-align:center;\">"+bot_date+"</div>" +
                    "</div>" +
                    "<div style='background-color:#EBEDF0;border-radius:.90rem!important;' class=\"flex-shrink-1 rounded py-2 px-3 ml-3\">" +
                        "<div class=\"font-weight-bold mb-1\">GPT</div>" +
                        "<a id=\"text_rep_bot_" + (count_rep_user + 1) +"\" class=\"msg_rep\">"+message+"</a>\n" +
                    "</div>" +
                "</div>");

            // enable input form
            $('#input_send_message').removeAttr('disabled');
            // enable button send
            $('#btn_send_message').removeAttr('disabled');
            // reset input form
            $("#input_send_message").val("");
            // set cursor
            $("#input_send_message").focus();
            // set status typing
            $("#text_status_typing").html("");

            // scroll
            $(document).ready(function() {
                $('#messages_area').animate({
                    scrollTop: $('#messages_area').get(0).scrollHeight
                }, 1000);
            });

            // scroll
            // $( "#page_messages_area" ).scrollTop(+300);;

            // clear previous data variants
            $("#variants_responses_area").empty();
            var variantsLength = data.variants_responses.length;
            for (var i = 0; i < variantsLength; i++) {
                $("#variants_responses_area").append(
                    "<div class=\"alert alert-success pt-0 pb-0 pr-1 pl-1 mb-1 pointer variants\" onClick=\"setHTML('" + "text_rep_bot_" + (count_rep_user + 1) + "','" + data.variants_responses[i].replace(/"/g, '&#34') + "'" + ");\">" +
                        "<a id=\"variant_" + (i+1) + "\"\" data-toggle=\"tooltip\" data-placement=\"right\" title=\"\">" + data.variants_responses[i] + "</a>" +
                    "</div>"
                );
            }

        }
    });

});


// function for set text by element
function setHTML(elementId, text){
    document.getElementById(elementId).innerHTML = text;
};


// click button for send message via Enter
$("#input_send_message").keyup(function(event) {
    if (event.keyCode === 13) {
        $("#btn_send_message").click();
    }
});


// clear dialog history by click button
$("#btn_clear_dialog").click(function() {
    $("#messages_area").empty();
    $("#variants_responses_area").empty();
    $("#input_send_message").val("");
    $("#input_send_message").focus();
});


// edit message block
$("#messages_area").on('dblclick', 'a', function() {
    oriVal = $(this).text();
    $(this).text("");
    $('<input type="text" class="msg_edit" value="' + oriVal + '">').appendTo(this).focus();
});

$("#messages_area").on('focusout', 'a > input', function() {
    var $this = $(this);
    $this.parent().text($this.val());
    $this.remove();
});