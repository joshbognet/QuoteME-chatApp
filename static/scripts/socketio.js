document.addEventListener('DOMContentLoaded', () => {

    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
    
    const username = document.querySelector('#get-username').innerHTML;
    
    let room = "Lounge";
    joinRoom('Lounge')


     //send message
     document.querySelector('#send_message').onclick = () => {
        socket.emit('message', {'msg': document.querySelector('#user_message').value,
               'username': username, 'room':room});
        //clear input Area
        document.querySelector('#user_message').value = '';
    }


    socket.on('message', data =>{
       if(data.msg) {
            const p = document.createElement('p');
            const br = document.createElement('br');
            const hr = document.createElement('hr')
            const span_username = document.createElement('span');
            const span_timestamp = document.createElement('span');

            if (data.username == username){
                p.setAttribute("class", "my-msg");
                span_username.setAttribute("class", "my-username");
                span_username.innerText= data.username;
                
                span_timestamp.setAttribute("class", "timestamp");
                span_timestamp.innerText = data.time_stamp; 
                p.innerHTML += span_username.outerHTML + br.outerHTML + data.msg + br.outerHTML +hr.outerHTML+ span_timestamp.outerHTML
                document.querySelector('#display-message-section').append(p);

            } 
 
            else if (typeof data.username !== 'undefined') {
                p.setAttribute("class", "others-msg");

                // Username
                span_username.setAttribute("class", "other-username");
                span_username.innerText = data.username;

                // Timestamp
                span_timestamp.setAttribute("class", "timestamp");
                span_timestamp.innerText = data.time_stamp;

                // HTML to append
                p.innerHTML += span_username.outerHTML + br.outerHTML + data.msg + br.outerHTML + hr.outerHTML + span_timestamp.outerHTML;

                //Append
                document.querySelector('#display-message-section').append(p);
            
            }else{
            printSysMsg(data.msg);
            }
            
        }
        
        scrollDownChatWindow();
    });
    

    // Scroll chat window down
    function scrollDownChatWindow() {
        const chatWindow = document.querySelector("#display-message-section");
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }

   


     // Select a room
    document.querySelectorAll('.select-room').forEach(p => {
        p.onclick = () => {
            let newRoom = p.innerHTML;
            // Check if user already in the room
            if (newRoom === room) {
                msg = `You are already in ${room} room.`;
                printSysMsg(msg);
            } else {
                leaveRoom(room);
                joinRoom(newRoom);
                room = newRoom;
            }
        };
    });


    // Trigger 'join' event
    function joinRoom(room) {

        // Join room
        socket.emit('join', {'username': username, 'room': room});

    
        // Clear message area
        document.querySelector('#display-message-section').innerHTML = '';

    }



     // Trigger 'leave' event if user was previously on a room
    function leaveRoom(room) {
        socket.emit('leave', {'username': username, 'room': room});

        // document.querySelectorAll('.select-room').forEach(p => {
        //     p.style.color = "black";
            
        // });
    }

    
    // Print system messages
    function printSysMsg(msg) {
        const p = document.createElement('p');
        p.setAttribute("class", "system-msg");
        p.innerHTML = msg;
        document.querySelector('#display-message-section').append(p);
    //     scrollDownChatWindow()

        // Autofocus on text box
        document.querySelector("#user_message").focus();
    }
   
   






    // // Retrieve username
    // const username = document.querySelector('#get-username').innerHTML;

    // // Set default room
    // let room = "Lounge"
    // joinRoom("Lounge");

    // // Send messages
    // document.querySelector('#send_message').onclick = () => {
    //     socket.emit('incoming-msg', {'msg': document.querySelector('#user_message').value,
    //         'username': username, 'room': room});

    //     document.querySelector('#user_message').value = '';
    // };

    // // Display all incoming messages
    // socket.on('message', data => {

    //     // Display current message
    //     if (data.msg) {
    //         const p = document.createElement('p');
    //         const span_username = document.createElement('span');
    //         const span_timestamp = document.createElement('span');
    //         const br = document.createElement('br')
    //         // Display user's own message
    //         if (data.username == username) {
    //                 p.setAttribute("class", "my-msg");

    //                 // Username
    //                 span_username.setAttribute("class", "my-username");
    //                 span_username.innerText = data.username;

    //                 // Timestamp
    //                 span_timestamp.setAttribute("class", "timestamp");
    //                 span_timestamp.innerText = data.time_stamp;

    //                 // HTML to append
    //                 p.innerHTML += span_username.outerHTML + br.outerHTML + data.msg + br.outerHTML + span_timestamp.outerHTML

    //                 //Append
    //                 document.querySelector('#display-message-section').append(p);
    //         }
    //         // Display other users' messages
    //         else if (typeof data.username !== 'undefined') {
    //             p.setAttribute("class", "others-msg");

    //             // Username
    //             span_username.setAttribute("class", "other-username");
    //             span_username.innerText = data.username;

    //             // Timestamp
    //             span_timestamp.setAttribute("class", "timestamp");
    //             span_timestamp.innerText = data.time_stamp;

    //             // HTML to append
    //             p.innerHTML += span_username.outerHTML + br.outerHTML + data.msg + br.outerHTML + span_timestamp.outerHTML;

    //             //Append
    //             document.querySelector('#display-message-section').append(p);
    //         }
    //         // Display system message
    //         else {
    //             printSysMsg(data.msg);
    //         }


    //     }
    //     scrollDownChatWindow();
    // });

   
    // Logout from chat
    document.querySelector("#logout-btn").onclick = () => {
        leaveRoom(room);
    };

   

    
    // // Scroll chat window down
    // function scrollDownChatWindow() {
    //     const chatWindow = document.querySelector("#display-message-section");
    //     chatWindow.scrollTop = chatWindow.scrollHeight;
    // }

    
});

