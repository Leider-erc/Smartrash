function abrirCaneca(caneca) {
    fetch(`/send/${caneca}`)
        .then(res => res.json())
        .then(data => console.log(data));
}

let socket = new WebSocket("wss://" + location.host + "/ws");

socket.onmessage = function(event) {
    console.log("Mensaje del ESP32:", event.data);
};
