const socketio = require("socket.io");
const express = require("express");
const http = require("http");

const app = express();
const server = http.createServer(app);
const io = new socketio.Server(server, {
  allowEIO3 : true
});

const PORT = process.env.PORT || 3000;

const device = io.of("/device");
const android = io.of("/android");
const ai = io.of("/ai");

android.on("connection", (socket) => {
  console.log("Co ket noi");
  socket.on("evt", (res) => {
    device.emit("evt", res);
  });

  socket.on("speed", (res) => {
    device.emit("speed", res.speed);
  });

  socket.on("direction", (res) => {
    device.emit("direction", res == 't' ? true : false);
  });
});

device.on("connection", (socket) => {
  socket.on("record", (data) => {
    console.log(data);
    android.emit("record", data);
  });

  socket.on("gps", (data) => {
    console.log(data);
    android.emit("gps", data);
  });
});

ai.on("connection", (socket) => {
  socket.on("resp", (inf) => {
    device.emit("res_rec", inf);
  });
});

app.use(express.urlencoded({ extended : false, limit : "5mb" }));
app.use(express.json({ limit : "5mb" }));
app.get("/", (req, res) => {
  ai.emit("handle", req.body.base64);
  res.status(200).send("OK");
});

server.listen(PORT, () => {
  console.log(`Server is listening on port ${PORT}`);
});