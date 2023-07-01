# MinIO Chunked File Upload / Download

This is a flask app used to transfer files between server and client. There are
only two usecases: the client may **upload a file** to the server or **download
files** from it. Each uploaded file is stored in chunks into a MinIO storage
server. This process is implemented in such a way that the client may _upload
very large files without the risk of running into any browser memory issues_!

## Uploading a file

The flask app serves a home page where the client may select any file in his
local machine and upload it to the server. After a file is selected, the user
may press the `send` button which will then start the process responsible for
uploading the file to the server.

This upload process is done via chunking, that is, the original file is sliced
into smaller pieces of equal size, except possibly for the last one, and are
indexed accordingly. These smaller files are called "chunks". A loop process
begins iterating over these chunks. Each loop does the following: append the
chunk and its metadata into a new FormData object, then send it to the server
via a XML http request. The process of chunking the bigger one into smaller
pieces allows the upload of very large files without the worry of running out
of memory.

On the server, each request mentioned above calls a MinIO method responsible
for storing the data in buckets. For each file, a new bucket is created. The
name of each bucket is a unique identifier and each chunk inside this bucket is
named after the original file with the suffix "partXofY" where X is the current
chunk index (+1) and Y is the total number of chunks. The total number of
chunks is determined on the client side by the formula

```
chunksTotal = Math.ceil(file.size / CHUNK_SIZE)
```

where `CHUNK_SIZE` is a constant set to 5MB by default and `file.size` is the
size of the file selected, set on the input element "change" event.

## Downloading files

When the user access and loads the home page, the page script automatically
loads a list of buckets. Each bucket consists of a folder containing chunks of
a previously uploaded file.

The list of buckets are all anchors with an identifier string. When clicked,
the browser downloads the associated file. Each bucket contains a file split in
many chunks, so the server streams each chunk one after the other directly to
the user. By streaming the chunks this way, the browser already saves
everything in one single file.

## File validation

To be implemented.

## Handling of exceptions

To be implemented.

# Installation

This is a simple flask app. Change to server directory, create a virtual
environment, activate it then install the requirements. Lastly, run the flask
server.

```
cd server
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
flask --app source run
```

The app home page will be served on `http://localhost:5000`.
