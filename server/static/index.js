

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

    var message = document.getElementById("message_sent");
    // console.log(message.value);
    if( message.value.length<1){
        //there is nothing to send, so we return 
        return None
    }
    
    let tosend = new XMLHttpRequest();
    let url = '/';
    tosend.open('POST',url,true);
    let json_to_send = {"username":message.value};

    tosend.send(JSON.stringify(json_to_send));



    message.value = ""; //resetting the input field 

}

function check_if_enter(e) {

    if(e && e.keyCode == 13) {
       send_message();
    }
 }

