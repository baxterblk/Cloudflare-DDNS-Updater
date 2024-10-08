from flask import Flask, render_template, jsonify, request, redirect, url_for
from ddns_updater import DDNSUpdater
from apscheduler.schedulers.background import BackgroundScheduler
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///domains.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Domain(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    token = db.Column(db.String(100), nullable=False)
    zone_id = db.Column(db.String(100), nullable=False)

ddns_updater = DDNSUpdater(db)

def update_job():
    ddns_updater.update_all_records()

scheduler = BackgroundScheduler()
scheduler.add_job(func=update_job, trigger="interval", minutes=5)
scheduler.start()

@app.route('/')
def index():
    domains = Domain.query.all()
    return render_template('index.html', domains=domains)

@app.route('/add_domain', methods=['GET', 'POST'])
def add_domain():
    if request.method == 'POST':
        name = request.form['name']
        token = request.form['token']
        zone_id = request.form['zone_id']
        new_domain = Domain(name=name, token=token, zone_id=zone_id)
        db.session.add(new_domain)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_domain.html')

@app.route('/domain/<int:domain_id>')
def view_domain(domain_id):
    domain = Domain.query.get_or_404(domain_id)
    records = ddns_updater.get_dns_records(domain)
    return render_template('domain.html', domain=domain, records=records)

@app.route('/update_record/<int:domain_id>', methods=['POST'])
def update_record(domain_id):
    domain = Domain.query.get_or_404(domain_id)
    record_id = request.form['record_id']
    new_ip = request.form['new_ip']
    result = ddns_updater.update_record(domain, record_id, new_ip)
    return jsonify(result)

@app.route('/create_record/<int:domain_id>', methods=['POST'])
def create_record(domain_id):
    domain = Domain.query.get_or_404(domain_id)
    name = request.form['name']
    record_type = request.form['type']
    content = request.form['content']
    auto_update = request.form.get('auto_update', False)
    result = ddns_updater.create_record(domain, name, record_type, content, auto_update)
    return jsonify(result)

@app.route('/get_current_ip')
def get_current_ip():
    ip = ddns_updater.get_current_ip()
    return jsonify({'ip': ip})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=8080)