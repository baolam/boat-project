let motor_speed_param = document.getElementById("param");
let input_param = document.querySelector("input");
let go_to_home = document.getElementById("go-to-home");
let left = document.getElementById("left");
let right = document.getElementById("right");
let stop_ = document.getElementById("stop");
let list_notification = document.getElementById("list-notification");

function create_chart(ntu, tds) {
  Highcharts.chart("ntu-tds-container", {
    chart : {
      type : "column"
    },
    title : {
      text : "Biểu đồ giá trị nồng độ chất rắn hòa tan và độ đục của nước"
    },
    yAxis : {
      min : 0,
      title : {
        text : "Giá trị"
      }
    },
    series : [
      {
        name : "ntu",
        data : [ntu]
      },
      {
        name : "tds",
        data : [tds]
      }
    ]
  });
}

socket.on("record", (data) => {
  input_param.value = data.motor_speed;
  motor_speed_param.innerHTML = '<div class="color-param">Tốc độ : </div><strong>' + String(input_param.value) + '</strong>';
  create_chart(data.turbidity, data.dissolved_solid);
});

socket.on("is_full", () => {
  list_notification.innerHTML = '<li>Rác đã đầy</li>';
});

let temp = true;
socket.on("notification", (notify) => {
  let l = document.createElement('li');
  l.className = "item-notification";

  if (notify.standard != undefined) {
    l.innerHTML = "Chưa đọc được GPS";

    if (notify.standard)
      l.innerHTML = "Đọc GPS thành công";
    
    list_notification.appendChild(l);
  } else if (notify.can !== undefined) {
    l.innerHTML = notify.can;
    
    list_notification.appendChild(l);
  } else {
    let left = notify.left_right;
    let deg = notify.deg;
    
    if (! left)
      l.innerHTML = `Rẽ trái góc ${Math.floor(deg)} độ`;
    else 
      l.innerHTML = `Rẽ phải góc ${Math.floor(deg)} độ`;
  }
});

// Sau 5s refresh 1 lần
setInterval(() => {
  list_notification.innerHTML = "";
}, 5000);

input_param.addEventListener("change", (ev) => {
  input_param.value = ev.target.value;
  motor_speed_param.innerHTML = '<div class="color-param">Tốc độ : </div><strong>' + String(ev.target.value) + '</strong>';

  // Phát sự kiện đến thuyền
  socket.emit("speed", JSON.stringify({
    speed : ev.target.value
  }));
});

create_chart(0, 0);
get_journey();

// Phát sự kiện đi về nhà
go_to_home.addEventListener("click", () => {
  socket.emit("go-to-home"); 
});

left.addEventListener("click", () => {
  socket.emit("direction", "f");
});

right.addEventListener("click", () => {
  socket.emit("direction", "t");
});

stop_.addEventListener("click", () => {
  socket.emit("stop");
});