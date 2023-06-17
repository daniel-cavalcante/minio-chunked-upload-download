# chunked-file-transfer

This is a flask app used to transfer files between server and client. There are only two usecases: the client may upload(download) a file to(from) the server. Each uploaded file is stored in chunks in a MinIO storage server. This process is such a way that the client may _upload very large files without running into any browser memory issues_!

## Uploading files

The flask app serves a home page where the client may select any file in his local machine and upload it to the server. After a file is selected, the user may press the `send` button which will then start the process responsible for uploading the file to the server.

This upload process is done via chunking, that is, the original file is sliced into smaller pieces of equal size, except possibly for the last one, and are indexed accordingly. These smaller files are called "chunks". A loop process begins iterating over these chunks. Each loop does the following: append the chunk and its metadata into a new FormData object, then send it to the server via a XML http request. The process of chunking the bigger one into smaller pieces allows the upload of very large files without the worry of running out of memory.

On the server, each request mentioned above calls a MinIO method responsible for storing the data in buckets. For each file, a new bucket is created. The name of each bucket is a unique identifier and each chunk inside this bucket is named after the original file with the suffix "partXofY" where X is the current chunk index (+1) and Y is the total number of chunks. The total number of chunks is determined on the client side by the formula

total number of chunks = ceiling(file.size/CHUNK_SIZE)

where CHUNK_SIZE is a constant set to 5MB by default and file.size is the size of the file selected by the user.

## Download logic

To be implemented.

## File validation

To be implemented.

## Exceptions

To be implemented.

# Installation

This is a simple flask app. First, install the requirements listed on `server/requirements.txt` using `pip` (or any other similar). Then run `server/app.py`. The app home page will be served on `http://localhost:5000`.
