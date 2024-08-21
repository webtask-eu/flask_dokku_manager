from flask import Flask, request
import subprocess

app = Flask(__name__)

@app.route('/deploy', methods=['POST'])
def deploy():
    if request.method == 'POST':
        subprocess.call(['/root/flask_dokku_manager/deploy.sh'])
        return 'Deployed!', 200
    else:
        return 'Invalid request', 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)
