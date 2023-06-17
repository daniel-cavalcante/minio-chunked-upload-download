const DOWNLOAD_URL = "http://localhost:5000/download";

const getFilesList = () => {
  const storedFilesList = document.getElementById("storedFilesList");
  XHR = new XMLHttpRequest();

  // on success, append the name of stored files on <ol> list element
  XHR.addEventListener("load", (event) => {
    const storedFiles = JSON.parse(event.target.response);

    for (let index = 0; index < storedFiles.length; index++) {
      // anchor element referencing specific file download url
      a = document.createElement("a");
      a.setAttribute("href", DOWNLOAD_URL + "/" + storedFiles[index]);
      linkText = document.createTextNode(storedFiles[index]);
      a.appendChild(linkText);

      // append anchor element to the list as a list item
      item = storedFilesList
        .appendChild(document.createElement("li"))
        .appendChild(a);
    }
  });

  // on failure, log event
  XHR.addEventListener("error", (event) => {
    console.error(event);
  });

  XHR.open("GET", DOWNLOAD_URL);
  XHR.send();
};

window.onload = getFilesList;
