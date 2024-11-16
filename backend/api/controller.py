from flask import Flask, request, jsonify, Response, render_template_string
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_basicauth import BasicAuth
from dotenv import load_dotenv
import logging
import os
import csv
from service import query_rag, log_interaction

load_dotenv()

app = Flask(__name__)
limiter = Limiter(get_remote_address, app=app, default_limits=["1000 per day", "100 per hour"])
logging.basicConfig(level=logging.INFO)

app.config['BASIC_AUTH_USERNAME'] = os.getenv("USERNAME")
app.config['BASIC_AUTH_PASSWORD'] = os.getenv("PASSWORD")
basic_auth = BasicAuth(app)

LOG_FILE = "query_log.csv"

@app.route('/api/query', methods=['POST'])
@limiter.limit("1 per second")
@basic_auth.required
def handle_query():
    data = request.json
    query_text = data.get("query_text")
    chat_history = data.get("chat_history")
    client = request.remote_addr

    if not query_text:
        return jsonify({"error": "No query_text provided"}), 400

    def generate_stream():
        response_stream = query_rag(query_text, chat_history, client)
        for chunk in response_stream:
            yield chunk

    return Response(generate_stream(), content_type='text/plain; charset=utf-8')

@app.route('/api/log', methods=['GET'])
@limiter.limit("1 per second")
@basic_auth.required
def display_log():
    log_entries = []
    with open(LOG_FILE, "r") as log_file:
        reader = csv.reader(log_file)
        for row in reader:
            log_entries.append(row)

    table_html = """
    <table border="1">
        <tr>
            <th>time</th>
            <th>query</th>
            <th>response</th>
            <th>parameters</th>
            <th>client</th>
        </tr>
        {% for entry in log_entries %}
        <tr>
            <td>{{ entry[0] }}</td>
            <td>{{ entry[1] }}</td>
            <td>{{ entry[2] }}</td>
            <td>{{ entry[3] }}</td>
            <td>{{ entry[4] }}</td>
        </tr>
        {% endfor %}
    </table>
    """
    return render_template_string(table_html, log_entries=log_entries)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)