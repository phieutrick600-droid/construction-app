from flask import Flask, render_template, jsonify, request
from models import init_db
from services import CompanyService, DepartmentService, ProjectService, ItemService

app = Flask(__name__)

# Khởi tạo cơ sở dữ liệu
init_db()

@app.route("/")
def home():
    return render_template("index.html")

# --- API CÔNG TY ---
@app.route("/api/company", methods=["GET", "POST"])
def handle_company():
    if request.method == "POST":
        CompanyService.save(request.json)
        return jsonify({"msg": "OK"})
    return jsonify([c.__dict__ for c in CompanyService.get_all()])

@app.route("/api/company/<id>", methods=["PUT", "DELETE"])
def update_delete_company(id):
    if request.method == "DELETE":
        CompanyService.delete(id)
    else:
        CompanyService.save(request.json)
    return jsonify({"msg": "OK"})

# --- API PHÒNG BAN ---
@app.route("/api/department", methods=["GET", "POST"])
def handle_department():
    if request.method == "POST":
        DepartmentService.save(request.json)
        return jsonify({"msg": "OK"})
    return jsonify([d.__dict__ for d in DepartmentService.get_all()])

@app.route("/api/department/<id>", methods=["PUT", "DELETE"])
def update_delete_department(id):
    if request.method == "DELETE":
        DepartmentService.delete(id)
    else:
        DepartmentService.save(request.json)
    return jsonify({"msg": "OK"})

# --- API CÔNG TRÌNH ---
@app.route("/api/project", methods=["GET", "POST"])
def handle_project():
    if request.method == "POST":
        ProjectService.save(request.json)
        return jsonify({"msg": "OK"})
    return jsonify([p.__dict__ for p in ProjectService.get_all()])

@app.route("/api/project/<id>", methods=["PUT", "DELETE"])
def update_delete_project(id):
    if request.method == "DELETE":
        ProjectService.delete(id)
    else:
        ProjectService.save(request.json)
    return jsonify({"msg": "OK"})

# --- API HẠNG MỤC ---
@app.route("/api/item", methods=["GET", "POST"])
def handle_item():
    if request.method == "POST":
        ItemService.save(request.json)
        return jsonify({"msg": "OK"})
    return jsonify([i.__dict__ for i in ItemService.get_all()])

@app.route("/api/item/<id>", methods=["PUT", "DELETE"])
def update_delete_item(id):
    if request.method == "DELETE":
        ItemService.delete(id)
    else:
        ItemService.save(request.json)
    return jsonify({"msg": "OK"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
from flask import Flask, render_template, request, redirect, url_for, session
from services import CompanyService, DepartmentService, ProjectService, ItemService, UserService

app = Flask(__name__)
app.secret_key = 'lokhai_construction_secret_key' # Khóa bảo mật Session

# Route Trang chủ (Yêu cầu phải đăng nhập)
@app.route('/')
def index():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    # GIỮ NGUYÊN CODE LẤY DỮ LIỆU CŨ CỦA BẠN BÊN DƯỚI
    companies = CompanyService.get_all()
    departments = DepartmentService.get_all()
    projects = ProjectService.get_all()
    items = ItemService.get_all()
    
    return render_template('index.html', 
                           companies=companies, 
                           departments=departments, 
                           projects=projects, 
                           items=items,
                           user_fullname=session.get('user_fullname'))

# BỔ SUNG: Route Đăng Nhập
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = UserService.check_login(username, password)
        if user:
            session['user'] = user.username
            session['user_fullname'] = user.full_name
            return redirect(url_for('index'))
        else:
            return render_template('login.html', msg="Tài khoản hoặc mật khẩu không đúng!", msg_type="danger")
    return render_template('login.html')

# BỔ SUNG: Route Đăng Ký
@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    full_name = request.form.get('full_name')
    
    success, message = UserService.register(username, password, full_name)
    if success:
        return render_template('login.html', msg=message, msg_type="success", active_tab="login")
    else:
        return render_template('login.html', msg=message, msg_type="danger", active_tab="register")

# BỔ SUNG: Route Đăng Xuất
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# --- GIỮ NGUYÊN TOÀN BỘ CÁC ROUTE CỦA BẠN Ở ĐÂY ---
