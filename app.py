from flask import Flask, request, render_template_string, redirect, session, send_file, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import uuid, io
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfgen import canvas

app = Flask(__name__)
app.config['SECRET_KEY'] = 'GP_HINGOLI_PRO_FINAL_V2'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.String(20), unique=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100))
    phone = db.Column(db.String(15))
    first_year_marks = db.Column(db.String(10))
    second_year_marks = db.Column(db.String(10))
    course_year = db.Column(db.String(20))
    college_name = db.Column(db.String(100), default='GOVERNMENT POLYTECHNIC HINGOLI')
    admission_status = db.Column(db.String(20), default='Pending') # Pending / Accepted / Rejected
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

ADMIN_USER = "admin"
ADMIN_PASS_HASH = generate_password_hash("PALLAVI@8083")

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'admin' not in session:
            return redirect('/admin-login')
        return f(*args, **kwargs)
    return wrap

def gen_id(): return f"GPH2026{str(uuid.uuid4().int)[:4]}"

BASE = """
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;800&display=swap');
body{font-family:'Poppins',sans-serif;background:#f0f2ff}
.navbar{background:linear-gradient(90deg,#1e3a8a,#3b82f6)!important;padding:12px 15px}
.navbar-brand{font-weight:800;font-size:15px}
.card{border:none;border-radius:20px;box-shadow:0 15px 35px rgba(0,0,0,.08)}
.big-square{height:170px;border-radius:22px;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;transition:.3s;cursor:pointer;text-decoration:none;color:white;box-shadow:0 12px 30px rgba(0,0,0,.15)}
.big-square:hover{transform:translateY(-8px) scale(1.02);color:white}
.feature-card{border-radius:16px;padding:18px;text-align:center;background:white;box-shadow:0 8px 20px rgba(0,0,0,.06);transition:.3s;height:100%}
.feature-card:hover{transform:translateY(-5px)}
.trophy{font-size:28px}
@media(max-width:768px){.big-square{height:140px}.display-title{font-size:26px!important}}
</style>
<nav class="navbar navbar-dark">
<div class="container-fluid">
<a class="navbar-brand" href="/"><i class="fas fa-university me-2"></i>GOVT POLYTECHNIC HINGOLI</a>
<button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navMenu"><span class="navbar-toggler-icon"></span></button>
<div class="collapse navbar-collapse mt-3 mt-md-0" id="navMenu">
<div class="d-flex flex-column flex-md-row gap-2 ms-auto align-items-start align-items-md-center">
<a href="/" class="btn btn-light btn-sm rounded-pill fw-bold"><i class="fas fa-home me-1"></i> Home</a>
<a href="/register" class="btn btn-warning btn-sm rounded-pill fw-bold"><i class="fas fa-user-plus me-1"></i> Registration</a>
<a href="/student-login" class="btn btn-light btn-sm rounded-pill fw-bold" style="background:#e0f2fe"><i class="fas fa-user-graduate me-1"></i> Student Login</a>
<a href="/admission-check" class="btn btn-outline-light btn-sm rounded-pill">Admission Form</a>
<a href="/result" class="btn btn-success btn-sm rounded-pill">Result</a>
{% if session.get('admin') %}
<a href="/dashboard" class="btn btn-info btn-sm rounded-pill fw-bold">Dashboard</a>
<a href="/logout" class="btn btn-danger btn-sm rounded-pill fw-bold">Logout</a>
{% else %}
<a href="/admin-login" class="btn btn-outline-light btn-sm rounded-pill"><i class="fas fa-lock me-1"></i> Admin Login</a>
{% endif %}
</div>
</div>
</div>
</nav>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
"""

@app.route('/')
def home():
    total = Student.query.count()
    accepted = Student.query.filter_by(admission_status='Accepted').count()
    pending = Student.query.filter_by(admission_status='Pending').count()
    return render_template_string(BASE + """
    <div class="container py-4">
        <div class="text-center mb-4">
            <span class="badge bg-primary rounded-pill px-3 py-2 mb-2">MSBTE Approved | Est. 1985</span>
            <h1 class="fw-bold display-title" style="font-weight:800;font-size:38px">GOVERNMENT POLYTECHNIC<br><span style="color:#1e3a8a">HINGOLI</span></h1>
            <p class="fst-italic text-muted">"Empowering Futures Through Technical Education" | "शिक्षण हेच खरे धन"</p>
            <p class="small">Total: {{total}} | Accepted: {{accepted}} | Pending: {{pending}}</p>
        </div>

        <div class="row g-3 justify-content-center">
            <div class="col-6 col-md-4"><a href="/student-login" class="big-square" style="background:linear-gradient(135deg,#1e3a8a,#60a5fa)"><i class="fas fa-file-alt fa-3x mb-2"></i><h6 class="fw-bold">Check Admission Form</h6><small>ID Login</small></a></div>
            <div class="col-6 col-md-4"><a href="/register" class="big-square" style="background:linear-gradient(135deg,#f59e0b,#fbbf24);color:#000!important"><i class="fas fa-user-plus fa-3x mb-2"></i><h6 class="fw-bold" style="color:#000">Register Now</h6><small style="color:#000">New Admission</small></a></div>
        </div>

        <div class="mt-5">
            <h5 class="fw-bold text-center mb-3"><i class="fas fa-star text-warning me-2"></i>New Features 2026</h5>
            <div class="row g-3">
                <div class="col-6 col-md-3"><div class="feature-card"><div class="trophy">🏆</div><h6 class="fw-bold mt-2">1st Year Merit</h6><small class="text-muted">Based on 1st Year Marks % - Direct Admission</small></div></div>
                <div class="col-6 col-md-3"><div class="feature-card"><div class="trophy">🎓</div><h6 class="fw-bold mt-2">2nd Year Excellence</h6><small class="text-muted">2nd Year Performance Trophy - Top Scorers</small></div></div>
                <div class="col-6 col-md-3"><div class="feature-card"><div class="trophy">📜</div><h6 class="fw-bold mt-2">Instant PDF</h6><small class="text-muted">After Admin Approval - Official Stamp</small></div></div>
                <div class="col-6 col-md-3"><div class="feature-card"><div class="trophy">✅</div><h6 class="fw-bold mt-2">Admin Verified</h6><small class="text-muted">Accept / Reject by HOD - Secure Flow</small></div></div>
            </div>
        </div>

        <div class="card p-3 mt-4 text-center"><small class="text-muted">© 2026 Government Polytechnic Hingoli | Student Admission Portal | Sir Impress Project 🏆</small></div>
    </div>
    """, total=total, accepted=accepted, pending=pending)

@app.route('/admin-login', methods=['GET','POST'])
def admin_login():
    if request.method == 'POST':
        if request.form['username']==ADMIN_USER and check_password_hash(ADMIN_PASS_HASH, request.form['password']):
            session['admin']=True
            return redirect('/dashboard')
        return render_template_string(BASE + "<div class='container py-5'><div class='alert alert-danger col-md-4 mx-auto text-center'>Wrong ID Password!</div></div>")
    return render_template_string(BASE + """
    <div class="container py-5"><div class="col-md-4 mx-auto"><div class="card p-4">
    <h5 class="fw-bold text-center">Admin Login</h5>
    <form method="POST" class="mt-3"><input name="username" placeholder="Username" class="form-control mb-3 rounded-3" required><input name="password" type="password" placeholder="Password" class="form-control mb-3 rounded-3" required><button class="btn btn-primary w-100 rounded-pill">Login</button></form>
    </div></div></div>
    """)

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect('/')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        s = Student(
            application_id=gen_id(),
            full_name=request.form['full_name'],
            email=request.form['email'],
            phone=request.form['phone'],
            first_year_marks=request.form['first_year'],
            second_year_marks=request.form['second_year'],
            course_year=request.form['course_year'],
            college_name="GOVERNMENT POLYTECHNIC HINGOLI",
            admission_status="Pending"
        )
        db.session.add(s)
        db.session.commit()
        return render_template_string(BASE + """
        <div class="container py-5"><div class="col-md-6 mx-auto"><div class="card p-5 text-center">
        <i class="fas fa-check-circle fa-4x text-success mb-3"></i>
        <h4 class="fw-bold">Registration Submitted!</h4>
        <p>Your Application ID: <b class="text-primary">{{app_id}}</b></p>
        <p class="small text-muted">Form Admin kade gela aahe. Admin Accept kelyavar tumhi Student Login madhun PDF download karu shakal.</p>
        <div class="d-flex gap-2 justify-content-center mt-4">
        <a href="/student-login" class="btn btn-primary rounded-pill">Go to Student Login</a>
        <a href="/" class="btn btn-outline-secondary rounded-pill">Home</a>
        </div>
        </div></div></div>
        """, app_id=s.application_id)
    return render_template_string(BASE + """
    <div class="container py-4"><div class="col-md-6 mx-auto"><div class="card p-4">
    <h5 class="fw-bold text-center">GOVT POLYTECHNIC HINGOLI<br><small class="text-muted">Admission Form - 1st & 2nd Year Based</small></h5>
    <form method="POST" class="mt-4">
    <label class="small fw-bold">Full Name *</label><input name="full_name" class="form-control mb-3 rounded-3" required>
    <label class="small fw-bold">Email</label><input name="email" class="form-control mb-3 rounded-3">
    <label class="small fw-bold">Phone *</label><input name="phone" class="form-control mb-3 rounded-3" required>
    <div class="row g-2"><div class="col-6"><label class="small fw-bold">1st Year Marks (%) *</label><input name="first_year" placeholder="78%" class="form-control mb-3 rounded-3" required></div>
    <div class="col-6"><label class="small fw-bold">2nd Year Marks (%) *</label><input name="second_year" placeholder="82%" class="form-control mb-3 rounded-3" required></div></div>
    <label class="small fw-bold">Admission For *</label><select name="course_year" class="form-select mb-3 rounded-3" required><option value="">-- Select --</option><option>CO-3K</option><option>CO-4K</option><option>CO-5K</option><option>CO-6K</option></select>
    <input value="GOVERNMENT POLYTECHNIC HINGOLI" class="form-control mb-4 rounded-3 bg-light" readonly>
    <button class="btn btn-primary w-100 rounded-pill py-2 fw-bold">Submit For Approval</button>
    </form>
    </div></div></div>
    """)

@app.route('/student-login', methods=['GET','POST'])
def student_login():
    student=None
    msg=None
    app_id = request.args.get('app_id','') or request.form.get('app_id','')
    if app_id:
        student = Student.query.filter_by(application_id=app_id).first()
        if not student:
            msg = "ID Not Found!"
    return render_template_string(BASE + """
    <div class="container py-4"><div class="col-md-6 mx-auto">
    <div class="card p-4"><h5 class="fw-bold text-center"><i class="fas fa-user-graduate me-2"></i>Student Login - Check Status</h5>
    <p class="small text-muted text-center">Enter your Application ID to check admission status</p>
    <form method="POST" class="d-flex gap-2 mt-3"><input name="app_id" value="{{app_id}}" placeholder="e.g. GPH2026..." class="form-control rounded-pill" required><button class="btn btn-primary rounded-pill px-4">Login</button></form>
    {% if msg %}<div class="alert alert-danger mt-3">{{msg}}</div>{% endif %}
    </div>
    {% if student %}
    <div class="card p-4 mt-4">
        <h6 class="fw-bold">{{student.full_name}} - {{student.course_year}}</h6>
        <p class="small">ID: {{student.application_id}} | 1st: {{student.first_year_marks}} | 2nd: {{student.second_year_marks}}</p>
        {% if student.admission_status=='Pending' %}
        <div class="alert alert-warning text-center"><i class="fas fa-clock fa-2x mb-2 d-block"></i><b>Pending</b><br><small>Admin kade approval sathi aahe. Thoda velane check kara.</small></div>
        {% elif student.admission_status=='Rejected' %}
        <div class="alert alert-danger text-center"><i class="fas fa-times-circle fa-2x mb-2 d-block"></i><b>Rejected</b><br><small>Sorry, Tumcha admission reject jhala aahe. Office la sampark kara.</small></div>
        {% elif student.admission_status=='Accepted' %}
        <div class="alert alert-success text-center"><i class="fas fa-check-circle fa-2x mb-2 d-block"></i><b>Accepted! 🎉</b><br><small>Abhinandan! Tumcha admission confirm jhala aahe.</small></div>
        <a href="/download-pdf/{{student.application_id}}" class="btn btn-success w-100 rounded-pill"><i class="fas fa-file-pdf me-2"></i>Download Admission PDF with Stamp</a>
        {% endif %}
    </div>
    {% endif %}
    </div></div>
    """, student=student, app_id=app_id, msg=msg)

# Keep old admission-check redirect to student-login for compatibility
@app.route('/admission-check', methods=['GET','POST'])
def admission_check():
    return redirect('/student-login')

def create_pdf(student):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    c.setStrokeColor(colors.HexColor("#1e3a8a")); c.setLineWidth(3); c.rect(20, 20, width-40, height-40)
    c.setFillColor(colors.HexColor("#1e3a8a")); c.setFont("Helvetica-Bold", 18); c.drawCentredString(width/2, height-60, "GOVERNMENT POLYTECHNIC HINGOLI")
    c.setFillColor(colors.black); c.setFont("Helvetica", 10); c.drawCentredString(width/2, height-78, "MSBTE | Admission Confirmation 2026 | ID: "+student.application_id)
    c.setFont("Helvetica-Bold", 14); c.drawCentredString(width/2, height-105, "ADMISSION ACCEPTED - FINAL CONFIRMATION")
    c.line(20, height-115, width-20, height-115)
    c.setFont("Helvetica", 11)
    y = height-150
    for line in [f"Application ID   : {student.application_id}", f"Name            : {student.full_name}", f"Phone           : {student.phone}", f"1st Year Marks  : {student.first_year_marks} 🏆", f"2nd Year Marks  : {student.second_year_marks} 🏆", f"Admission For   : {student.course_year}", f"College         : {student.college_name}", f"Date            : {student.created_at.strftime('%d-%m-%Y')}", f"Status          : {student.admission_status}"]:
        c.drawString(50, y, line); y-=28
    c.setStrokeColor(colors.HexColor("#16a34a")); c.setFillColor(colors.HexColor("#f0fdf4")); c.rect(width-180, y-5, 135, 75, stroke=1, fill=1)
    c.setFillColor(colors.HexColor("#16a34a")); c.setFont("Helvetica-Bold", 13); c.drawCentredString(width-112, y+40, "G.P. HINGOLI"); c.setFont("Helvetica-Bold", 9); c.drawCentredString(width-112, y+25, "OFFICIAL STAMP"); c.drawCentredString(width-112, y+15, "ACCEPTED"); c.setFont("Helvetica", 7); c.drawCentredString(width-112, y+5, f"{datetime.now().strftime('%d/%m/%Y')}")
    c.setFillColor(colors.HexColor("#1e3a8a")); c.setFont("Helvetica-Oblique", 9); c.drawCentredString(width/2, 60, "Congratulations! Your admission is confirmed by Admin.")
    c.showPage(); c.save(); buffer.seek(0); return buffer

@app.route('/download-pdf/<app_id>')
def download_pdf(app_id):
    s = Student.query.filter_by(application_id=app_id).first_or_404()
    if s.admission_status != 'Accepted':
        return "PDF Only Available After Admin Accepts Admission!", 403
    pdf = create_pdf(s)
    return send_file(pdf, as_attachment=True, download_name=f"GPH_Admission_{s.application_id}.pdf", mimetype='application/pdf')

@app.route('/result')
def result_page():
    return render_template_string(BASE + "<div class='container py-5 text-center'><div class='card p-5 col-md-6 mx-auto'><h5>Result - As per 1st & 2nd Year Merit 🏆</h5><p class='small'>Result will be declared after admission confirmation.</p><a href='/student-login' class='btn btn-primary rounded-pill'>Student Login</a></div></div>")

@app.route('/dashboard')
@login_required
def dashboard():
    students = Student.query.order_by(Student.created_at.desc()).all()
    return render_template_string(BASE + """
    <div class="container-fluid py-4"><h5 class="fw-bold">Admin Dashboard - Accept / Reject</h5>
    <div class="card p-0 overflow-hidden mt-3"><div class="table-responsive"><table class="table small mb-0"><thead class="table-light"><tr><th>ID</th><th>Name</th><th>1st</th><th>2nd</th><th>For</th><th>Status</th><th>Action</th></tr></thead><tbody>
    {% for s in students %}<tr><td><small>{{s.application_id}}</small></td><td>{{s.full_name}}<br><small>{{s.phone}}</small></td><td>{{s.first_year_marks}}</td><td>{{s.second_year_marks}}</td><td>{{s.course_year}}</td><td><span class="badge bg-{% if s.admission_status=='Accepted' %}success{% elif s.admission_status=='Rejected' %}danger{% else %}warning{% endif %}">{{s.admission_status}}</span></td>
    <td><div class="d-flex gap-1"><button onclick="act({{s.id}},'Accepted')" class="btn btn-sm btn-success">Accept</button><button onclick="act({{s.id}},'Rejected')" class="btn btn-sm btn-danger">Reject</button><a href="/download-pdf/{{s.application_id}}" class="btn btn-sm btn-outline-primary"><i class="fas fa-file-pdf"></i></a></div></td></tr>{% endfor %}
    </tbody></table></div></div></div>
    <script>
    function act(id,status){fetch('/api/'+id+'/status',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({status:status})}).then(()=>location.reload())}
    </script>
    """, students=students)

@app.route('/api/<int:id>/status', methods=['POST'])
@login_required
def update_status(id):
    s=Student.query.get_or_404(id)
    d=request.get_json()
    s.admission_status=d['status']
    db.session.commit()
    return jsonify(ok=True)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)