

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
    var message = document.getElementById("message");
    // console.log(message.value);

    console.log(fillform.textContent);
    

    fillform.submit();



}


function alpa(){
    console.log("connected to this file");
}