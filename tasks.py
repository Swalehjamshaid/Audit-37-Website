# tasks.py (FINAL, ORGANIZED, RAILWAY-READY CODE)

import json
from weasyprint import HTML, CSS
from flask import render_template
from flask_mail import Message
# All imports are absolute:
from app import app, db, mail, AuditService, User, AuditReport


def send_scheduled_report(user_id, url, recipient_email):
    # Use the imported 'app' instance for application context
    with app.app_context(): 
        audit_results = AuditService.run_audit(url)
        user = User.query.get(user_id)
        
        if not user:
            print(f"Task failed: User ID {user_id} not found.")
            return False

        # --- Database Insertion ---
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

        # --- PDF Generation ---
        metrics = json.loads(new_report.metrics_json)
        categorized_metrics = {}
        for cat, keys in AuditService.METRICS.items():
            categorized_metrics[cat] = {k: metrics.get(k) for k in keys} 

        def generate_pdf_content(report, metrics):
            return render_template('report_pdf.html', report=report, metrics=metrics)

        html_content = generate_pdf_content(new_report, categorized_metrics)
        
        pdf_file = HTML(string=html_content).write_pdf(
            stylesheets=[CSS(string='@page { size: A4; margin: 1.5cm } body { font-family: sans-serif; }')]
        )

        # --- Email Sending ---
        msg = Message(f"Daily Audit Report: {url}", recipients=[recipient_email])
        msg.attach(f"report_{new_report.id}.pdf", "application/pdf", pdf_file)
        mail.send(msg)
        
        print(f"Report ID {new_report.id} sent to {recipient_email}")
        return True
