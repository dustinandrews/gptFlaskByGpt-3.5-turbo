import openai
from flask import Flask, redirect, render_template, request, url_for
import csv
import base64
import sys
import traceback
from lib import DictArrayManager
import importlib

app = Flask(__name__)
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
openai.api_key = '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'

messages = DictArrayManager()
messages.add("system", "You are a helpful assistant")

@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        if  'reset' in request.form:
            reset()
        elif len(request.form["query"]) > 0:
            return process_request(request)
    return render_template("index.html", anchor='query', messages=messages.array, tokens=messages.tokens, n=len(messages.array))

def reset():
    # Reload openai module
    importlib.reload(openai)
    messages.clear()
    messages.add("system", "You are a helpful assistant")
    return redirect(url_for('index', _anchor='query'))

def process_request(request):
    model = request.form["model"]
    messages.add("user", request.form["query"])
    messages.truncate(1024)
    try:
        response = openai.ChatCompletion.create(model=model, messages=messages.array)
        repsonse_message = response.choices[0].message["content"]
        messages.add("assistant", repsonse_message)
    except Exception as e:
        print("handled exception")
        exc_type, exc_value, exc_traceback = sys.exc_info()
        lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        messages.add("system", "ERROR:\n" + (''.join('!! ' + line for line in lines)))
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
        # Trying to decode the string using base64 decoding
        decoded_string = base64.b64decode(s).decode("utf-8")
        # Checking if the decoded string matches the original string
        if messages.encode(decoded_string) == s:
            return True
        else:
            return False
    except:
        return False