

// $(function() {
//     $('a#somebutton').on('click', function() {
//         $.getJSON('/work',
//             function(data) {
//         //do nothing
//         });
//         return false;
//     });
//     });

var current_messages = [];

window.addEventListener("load",function(){
    var update_loop = setInterval(update_messages,100);
    update_messages();
})
async function update_messages() {

    const response = await fetch('/api/get_real_messages');
    const usable = await response.json();
    
    // let to_append = document.getElementsByTagName("body");
    
    let to_loop = Object.keys(usable).length;
    if (to_loop>current_messages.length){

        for (i = current_messages.length ; i < to_loop; i++) {
            if (current_messages[i]!==usable[i]){
                console.log(usable[i]);
                current_messages.push(usable[i])
            }
          }
          
    }




}


    // let tosend = new XMLHttpRequest();
    // let url = '/';
    // tosend.open('POST',url,true);
    
    // let json_to_send = {"update":""};

    // let new_messages = tosend.send(JSON.stringify(json_to_send));

    // console.log(new_messages.json());

function send_message(){

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

