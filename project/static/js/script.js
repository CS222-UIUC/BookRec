

function readlistone() {
    const listone = document.querySelector(".booklistone");
    const booklistone = document.querySelector("#listoneupload").files[0];
    const reader = new FileReader();
    reader.addEventListener("load", () => {
        // this will then display a text file
        listone.innerText = "File Uploaded!";
      }, false);
    reader.onerror = err => console.log(err);
    reader.readAsText(booklistone);
};

function readlisttwo() {
  const listtwo = document.querySelector(".booklisttwo");
  const booklisttwo = document.querySelector("#listtwoupload").files[0];
  const reader = new FileReader();
  reader.addEventListener("load", () => {
    listtwo.innerText = "File Uploaded!";
  }, false);
  reader.onerror = err => console.log(err);
  reader.readAsText(booklisttwo);
}