from flask import Flask, render_template, redirect, url_for, Response, stream_with_context
import subprocess

app = Flask(__name__)

def run_command(command):
    """Запуск команды в системе и возврат результата"""
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout.strip()

def stream_command(command):
    """Генерация логов в реальном времени"""
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    for line in process.stdout:
        yield line
    process.wait()

@app.route('/')
def index():
    apps_status = get_apps_status()
    return render_template('index.html', apps_status=apps_status)

@app.route('/restart/<app_name>')
def restart(app_name):
    return render_template('restart.html', app_name=app_name)

@app.route('/restart_log/<app_name>')
def restart_log(app_name):
    command = f"dokku ps:restart {app_name}"
    return Response(stream_with_context(stream_command(command)), mimetype='text/plain')

@app.route('/stop/<app_name>')
def stop(app_name):
    run_command(f"dokku ps:stop {app_name}")
    return redirect(url_for('index'))

@app.route('/logs/<app_name>')
def logs(app_name):
    logs_output = run_command(f"dokku logs {app_name}")
    return f"<pre>{logs_output}</pre>"

def get_apps_status():
    """Получить список приложений и их статус"""
    output = run_command("dokku apps:list")
    apps = output.strip().split('\n')[1:]  # Пропускаем заголовок
    apps_status = []
    for app in apps:
        deployed = run_command(f"dokku ps:report {app} --deployed")
        processes = run_command(f"dokku ps:report {app} --processes")
        running = run_command(f"dokku ps:report {app} --running")
        apps_status.append((app, deployed, processes, running))
    return apps_status

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
