window.addEventListener("DOMContentLoaded", () => {
  const websocket = new WebSocket("ws://localhost:6789/");

  document.querySelector(".minus").addEventListener("click", () => {
    websocket.send(JSON.stringify({ action: "minus" }));
  });

  document.querySelector(".plus").addEventListener("click", () => {
    websocket.send(JSON.stringify({ action: "plus" }));
  });


  document.getElementById('myForm').addEventListener('submit', function (event){
    event.preventDefault();

    const inputValue = document.getElementById('myInput').value;
    websocket.send(JSON.stringify({mgs: inputValue}));
  });

  websocket.onmessage = ({ data }) => {
  const event = JSON.parse(data);
  console.log(event)
  switch (event.type) {
    case "value":
      document.querySelector(".value").textContent = event.value;
      break;
    case "users":
      const users = `${event.count} user${event.count == 1 ? "" : "s"}`;
      document.querySelector(".users").textContent = users;
      break;
    case "message":
      const g = document.createElement('div');
      const message = `Hi ${event.value} \n`;
      g.textContent = message;
      document.querySelector(".userIN").appendChild(g);
      break;
    default:
      console.error("unsupported event", event);
  }
};

});