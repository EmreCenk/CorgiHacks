

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
var thing = document.getElementById("formessages");
window.addEventListener("load",function(){
    var update_loop = setInterval(update_messages,100);
    update_messages();
})
async function update_messages() {

    const response = await fetch('/api/get_real_messages');
    const usable = await response.json();
    let thing = document.getElementById("formessages");

    // let to_append = document.getElementsByTagName("body");
    
    let to_loop = Object.keys(usable).length;
    if (to_loop>current_messages.length){

        for (i = current_messages.length ; i < to_loop; i++) {
            if (current_messages[i]!==usable[i]){
                console.log(usable[i]);
                let newthing=document.createElement("div");
                newthing.setAttribute("class","message_container");
                newthing.setAttribute("value",usable[i]);
                newthing.innerHTML = usable[i];
                thing.appendChild(newthing);
                // thing.appendChild("<div class='container'><p> "+usable[i] + " </p><span class='time-right'>11:00</span> </div>")
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
    // console.log("updated message");
    var message = document.getElementById("message_sent");
    console.log(message.value);
    if( message.value.length>=2){
        //there is nothing to send, so we return 
        let tosend = new XMLHttpRequest();
        let url = '/';
        tosend.open('POST',url,true);
        let json_to_send = {"username":message.value};
    
        tosend.send(JSON.stringify(json_to_send));
    
    
    
        message.value = ""; //resetting the input field 
        message.focus();
        let objDiv = document.getElementById("formessages");
        objDiv.scrollTop = objDiv.scrollHeight;
    }
    
    

}

function check_if_enter(e) {

    if(e && e.keyCode == 13) {
       send_message();
    }
 }

