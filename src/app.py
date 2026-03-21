import os
import json
import threading
import time
import contextlib
import io
from datetime import datetime
from flask import Flask, render_template, request, jsonify, session
from agent import EasyMate

app = Flask(__name__)
app.secret_key = 'EasyMate'

def load_config():
    with open("./config.json", 'r', encoding='utf-8') as f:
        return json.load(f)

def save_config(config):
    with open("./config.json", 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

chat_agent = None
chat_agent_lock = threading.Lock()

tasks_agent = None

def init_agents():
    global chat_agent, tasks_agent
    config = load_config()
    pre_memory = ""
    try:
        with open("memory.txt", "r", encoding="utf-8") as f:
            pre_memory = f.read()
    except:
        pass
    settings = config.get("settings", "")
    full_settings = f"{settings}\n\n{pre_memory}" if pre_memory else settings
    chat_agent = EasyMate(
        key=config["api_key"],
        url=config["base_url"],
        model=config["model"],
        settings=full_settings
    )
    tasks_agent = EasyMate(
        key=config["api_key"],
        url=config["base_url"],
        model=config["model"],
        settings=full_settings
    )

def run_tasks():
    if not hasattr(run_tasks, "_executed"):
        run_tasks._executed = set()
    if not hasattr(run_tasks, "_last_date"):
        run_tasks._last_date = None

    while True:
        if os.path.exists("./tasks.json"):
            try:
                with open("./tasks.json", 'r', encoding='utf-8') as f:
                    tasks = json.load(f)
            except:
                pass
            else:
                now = datetime.now()
                current_time = now.strftime("%H:%M")
                today = now.strftime("%Y-%m-%d")
                if today != run_tasks._last_date:
                    run_tasks._executed.clear()
                    run_tasks._last_date = today

                for task_id, (content, time_str) in tasks.items():
                    if time_str == current_time and task_id not in run_tasks._executed:
                        print(f"执行任务 {task_id}: {content}")
                        try:
                            tasks_agent.input(content)
                        except Exception as e:
                            print(f"任务执行失败: {e}")
                        run_tasks._executed.add(task_id)
        time.sleep(10)

run_tasks_thread = threading.Thread(target=run_tasks, daemon=True)
run_tasks_thread.start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '').strip()
    if not user_message:
        return jsonify({'error': '消息不能为空'}), 400

    logs_capture = io.StringIO()
    with contextlib.redirect_stdout(logs_capture):
        with chat_agent_lock:
            try:
                answer = chat_agent.input(user_message)
            except Exception as e:
                answer = f"处理消息时出错: {e}"
    logs = logs_capture.getvalue()

    return jsonify({'answer': answer, 'logs': logs})

@app.route('/config', methods=['GET'])
def get_config():
    try:
        with open("./config.json", 'r', encoding='utf-8') as f:
            config = json.load(f)
        return jsonify(config)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/config', methods=['POST'])
def update_config():
    data = request.get_json()
    required = ['api_key', 'base_url', 'model']
    for field in required:
        if field not in data:
            return jsonify({'error': f'缺少字段: {field}'}), 400
    try:
        with open("./config.json", 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        init_agents()
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    init_agents()
    app.run(host='127.0.0.1', port=5000, debug=True, use_reloader=False)