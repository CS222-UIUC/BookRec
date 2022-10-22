

function readlistone() {
    const listone = document.querySelector(".booklistone");
    const booklistone = document.querySelector("#listoneupload").files[0];
    const reader = new FileReader();
    reader.addEventListener("load", () => {
        // this will then display a text file
        listone.innerText = reader.result;
      }, false);
    reader.onerror = err => console.log(err);
    reader.readAsText(booklistone);
};