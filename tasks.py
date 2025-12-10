# tasks.py
import json
from weasyprint import HTML, CSS
from flask import current_app, render_template
from flask_mail import Message
from app import db, mail, AuditService, User, AuditReport


def send_scheduled_report(user_id, url, recipient_email):
    with current_app.app_context():
        audit_results = AuditService.run_audit(url)
        user = User.query.get(user_id)
        if not user:
            return False

        new_report = AuditReport(
            website_url=url,
            performance_score=audit_results['performance_score'],
            security_score=audit_results['security_score'],
            accessibility_score=audit_results['accessibility_score'],
            metrics_json=json.dumps(audit_results['metrics']),
            user_id=user.id
        )
        db.session.add(new_report)
        db.session.commit()

        metrics = json.loads(new_report.metrics_json)
        categorized_metrics = {}
        for cat, keys in AuditService.METRICS.items():
            categorized_metrics[cat] = {k: metrics[k] for k in keys}

        html_content = render_template('report_pdf.html', report=new_report, metrics=categorized_metrics)
        pdf_file = HTML(string=html_content).write_pdf(stylesheets=[CSS(string='body { font-family: sans-serif; }')])

        msg = Message(f"Daily Audit Report: {url}", recipients=[recipient_email])
        msg.attach("report.pdf", "application/pdf", pdf_file)
        mail.send(msg)
        return True
