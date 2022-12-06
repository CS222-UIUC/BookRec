document.getElementById("login").addEventListener("click", () => {
  const loginEmail = document.getElementById("email").value;
  const loginPassword = document.getElementById("password").value;
  signInWithEmailAndPassword(auth, loginEmail, loginPassword)
    .then((userCredential) => {
      // Signed in
      const user = userCredential.user;
      alert("Login Successful");
      window.location.href = "index.html";

      // ...
    })
    .catch((error) => {
      const errorCode = error.code;
      const errorMessage = error.message;
      alert("Error : " + errorMessage);
      // ..
    });
});

document.getElementById("create").addEventListener("click", () => {
  const creatEmail = document.getElementById("email_reg").value;
  const createPassword = document.getElementById("id_reg").value;
  createUserWithEmailAndPassword(auth, createEmail, createPassword)
    .then((userCredential) => {
      // Signed in
      const user = userCredential.user;
      alert("Account Creation Successful");
      window.location.href = "index.html";
    })
    .catch((error) => {
      const errorCode = error.code;
      const errorMessage = error.message;
      window.alert("Error : " + errorMessage);
      // ..
    });
});
const sign_in_btn = document.querySelector("#sign-in-btn");
const sign_up_btn = document.querySelector("#sign-up-btn");
const container = document.querySelector(".container");

sign_up_btn.addEventListener("click", () => {
  container.classList.add("sign-up-mode");
});

sign_in_btn.addEventListener("click", () => {
  container.classList.remove("sign-up-mode");
});

const htmlEl = document.getElementsByTagName("html")[0];

const togglePassword = document.querySelector("#togglePassword");
const password = document.querySelector("#id_password");

togglePassword.addEventListener("click", function (e) {
  const type =
    password.getAttribute("type") === "password" ? "text" : "password";
  password.setAttribute("type", type);
  this.classList.toggle("fa-eye-slash");
});

const toggleReg = document.querySelector("#toggleReg");
const pass = document.querySelector("#id_reg");

toggleReg.addEventListener("click", function (e) {
  const type = pass.getAttribute("type") === "password" ? "text" : "password";
  pass.setAttribute("type", type);
  this.classList.toggle("fa-eye-slash");
});
