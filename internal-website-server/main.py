from flask import Flask, send_file, abort
from google.cloud import storage
import os

app = Flask(__name__)

# Configure your GCS bucket name
GCS_BUCKET_NAME = os.environ.get('GCS_BUCKET_NAME', 'sentiment-dashboard-static') # Replace with your bucket name

# Initialize Google Cloud Storage client
storage_client = storage.Client()
bucket = storage_client.bucket(GCS_BUCKET_NAME)

# Route for the root URL, serving index.html
@app.route('/')
def serve_index():
    return serve_from_gcs('index.html')

# Route to serve other static files (HTML, CSS, JS, images)
@app.route('/<path:filename>')
def serve_static(filename):
    return serve_from_gcs(filename)

def serve_from_gcs(filename):
    # Prevent directory traversal attacks
    if '..' in filename or filename.startswith('/'):
        abort(404)

    blob = bucket.blob(filename)
    if not blob.exists():
        # If a file is not found, try adding .html for cleaner URLs (optional)
        if not '.' in filename: # If no file extension
            blob = bucket.blob(f'{filename}.html')
            if blob.exists():
                return send_file(blob.download_as_bytes(), mimetype='text/html')
        abort(404)

    # Determine mimetype from filename extension
    # You might need a more robust mimetypes library for production
    if filename.endswith('.html'):
        mimetype = 'text/html'
    elif filename.endswith('.css'):
        mimetype = 'text/css'
    elif filename.endswith('.js'):
        mimetype = 'application/javascript'
    elif filename.endswith('.png'):
        mimetype = 'image/png'
    elif filename.endswith('.jpg') or filename.endswith('.jpeg'):
        mimetype = 'image/jpeg'
    else:
        mimetype = 'application/octet-stream' # Default for unknown types

    return send_file(blob.download_as_bytes(), mimetype=mimetype)


if __name__ == '__main__':
    # Port 8080 is the default for Cloud Run
    app.run(debug=True, host='0.0.0.0', port=8080)