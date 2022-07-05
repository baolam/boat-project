const socketio = require("socket.io");
const express = require("express");
const http = require("http");
const path = require("path");

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
  socket.on("evt", (res) => {
    device.emit("evt", res);
  });

  socket.on("speed", (res) => {
    res = JSON.parse(res);
    device.emit("speed", res.speed);
  });

  socket.on("direction", (res) => {
    device.emit("direction", res == 't' ? true : false);
  });

  socket.on("journey", (res) => {
    device.emit("journey", res);
  });
  
  socket.on("stop", () => {
    device.emit("stop");
  });
});

device.on("connection", (socket) => {
  socket.on("record", (data) => {
    android.emit("record", data);
  });

  socket.on("gps", (data) => {
    android.emit("gps", data);
  });

  socket.on("is_full", () => {
    android.emit("is_full");
  });

  socket.on("notification", (res) => {
    android.emit("notification", res);
  });
});

ai.on("connection", (socket) => {
  socket.on("resp", (inf) => {
    device.emit("res_rec", inf);
  });
});

app.use(express.urlencoded({ extended : false, limit : "5mb" }));
app.use(express.json({ limit : "5mb" }));
app.use(express.static(path.join(__dirname, "public")));
app.get("/", (req, res) => {
  ai.emit("handle", req.body.base64);
  res.status(200).send("OK");
});

app.get("/control", (__, res) => {
  res.sendFile(path.join(__dirname, "public", "layout", "index.html"));
});

server.listen(PORT, () => {
  console.log(`Server is listening on port ${PORT}`);
});