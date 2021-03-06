

// $(function() {
//     $('a#somebutton').on('click', function() {
//         $.getJSON('/work',
//             function(data) {
//         //do nothing
//         });
//         return false;
//     });
//     });

function send_message(){

    var fillform = document.getElementById("message_sending");
    var message = document.getElementById("message_sent");
    // console.log(message.value);

    message.value = ""; //resetting the input field
    

    fillform.submit();



}

function check_if_enter(e) {

    if(e && e.keyCode == 13) {
       send_message();
    }
 }

