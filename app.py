from flask import Flask, render_template, redirect, url_for
import subprocess

app = Flask(__name__)

def run_command(command):
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result.stdout.strip(), result.stderr.strip()

def get_apps():
    apps, _ = run_command('dokku apps:list')
    apps = apps.splitlines()[1:]  # Пропускаем заголовок "My Apps"
    return [app.strip() for app in apps]

def get_containers(app_name):
    containers, _ = run_command(f'docker ps -a --filter name={app_name} --format "{{{{.ID}}}} {{{{.Image}}}} {{{{.Status}}}} {{{{.Names}}}}"')
    return [container.split() for container in containers.splitlines()]

@app.route('/')
def index():
    apps = get_apps()
    app_containers = {app: get_containers(app) for app in apps}
    return render_template('index.html', app_containers=app_containers)

@app.route('/restart/<app_name>')
def restart_app(app_name):
    _, error = run_command(f'dokku ps:restart {app_name}')
    if error:
        return f"Error restarting app {app_name}: {error}", 500
    return redirect(url_for('index'))

@app.route('/logs/<app_name>')
def view_logs(app_name):
    logs, _ = run_command(f'dokku logs {app_name}')
    return render_template('logs.html', app_name=app_name, logs=logs)

@app.route('/stop_container/<container_id>')
def stop_container(container_id):
    _, error = run_command(f'docker stop {container_id}')
    if error:
        return f"Error stopping container {container_id}: {error}", 500
    return redirect(url_for('index'))

@app.route('/remove_container/<container_id>')
def remove_container(container_id):
    _, error = run_command(f'docker rm {container_id}')
    if error:
        return f"Error removing container {container_id}: {error}", 500
    return redirect(url_for('index'))

@app.route('/start_container/<container_id>')
def start_container(container_id):
    _, error = run_command(f'docker start {container_id}')
    if error:
        return f"Error starting container {container_id}: {error}", 500
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
