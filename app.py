import re
from flask import Flask, render_template ,request ,jsonify, send_from_directory
import os, uuid

app = Flask(__name__)
UPLOAD_FOLDER = 'media'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
paraphraph = f"<p><strong><u>${'='*221}$</u></strong></p>"
data_file = 'data.txt'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Generate a unique filename
    filename = f"{uuid.uuid4().hex}{os.path.splitext(file.filename)[1]}"
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    # Save the file
    file.save(file_path)

    # Return the URL for accessing the uploaded file
    return jsonify({'url': f'/media/{filename}'}), 201

@app.route('/media/<path:filename>', methods=['GET'])
def send_media(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/datasend', methods=['POST'])
def data_send():
    global paraphraph
    data = request.form['data']
    empty_content_regex = r'^(<p><\/p>|<p>\s*<\/p>|\s*)+$'
    if re.match(empty_content_regex, data):
        paraphraph = ''
    try:
        with open(data_file, 'a') as f:
            f.write(data + '\n' + paraphraph)
        return 'Data received', 200
    except IOError as e:
        print(f"Error writing to file: {e}")
        return 'Server error', 500

@app.route('/clearcontent',methods=('POST',))
def clear_content():
    if request.form['command'] == 'clearcontent':
        try:
            with open(data_file,'w') as f:
                f.write("")
                return 200
        except IOError as e:
            return 'Server error', 500

@app.route('/getdata', methods=['GET'])
def get_data():
    try:
        with open(data_file, 'r') as f:
            content = f.readlines()
            return ''.join(content), 200
    except IOError as e:
        print(f"Error reading from file: {e}")
        return 'Server error', 500

if __name__ == '__main__':
    if not os.path.exists(data_file):
        with open(data_file, 'w'):
            pass
    app.run(port=5000, debug=True)