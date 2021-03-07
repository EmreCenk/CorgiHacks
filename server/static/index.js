

// $(function() {
//     $('a#somebutton').on('click', function() {
//         $.getJSON('/work',
//             function(data) {
//         //do nothing
//         });
//         return false;
//     });
//     });
async function update_messages() {
    const response = await fetch('/api/get_real_messages');
    const usable = await response.json();
    console.log(usable);
}


    // let tosend = new XMLHttpRequest();
    // let url = '/';
    // tosend.open('POST',url,true);
    
    // let json_to_send = {"update":""};

    // let new_messages = tosend.send(JSON.stringify(json_to_send));

    // console.log(new_messages.json());

function send_message(){
    update_messages();
    console.log("updated message");
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

