// Game board and status
const boardElement = document.getElementById("game-board");
const statusText = document.getElementById("status");
const CGI_URL = "http://localhost:8000/cgi-bin/main.py";

// --- Function to Start the Game ---
function startGame() {
  fetch("cgi-bin/main.py", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ action: "start" }) // Send action "start"
  })
    .then(response => response.json()) // Convert response to JSON
    .then(data => {
      updateBoard(data.board);  // Update board UI
      statusText.textContent = `Next Move: ${data.next_player}`;
    })
    .catch(error => console.error("Error starting game:", error));
}

// --- Function to Make a Move ---
function makeMove(index) {
  fetch("cgi-bin/main.py", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ action: "move", pos: index + 1 }) // Convert to 1-based index
  })
    .then(response => response.json())
    .then(data => {
      if (data.error) {
        alert(data.error); // Show error if invalid move
      } else {
        updateBoard(data.board);
        statusText.textContent = `Next Move: ${data.next_player}`;
      }
    })
    .catch(error => console.error("Error making move:", error));
}

// --- Function to Update Board UI ---
function updateBoard(board) {
  boardElement.innerHTML = "";
  board.forEach((cell, index) => {
    let cellElement = document.createElement("div");
    cellElement.classList.add("cell");
    cellElement.textContent = cell === 0 ? "" : (cell === -1 ? "X" : "O");
    cellElement.onclick = () => makeMove(index);
    boardElement.appendChild(cellElement);
  });
}

// --- Run Start Game on Page Load ---
startGame();
