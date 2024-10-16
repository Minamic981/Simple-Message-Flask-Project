from flask import Flask, render_template as t, request as r
import os

app = Flask(__name__)
paraphraph = "<p><strong><u>$=============================================================================================================================================================================================================================$</u></strong></p>"
data_file = 'data.txt'

@app.route('/')
def index():
    return t('index.html')

@app.route('/datasend', methods=['POST'])
def data_send():
    data = r.form['data']
    try:
        with open(data_file, 'a') as f:
            f.write(data + '\n' + paraphraph)
        return 'Data received', 200
    except IOError as e:
        print(f"Error writing to file: {e}")
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