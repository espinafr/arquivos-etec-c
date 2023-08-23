const fileInput = document.getElementById('fileInput');
const fileChosen = document.getElementById('file-chosen');

fileInput.addEventListener('change', function(){
    fileChosen.textContent = this.files[0].name
})