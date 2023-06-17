// constants and the global variables
const CHUNK_SIZE = 5 * 1024 * 1024;
const BASE_URL = "http://localhost:5000";
let file;

// code that handles user selecting a file
const handleChange = (event) => {
  file = event.target.files[0];
};

const input = document.getElementById("fileInput");
input.addEventListener("change", handleChange);

// code that handles user clicking on 'send' button
const handleClick = () => {
  // set total number of chunks
  const chunksTotal = Math.ceil(file.size / CHUNK_SIZE);

  // set file identifier to be used by the server to handle exceptions
  const fileId = crypto.randomUUID();

  for (let chunkIndex = 0; chunkIndex < chunksTotal; chunkIndex++) {
    // each loop picks a chunk of file to be sent to the server
    let chunk;
    const isLastChunk = chunkIndex + 1 == chunksTotal;
    if (isLastChunk) {
      // the last chunk is simply what is left of the file
      chunk = file.slice(chunkIndex * CHUNK_SIZE);
    } else {
      chunk = file.slice(
        chunkIndex * CHUNK_SIZE,
        (chunkIndex + 1) * CHUNK_SIZE
      );
    }

    const chunkMetaData = {
      chunkIndex: chunkIndex,
      chunksTotal: chunksTotal,
      originalFileId: fileId,
    };

    const chunkFormData = getFormData(chunk, chunkMetaData);

    sendData(chunkFormData);
  }
};

const button = document.getElementById("sendButton");
button.addEventListener("click", handleClick);

const getFormData = (chunk, metaData) => {
  const chunkForm = new FormData();

  // appending metaData attributes, but notice most of these is unused
  for (const [key, value] of Object.entries(metaData)) {
    chunkForm.append(key, value);
  }
  // append the slice blob with a unique name indicating its part
  const chunkName =
    file.name + ".part" + ++metaData.chunkIndex + "of" + metaData.chunksTotal;
  chunkForm.append("chunk", chunk, chunkName);

  return chunkForm;
};

const sendData = (formData) => {
  const XHR = new XMLHttpRequest();

  // code that listens for success or exceptions and handles it
  XHR.addEventListener("load", (event) => {
    console.info(event.target.status, event);
  });

  XHR.addEventListener("error", (event) => {
    console.error(event.target.status, event);
  });

  // sets up the request then sends the form
  // HTTP headers are set automatically
  XHR.open("POST", BASE_URL + "/upload");
  XHR.send(formData);
};
