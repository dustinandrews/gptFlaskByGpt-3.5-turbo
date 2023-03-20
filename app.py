import openai
from flask import Flask, redirect, render_template, request, url_for
import base64
import sys
import traceback
from lib import DictArrayManager
import importlib
import os
import csv

app = Flask(__name__)
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    with open('openai.api_key.txt', 'r') as f:
        OPENAI_API_KEY = f.readline().strip()
openai.api_key = OPENAI_API_KEY

# Set the number of past tokens to send with the current query
# rounds to the nearest whole message
history_max_tokens = 1024

messages = DictArrayManager()

@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        if 'reset' in request.form:
            reset()
        elif len(request.form["query"]) > 0:
            return process_request(request)
    return render_template("index.html", anchor='query', messages=messages.array, tokens=messages.tokens, n=len(messages.array))

def reset():
    # Reload openai module
    importlib.reload(openai)
    openai.api_key = OPENAI_API_KEY
    messages.clear()
    messages.add("system", "You are a helpful assistant")

def process_request(request):
    model = request.form["model"]
    messages.add("user", request.form["query"])
    messages.truncate(history_max_tokens)
    try:
        response = openai.ChatCompletion.create(model=model, messages=messages.array)
        response_message = response.choices[0].message["content"]
        messages.add("assistant", response_message)
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        stack = ''.join('!! ' + line for line in lines)
        messages.add("system", "ERROR:\n" + stack)
        print("handled exception\n", stack)
    return redirect(url_for('index', _anchor='query'))

@app.route('/log')
def view_log():
    log_lines = []
    with open('log.csv', newline='') as log_file:
        csv_reader = csv.DictReader(log_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in csv_reader:
            for i in row:
                if is_base64(row[i]):
                    row[i] = base64.b64decode(row[i]).decode("utf-8")
            log_lines.append(row)
    return render_template('log.html', log_lines=log_lines)

def is_base64(s):
    try:
        decoded_string = base64.b64decode(s).decode("utf-8")
        if messages.encode(decoded_string) == s:
            return True
        else:
            return False
    except:
        return False

reset()