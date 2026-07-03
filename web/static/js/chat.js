const socket = io();
let selectedUser = null;
let chatHistory = {};
let securityHistory = {};

document.querySelector(
".chat-status"
).innerHTML =
"Waiting for user...";

socket.on(
    "online_users",
    (users)=>{

        const box =
            document.getElementById(
                "onlineUsers"
            );

        box.innerHTML="";

        users.forEach(user=>{

            if(user===CURRENT_USER){

                box.innerHTML +=
                `
                <div class="user myself">

                    👤 ${user} (You)

                </div>
                `;

            }

            else{

                box.innerHTML +=
                `
                <div
                    class="user"
                    onclick="selectUser('${user}')"
                >

                    🟢 ${user}

                </div>
                `;

            }

        });

    }
);

socket.on("connect",()=>{

    console.log("CONNECTED");

});

socket.on("connect_error",(err)=>{

    console.log(err);

});

socket.on(
    "receive_message",
    (data) => {

        let partner;

        if (data.sender === CURRENT_USER) {

            partner = data.receiver;

        }
        else {

            partner = data.sender;

        }

        if (!chatHistory[partner]) {

            chatHistory[partner] = [];

        }

        chatHistory[partner].push(data);
        securityHistory[partner] = data;

        if (selectedUser === partner) {

            renderChat(partner);
            
            const box =
            document.getElementById(
            "messages"
            );

            box.scrollTop =
            box.scrollHeight;

            renderSecurity(partner);

        }

        updateSecurityPanel(data);

    }
);

socket.on(
    "attack_mode",
    (mode) => {

        updateAttackModeDisplay(mode);

    }
);

socket.on(
    "security_alert",
    (data) => {

        document.getElementById(
            "securityStatus"
        ).innerHTML =
            data.message;

    }
);

function updateSecurityPanel(data){

    document.getElementById(
        "plainText"
    ).innerHTML =
        data.plaintext;

    document.getElementById(
        "cipherText"
    ).innerHTML =
        data.ciphertext;

    document.getElementById(
        "nonce"
    ).innerHTML =
        data.nonce;

    document.getElementById(
        "signature"
    ).innerHTML =
        data.signature;

    document.getElementById(
        "sessionId"
    ).innerHTML =
        data.session_id;

    document.getElementById(
        "sequence"
    ).innerHTML =
        data.sequence_number;

    document.getElementById(
        "messageId"
    ).innerHTML =
        data.message_id;

    document.getElementById(
        "timestamp"
    ).innerHTML =
        data.timestamp || "N/A";

    document.getElementById(
        "securityStatus"
    ).innerHTML =
        data.security_status || "N/A";

}

function updateAttackModeDisplay(mode){

    const labels = [];

    if(mode.ciphertext){
        labels.push("Ciphertext ON");
    }

    if(mode.sequence){
        labels.push("Sequence ON");
    }

    if(mode.wrong_key){
        labels.push("Wrong Key ON");
    }

    if(mode.fake_sender){
        labels.push("Fake Sender ON");
    }

    const text =
        labels.length > 0
        ? labels.join(" | ")
        : "All attacks OFF";

    document.getElementById(
        "attackMode"
    ).innerHTML = text;

    document.getElementById(
        "btnCipher"
    ).classList.toggle(
        "active",
        mode.ciphertext
    );

    document.getElementById(
        "btnSequence"
    ).classList.toggle(
        "active",
        mode.sequence
    );

    document.getElementById(
        "btnWrongKey"
    ).classList.toggle(
        "active",
        mode.wrong_key
    );

    document.getElementById(
        "btnFakeSender"
    ).classList.toggle(
        "active",
        mode.fake_sender
    );

}

function sendMessage(){

    if(selectedUser==null){

        alert("Please select a user.");

        return;

    }

    const input =
        document.getElementById(
            "messageInput"
        );

    if(
        input.value.trim()==""
    ){

        return;

    }

    socket.emit(
        "send_message",
        {

            receiver:
                selectedUser,

            message:
                input.value

        }
    );

    input.value="";

    input.focus();

    setTimeout(()=>{

        const box =
        document.getElementById(
        "messages"
        );

        box.scrollTop =
        box.scrollHeight;

    },100);

}

function selectUser(username){

    selectedUser = username;

    document.querySelector(
    ".chat-status"
    ).innerHTML =
    "🟢 Secure Connection";

    document.getElementById(
        "selectedUser"
    ).innerHTML =
        username;

    renderChat(username);
    renderSecurity(username);

}

function renderChat(username){

    const messages =
        document.getElementById("messages");

    messages.innerHTML = "";

    if(!chatHistory[username]){
        return;
    }

    chatHistory[username].forEach(data=>{

        const side =
            data.sender===CURRENT_USER
            ? "sent"
            : "received";

        const time =
            data.timestamp
            ? new Date(data.timestamp).toLocaleTimeString([],{
                hour:"2-digit",
                minute:"2-digit"
            })
            : "";

        messages.innerHTML +=
        `
        <div class="message ${side}">

            <b>${data.sender}</b>

            ${data.plaintext}

            <div class="message-time">

                ${time}

            </div>

        </div>
        `;

    });

    messages.scrollTop =
        messages.scrollHeight;

}

function renderSecurity(username){

    if(!securityHistory[username]){

        return;

    }

    updateSecurityPanel(
        securityHistory[username]
    );

}

function disableAttacks(){

    socket.emit(
        "disable_attacks"
    );

}

function toggleCipherAttack(){

    socket.emit(
        "toggle_ciphertext_attack"
    );

}

function toggleSequenceAttack(){

    socket.emit(
        "toggle_sequence_attack"
    );

}

function toggleWrongKey(){

    socket.emit(
        "toggle_wrong_key_attack"
    );

}

function toggleFakeSender(){

    socket.emit(
        "toggle_fake_sender"
    );

}

function replayAttack(){

    socket.emit(
        "replay_attack"
    );

}

document
.getElementById("messageInput")
.addEventListener(
    "keydown",
    function(e){

        if(e.key==="Enter"){

            e.preventDefault();

            sendMessage();

        }

    }
);