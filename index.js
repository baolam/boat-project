const socketio = require("socket.io");
const express = require("express");
const http = require("http");

const app = express();
const server = http.createServer(app);
const io = new socketio.Server(server);

const PORT = process.env.PORT || 3000;

const device = io.of("/device");
const android = io.of("/android");

android.on("connection", (socket) => {
  socket.on("evt", (res) => {
    device.sockets.emit("evt", res);
  });
});

device.on("connection", (socket) => {
  socket.on("record", (data) => {
    android.sockets.emit("record", data);
  });
});

server.listen(PORT, () => {
  console.log(`Server is listening on port ${PORT}`);
});