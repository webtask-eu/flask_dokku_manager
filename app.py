from flask import Flask, render_template, redirect, url_for
import subprocess

app = Flask(__name__)

def run_command(command):
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result.stdout.strip(), result.stderr.strip()

@app.route('/')
def index():
    containers, _ = run_command('docker ps -a --format "{{.ID}} {{.Image}} {{.Status}} {{.Names}}"')
    containers = [container.split() for container in containers.splitlines()]
    return render_template('index.html', containers=containers)

@app.route('/stop/<container_id>')
def stop_container(container_id):
    _, error = run_command(f'docker stop {container_id}')
    if error:
        return f"Error stopping container {container_id}: {error}", 500
    return redirect(url_for('index'))

@app.route('/remove/<container_id>')
def remove_container(container_id):
    _, error = run_command(f'docker rm {container_id}')
    if error:
        return f"Error removing container {container_id}: {error}", 500
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
