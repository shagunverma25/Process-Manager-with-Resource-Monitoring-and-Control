from flask import Flask, request, jsonify, render_template
import psutil
import subprocess
import time
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/processes', methods=['GET'])
def list_processes():
    search = request.args.get('search', '')
    procs = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'status']):
        try:
            info = proc.info
            if search.lower() in info['name'].lower():
                procs.append(info)
        except:
            continue
    return jsonify(procs)

@app.route('/kill', methods=['POST'])
def kill():
    pid = int(request.json['pid'])
    try:
        psutil.Process(pid).terminate()
        return jsonify({'status': 'success', 'message': f'Process {pid} killed'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/suspend', methods=['POST'])
def suspend():
    pid = int(request.json['pid'])
    try:
        psutil.Process(pid).suspend()
        return jsonify({'status': 'success', 'message': f'Process {pid} suspended'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/resume', methods=['POST'])
def resume():
    pid = int(request.json['pid'])
    try:
        psutil.Process(pid).resume()
        return jsonify({'status': 'success', 'message': f'Process {pid} resumed'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})



@app.route('/create', methods=['POST'])
def create_process():
    data = request.get_json()
    cmd = data['cmd']
    try:
        p = subprocess.Popen(cmd.split(), shell=True)
        time.sleep(0.5) 
        parent = psutil.Process(p.pid)
        children = parent.children(recursive=True)
        child_pids = [c.pid for c in children]

        return jsonify({
            'status': 'success',
            'pid': p.pid,
            'child_pids': child_pids
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/details/<int:pid>', methods=['GET'])
def details(pid):
    try:
        p = psutil.Process(pid)
        info = {
            'pid': p.pid,
            'name': p.name(),
            'exe': p.exe(),
            'cwd': p.cwd(),
            'status': p.status(),
            'create_time': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(p.create_time())),
            'cpu_times': str(p.cpu_times()),
            'memory_info': str(p.memory_info()),
            'open_files': str(p.open_files()),
            'connections': str(p.connections()),
            'threads': p.num_threads(),
            'username': p.username(),
            'cmdline': p.cmdline(),
        }
        return jsonify(info)
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
