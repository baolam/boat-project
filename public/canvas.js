
let rows_default = 25, cols_default = 20;
let previ = 0, prevj = 0;
let alpha_rows = 0, alpha_cols = 0;

let socket = io("/android");
let lat_param = document.getElementById("lat-param");
let lng_param = document.getElementById("lng-param");
let width_journey = document.getElementById("width-journey");
let height_journey = document.getElementById("height-journey");
let journey_drawing = document.querySelector('canvas');

function draw_matrix_journey(rows, cols) {
  let context = journey_drawing.getContext('2d');
  let width_canvas = journey_drawing.width;
  let height_canvas = journey_drawing.height;
  let kwidth = width_canvas / rows;
  let kheight = height_canvas / cols;
  let st = 0;
  for (let i = 0; i < rows; i++) {
    context.beginPath();
    context.lineWidth = 0.08;
    context.moveTo(st, 0);
    context.lineTo(st, height_canvas);
    context.strokeStyle = "green";
    context.stroke();
    context.closePath();
    st += kwidth;
  }

  st = 0;
  for (let j = 0; j < cols; j++) {
    context.beginPath();
    context.lineWidth = 0.09;
    context.moveTo(0, st);
    context.lineTo(width_canvas, st);
    context.strokeStyle = "red";
    context.stroke();
    context.closePath();
    st += kheight;
  }
}

function get_journey() {
  let width = prompt("Chiều dài hành trình đi là : ");
  let height = prompt("Chiều rộng hành trình đi là : ");
  
  width = parseInt(width);
  height = parseInt(height);
  
  width_journey.innerHTML = '<i class="color-param">Chiều dài : </i><strong>' + String(width) +'m</strong>';
  height_journey.innerHTML = '<i class="color-param">Chiều rộng : </i><strong>' + String(height) +'m</strong>';
  
  // Vẽ ma trận
  draw_matrix_journey(rows_default, cols_default);

  // Tính toán tỉ lệ phóng
  alpha_rows = width / journey_drawing.width;
  alpha_cols = height / journey_drawing.height;

  prevj = journey_drawing.height;
}

function draw_point(i, j) {
  let context = journey_drawing.getContext('2d');
  context.beginPath();
  context.arc(i, j, 1, 0, 2 * Math.PI, false);
  context.lineWidth = 1;
  context.strokeStyle = "blue";
  context.stroke();
  context.closePath();
}

function draw_line(i, j) {
  let context = journey_drawing.getContext('2d');
  context.beginPath();
  context.moveTo(previ, prevj);
  context.lineTo(i, j);
  context.strokeStyle = "blue";
  context.lineWidth = 0.5;
  context.stroke();
  context.closePath();
}

socket.on("gps", (data) => {
  let lat = data.lat, lng = data.lng;

  // Đưa ra giao diện
  lat_param.innerHTML = '<div class="color-param">Vĩ độ : </div><strong>' + lat + '</strong>';
  lng_param.innerHTML = '<div class="color-param">Kinh độ : </div><strong>' + lng + '</strong>';

  let i = data.i, j = data.j;
  let pixeli = parseInt(i / alpha_rows);
  let pixelj = parseInt(j / alpha_cols);

  // Vẽ điểm ra ma trận
  draw_point(pixeli, pixelj);
  draw_line(pixeli, pixelj);
  previ = pixeli;
  prevj = pixelj;
});
