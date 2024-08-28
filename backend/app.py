from posix import abort
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import subprocess
import os

app = Flask(__name__)
CORS(app, origins=["https://port3002-workspaces-ws-mz8z4.us10.trial.applicationstudio.cloud.sap"], supports_credentials=True)

# Ensure the data and outputs directories exist
os.makedirs('data', exist_ok=True)
os.makedirs('outputs', exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify(message="No file part"), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify(message="No selected file"), 400
    if file:
        # Save the uploaded file to the data folder
        file_path = os.path.join('data', file.filename)
        file.save(file_path)
        
        # Define the output file path
        output_file_path = os.path.join('outputs', 'processed_' + file.filename)
        
        # Execute the ravalia.py script and pass necessary arguments
        result = subprocess.run(['python3', 'ravalia.py', file_path, output_file_path], capture_output=True, text=True)
        
        # Check if the script ran successfully
        if result.returncode != 0:
            return jsonify(message="Error processing file", error=result.stderr), 500
        
        # Return the URL to download the processed file
        return jsonify(message="File processed successfully", file_url=f"/outputs/processed_{file.filename}"), 200

@app.route('/outputs/<filename>', methods=['GET'])
def download_file(filename):
    file_path_download = os.path.join('outputs', filename)
    if os.path.exists(file_path_download):
        return send_from_directory('outputs', filename, as_attachment=True)
    else:
        abort(404, description="Resource not found")

if __name__ == '__main__':
    app.run(port=5000)
