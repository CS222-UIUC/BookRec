//https://www.superhi.com/video/smooth-movements-with-javascript
window.rInterval = function (callback, delay) {
  var dateNow = Date.now,
    requestAnimation = window.requestAnimationFrame,
    start = dateNow(),
    stop,
    intervalFunc = function () {
      dateNow() - start < delay || ((start += delay), callback());
      stop || requestAnimation(intervalFunc);
    };
  requestAnimation(intervalFunc);
  return {
    clear: function () {
      stop = 1;
    },
  };
};
const root = document.querySelector(":root");
const ball = document.querySelector(".light");
const darkness = getComputedStyle(document.documentElement).getPropertyValue(
  "--darkness"
);
const torchRadius = getComputedStyle(document.documentElement).getPropertyValue(
  "--torch-radius"
);
const poistionY = getComputedStyle(document.documentElement).getPropertyValue(
  "--position-y"
);
const positionX = getComputedStyle(document.documentElement).getPropertyValue(
  "--position-x"
);

let mouseX = 0;
let mouseY = 0;

let ballX = 0;
let ballY = 0;

let speed = 0.1;

let style = document.createElement("style");
style.id = "torch-style";
const fillStyle = (top, left) =>
  (style.innerHTML = `.container::after {background-image: radial-gradient(circle closest-side at ${left}px ${top}px, #FFF 0%, #FFF, ${darkness} var(--torch-radius), ${darkness}, ${darkness}); animation: none !important}`);

function animate() {
  let distX = mouseX - ballX;
  let distY = mouseY - ballY;

  ballX = ballX + distX * speed;
  ballY = ballY + distY * speed;

  fillStyle(ballY, ballX);
  document.body.appendChild(style);

  requestAnimationFrame(animate);
}
animate();

document.addEventListener("mousemove", function (event) {
  mouseX = event.pageX;
  mouseY = event.pageY;
});
document.addEventListener("mouseleave", () => {
  document.getElementById("torch-style").remove();
  root.style.setProperty("--torch-radius", torchRadius + "px");
});

document.addEventListener("click", () => {
  const radius = String(torchRadius * 1.2).replace("px", "");
  console.log(radius);
  root.style.setProperty("--torch-radius", radius * 2 + "px");
});

// Animate the spotlight randomly when user isn't interacting
// or when the user lands on the page

/*document.addEventListener(
  "mouseleave",
  rInterval(() => {
    fillStyle(
     // Math.floor(Math.random() * window.innerHeight),
     // Math.floor(Math.random() * window.innerWidth)
      100,100
    );
    document.body.appendChild(style);
  }, 3000)
);
*/
