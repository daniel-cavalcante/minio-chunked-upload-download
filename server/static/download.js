const DOWNLOAD_URL = "http://localhost:5000/download";

const getFilesList = () => {
  const bucketList = document.getElementById("bucketList");
  XHR = new XMLHttpRequest();

  // on success, append the name of stored files on <ol> list element
  XHR.addEventListener("load", (event) => {
    const bucket = JSON.parse(event.target.response);

    for (let index = 0; index < bucket.length; index++) {
      // anchor element referencing specific file download url
      a = document.createElement("a");
      a.setAttribute("href", DOWNLOAD_URL + "/" + bucket[index]);
      a.innerHTML = bucket[index];

      // append anchor element to the list as a list item
      item = bucketList
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
