import requests
import CloudFlare

class DDNSUpdater:
    def __init__(self, db):
        self.db = db

    def get_current_ip(self):
        response = requests.get('https://api.ipify.org')
        return response.text

    def update_all_records(self):
        from app import Domain  # Import here to avoid circular import
        domains = self.db.session.query(Domain).all()
        results = []
        for domain in domains:
            results.extend(self.update_domain_records(domain))
        return results

    def update_domain_records(self, domain):
        cf = CloudFlare.CloudFlare(token=domain.token)
        records = cf.zones.dns_records.get(domain.zone_id)
        current_ip = self.get_current_ip()
        results = []
        for record in records:
            if record['type'] in ['A', 'AAAA'] and record.get('auto_update', False):
                if record['content'] != current_ip:
                    cf.zones.dns_records.put(domain.zone_id, record['id'], data={
                        'name': record['name'],
                        'type': record['type'],
                        'content': current_ip
                    })
                    results.append(f"Updated {record['name']} to {current_ip}")
        return results

    def get_dns_records(self, domain):
        cf = CloudFlare.CloudFlare(token=domain.token)
        return cf.zones.dns_records.get(domain.zone_id)

    def update_record(self, domain, record_id, new_ip):
        cf = CloudFlare.CloudFlare(token=domain.token)
        record = cf.zones.dns_records.get(domain.zone_id, record_id)
        record['content'] = new_ip
        cf.zones.dns_records.put(domain.zone_id, record_id, data=record)
        return {"success": True, "message": f"Updated {record['name']} to {new_ip}"}

    def create_record(self, domain, name, record_type, content, auto_update):
        cf = CloudFlare.CloudFlare(token=domain.token)
        data = {
            'name': name,
            'type': record_type,
            'content': content,
            'auto_update': auto_update
        }
        cf.zones.dns_records.post(domain.zone_id, data=data)
        return {"success": True, "message": f"Created new record {name}"}