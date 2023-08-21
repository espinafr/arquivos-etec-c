// client-side js
// run by the browser each time your view template is loaded

// by default, you've got jQuery,
// add other scripts at the bottom of index.html

const fileInput = document.getElementById("fileInput");
const uploadButton = document.getElementById("uploadButton");
const fileList = document.getElementById("fileList");

uploadButton.addEventListener("click", () => {
    const files = fileInput.files;
    
    for (const file of files) {
        const listItem = document.createElement("li");
        listItem.textContent = file.name;
        
        const downloadLink = document.createElement("a");
        downloadLink.textContent = "Download";
        downloadLink.href = URL.createObjectURL(file);
        downloadLink.download = file.name;
        
        listItem.appendChild(downloadLink);
        fileList.appendChild(listItem);
    }
    
    fileInput.value = null;
});
