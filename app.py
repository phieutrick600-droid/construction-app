# --- TRANG CHỦ / DANG NHAP / DANG KY / DANG XUAT ---
@app.route("/")
def index():
    # Kiểm tra xem người dùng đã đăng nhập chưa. Nếu chưa -> Bắt buộc ra trang login
    if 'user' not in session:
        return redirect(url_for('login'))

    companies = CompanyService.get_all()
    departments = DepartmentService.get_all()
    projects = ProjectService.get_all()
    items = ItemService.get_all()

    # Lấy đúng họ tên đã lưu trong Session khi đăng nhập
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
        # 1. Trường hợp gửi dạng JSON (từ Firebase JS)
        if request.is_json:
            data = request.get_json(silent=True) or {}
            email = data.get('email')
            full_name = data.get('full_name')

            if email:
                session['user'] = email
                # Ưu tiên lấy Họ tên từ JS truyền sang, nếu không có mới tìm CSDL hoặc dùng email
                if full_name:
                    session['user_fullname'] = full_name
                else:
                    user = UserService.check_login(email, None)
                    if user and getattr(user, 'full_name', None):
                        session['user_fullname'] = user.full_name
                    else:
                        session['user_fullname'] = email.split('@')[0]
                return jsonify({'status': 'success', 'redirect': '/'})

        # 2. Trường hợp gửi dạng Form thông thường
        username = request.form.get('username')
        password = request.form.get('password')
        user = UserService.check_login(username, password)
        if user:
            session['user'] = user.username
            session['user_fullname'] = getattr(user, 'full_name', user.username)
            return redirect(url_for('index'))
        else:
            return render_template('login.html', msg="Tài khoản hoặc mật khẩu không đúng!", msg_type="danger")

    return render_template('login.html')
