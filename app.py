from flask import Flask, render_template, jsonify, request, redirect, url_for, session
from models import init_db
from services import CompanyService, DepartmentService, ProjectService, ItemService, UserService

app = Flask(__name__)
app.secret_key = 'lokhai_construction_secret_key'

# Khởi tạo cơ sở dữ liệu khi app chạy
init_db()


# --- TRANG CHỦ / DANG NHAP / DANG KY / DANG XUAT ---
@app.route("/")
def index():
    companies = CompanyService.get_all()
    departments = DepartmentService.get_all()
    projects = ProjectService.get_all()
    items = ItemService.get_all()

    # Lấy họ tên người dùng đã lưu trong Session khi đăng nhập
    user_fullname = session.get('user_fullname', 'Khách')

    return render_template(
        'index.html',
        companies=companies,
        departments=departments,
        projects=projects,
        items=items,
        user_fullname=user_fullname
    )


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Trường hợp 1: Nhận JSON từ Firebase / Javascript
        if request.is_json:
            data = request.get_json(silent=True) or {}
            email = data.get('email')
            if email:
                # Tìm thông tin user trong CSDL local để lấy đúng Họ và tên lúc đăng ký
                user = UserService.check_login(email, None)
                session['user'] = email
                if user and getattr(user, 'full_name', None):
                    session['user_fullname'] = user.full_name
                else:
                    session['user_fullname'] = email.split('@')[0]
                return jsonify({'status': 'success', 'redirect': '/'})

        # Trường hợp 2: Gửi từ Form đăng nhập chuẩn
        username = request.form.get('username')
        password = request.form.get('password')
        user = UserService.check_login(username, password)
        if user:
            session['user'] = user.username
            # Lấy đúng Họ và Tên lúc đăng ký
            session['user_fullname'] = getattr(user, 'full_name', user.username)
            return redirect(url_for('index'))
        else:
            return render_template('login.html', msg="Tài khoản hoặc mật khẩu không đúng!", msg_type="danger")

    return render_template('login.html')


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


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


# --- API CÔNG TY ---
@app.route("/api/company", methods=["GET", "POST"])
def handle_company():
    if request.method == "POST":
        data = request.json or request.form.to_dict()
        CompanyService.save(data)
        return jsonify({"msg": "OK"})
    return jsonify([c.__dict__ for c in CompanyService.get_all()])


@app.route("/api/company/<id>", methods=["PUT", "DELETE"])
def update_delete_company(id):
    if request.method == "DELETE":
        CompanyService.delete(id)
    else:
        data = request.json or request.form.to_dict()
        CompanyService.save(data)
    return jsonify({"msg": "OK"})


# --- API PHÒNG BAN ---
@app.route("/api/department", methods=["GET", "POST"])
def handle_department():
    if request.method == "POST":
        data = request.json or request.form.to_dict()
        DepartmentService.save(data)
        return jsonify({"msg": "OK"})
    return jsonify([d.__dict__ for d in DepartmentService.get_all()])


@app.route("/api/department/<id>", methods=["PUT", "DELETE"])
def update_delete_department(id):
    if request.method == "DELETE":
        DepartmentService.delete(id)
    else:
        data = request.json or request.form.to_dict()
        DepartmentService.save(data)
    return jsonify({"msg": "OK"})


# --- API CÔNG TRÌNH ---
@app.route("/api/project", methods=["GET", "POST"])
def handle_project():
    if request.method == "POST":
        data = request.json or request.form.to_dict()
        ProjectService.save(data)
        return jsonify({"msg": "OK"})
    return jsonify([p.__dict__ for p in ProjectService.get_all()])


@app.route("/api/project/<id>", methods=["PUT", "DELETE"])
def update_delete_project(id):
    if request.method == "DELETE":
        ProjectService.delete(id)
    else:
        data = request.json or request.form.to_dict()
        ProjectService.save(data)
    return jsonify({"msg": "OK"})


# --- API HẠNG MỤC ---
@app.route("/api/item", methods=["GET", "POST"])
def handle_item():
    if request.method == "POST":
        data = request.json or request.form.to_dict()
        ItemService.save(data)
        return jsonify({"msg": "OK"})
    return jsonify([i.__dict__ for i in ItemService.get_all()])


@app.route("/api/item/<id>", methods=["PUT", "DELETE"])
def update_delete_item(id):
    if request.method == "DELETE":
        ItemService.delete(id)
    else:
        data = request.json or request.form.to_dict()
        ItemService.save(data)
    return jsonify({"msg": "OK"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
