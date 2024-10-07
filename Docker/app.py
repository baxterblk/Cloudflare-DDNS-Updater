from flask import Flask, render_template, jsonify
from ddns_updater import DDNSUpdater
from apscheduler.schedulers.background import BackgroundScheduler
import os

app = Flask(__name__)
ddns_updater = DDNSUpdater()

def update_job():
    ddns_updater.update_all_records()

scheduler = BackgroundScheduler()
scheduler.add_job(func=update_job, trigger="interval", minutes=5)
scheduler.start()

@app.route('/')
def index():
    return render_template('index.html', subdomains=os.environ['SUBDOMAINS'].split())

@app.route('/update_ip')
def update_ip():
    results = ddns_updater.update_all_records()
    return jsonify(results)

@app.route('/get_current_ip')
def get_current_ip():
    ip = ddns_updater.get_current_ip()
    return jsonify({'ip': ip})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)