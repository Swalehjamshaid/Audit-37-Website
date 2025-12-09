import requests
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from .forms import RegisterForm, AuditForm
from .models import Website, Audit, AuditMetric

def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        messages.error(request, 'Invalid credentials')
    return render(request, 'login.html')

@login_required
def dashboard(request):
    if request.method == 'POST':
        form = AuditForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            audit = run_website_audit(request.user, url)
            return redirect('report', audit.id)
    else:
        form = AuditForm()

    audits = Audit.objects.filter(user=request.user).order_by('-timestamp')[:10]
    return render(request, 'dashboard.html', {'form': form, 'audits': audits})

@login_required
def report(request, audit_id):
    audit = Audit.objects.get(id=audit_id, user=request.user)
    return render(request, 'report.html', {'audit': audit})

@login_required
def download_pdf(request, audit_id):
    audit = Audit.objects.get(id=audit_id)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="FFTech_WebAudit_Report_{audit_id}.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("FF Tech WebAudit - Official Report", styles['Title']))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"Website: <b>{audit.website}</b>", styles['Normal']))
    elements.append(Paragraph(f"Date: {audit.timestamp.strftime('%Y-%m-%d %H:%M')}", styles['Normal']))
    elements.append(Spacer(1, 20))

    data = [["Metric", "Score (0-100)", "Status"]]
    for m in audit.metrics.all():
        status = "Good" if m.value >= 80 else "Warning" if m.value >= 60 else "Critical"
        data.append([m.name, f"{m.value:.1f}", status])

    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a5276')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f0f8ff')),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(table)
    doc.build(elements)
    return response

def run_website_audit(user, url):
    website, _ = Website.objects.get_or_create(url=url)
    audit = Audit.objects.create(website=website, user=user)

    # Simulate 37 real-world metrics (expand later with Lighthouse API)
    sample_metrics = [
        ("Page Load Speed", 88.5, "LCP under 2.5s"),
        ("Mobile Responsiveness", 95.0, "Fully responsive"),
        ("Accessibility (WCAG 2.1)", 82.0, "Good contrast"),
        ("SEO Score", 91.0, "Meta tags present"),
        ("HTTPS Security", 100.0, "Valid SSL"),
        ("Core Web Vitals", 89.0, "All passing"),
        ("Server Response Time", 76.0, "TTFB 340ms"),
    ]

    for name, value, detail in sample_metrics:
        AuditMetric.objects.create(audit=audit, name=name, value=value, details=detail)

    return audit
