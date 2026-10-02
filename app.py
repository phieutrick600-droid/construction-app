from flask import Flask, render_template, render_template_string, request, jsonify, session, redirect, url_for
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'lo_khai_construction_secret_key'

DATABASE = 'database.db'


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db() as conn:
        cursor = conn.cursor()

        # Bảng Công ty
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS company (
                ma_cty TEXT PRIMARY KEY,
                ten_cty TEXT NOT NULL,
                dia_chi TEXT,
                so_dien_thoai TEXT,
                nguoi_dai_dien TEXT
            )
        ''')

        # Bảng Phòng ban
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS department (
                ma_pb TEXT PRIMARY KEY,
                ten_pb TEXT NOT NULL,
                ma_cty TEXT,
                truong_phong TEXT,
                so_nhan_su INTEGER,
                FOREIGN KEY (ma_cty) REFERENCES company (ma_cty)
            )
        ''')

        # Bảng Công trình
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS project (
                ma_ct TEXT PRIMARY KEY,
                ten_ct TEXT NOT NULL,
                dia_diem TEXT,
                chu_dau_tu TEXT,
                trang_thai TEXT,
                ma_cty TEXT,
                FOREIGN KEY (ma_cty) REFERENCES company (ma_cty)
            )
        ''')

        # Bảng Hạng mục
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS item (
                ma_hm TEXT PRIMARY KEY,
                ten_hm TEXT NOT NULL,
                ma_ct TEXT,
                kinh_phi REAL,
                tien_do TEXT,
                FOREIGN KEY (ma_ct) REFERENCES project (ma_ct)
            )
        ''')
        conn.commit()


init_db()


# --- GIAO DIỆN ĐĂNG NHẬP ---
LOGIN_HTML = '''
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Đăng nhập - LÒ KHẢI CONSTRUCTION</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        body { background-color: #1a252f; height: 100vh; display: flex; align-items: center; justify-content: center; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        .card-login { width: 100%; max-width: 420px; border-radius: 12px; box-shadow: 0 8px 24px rgba(0,0,0,0.3); border: none; }
        .header-title { color: #ffc107; font-weight: bold; }
    </style>
</head>
<body>
<div class="card card-login p-4 bg-white">
    <div class="text-center mb-4">
        <h3 class="header-title text-dark"><i class="fa-solid fa-city text-warning me-2"></i>LÒ KHẢI</h3>
        <p class="text-muted small">Hệ Thống Quản Lý Doanh Nghiệp & Xây Dựng</p>
    </div>
    
    {% if error %}
    <div class="alert alert-danger p-2 text-center small" role="alert">{{ error }}</div>
    {% endif %}

    <form method="POST" action="/login">
        <div class="mb-3">
            <label class="form-label fw-bold">Email / Tài khoản</label>
            <div class="input-group">
                <span class="input-group-text"><i class="fa-solid fa-envelope"></i></span>
                <input type="email" name="email" class="form-control" value="phieutrick600@gmail.com" required>
            </div>
        </div>
        <div class="mb-3">
            <label class="form-label fw-bold">Mật khẩu</label>
            <div class="input-group">
                <span class="input-group-text"><i class="fa-solid fa-lock"></i></span>
                <input type="password" name="password" class="form-control" placeholder="Nhập mật khẩu bất kỳ" required>
            </div>
        </div>
        <button type="submit" class="btn btn-primary w-100 fw-bold py-2 mt-2">
            <i class="fa-solid fa-right-to-bracket me-1"></i> Đăng Nhập
        </button>
    </form>
</div>
</body>
</html>
'''


# --- ROUTES AUTHENTICATION ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        if email:
            session['user'] = email
            return redirect(url_for('index'))
        return render_template_string(LOGIN_HTML, error="Vui lòng nhập Email!")
    return render_template_string(LOGIN_HTML)


@app.route('/')
def index():
    # Bắt buộc chuyển sang trang Đăng nhập nếu chưa có session
    if 'user' not in session:
        return redirect(url_for('login'))
        
    user_fullname = session.get('user', 'phieutrick600@gmail.com')
    return render_template('index.html', user_fullname=user_fullname)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


# --- API CÔNG TY ---
@app.route('/api/company', methods=['GET', 'POST'])
def api_company():
    conn = get_db()
    cursor = conn.cursor()
    if request.method == 'POST':
        data = request.json
        cursor.execute('''
            INSERT OR REPLACE INTO company (ma_cty, ten_cty, dia_chi, so_dien_thoai, nguoi_dai_dien)
            VALUES (?, ?, ?, ?, ?)
        ''', (data.get('ma_cty'), data.get('ten_cty'), data.get('dia_chi'), data.get('so_dien_thoai'),
              data.get('nguoi_dai_dien')))
        conn.commit()
        return jsonify({'success': True})
    else:
        cursor.execute('SELECT * FROM company')
        rows = [dict(r) for r in cursor.fetchall()]
        return jsonify(rows)


@app.route('/api/company/<ma_cty>', methods=['DELETE'])
def del_company(ma_cty):
    conn = get_db()
    conn.execute('DELETE FROM company WHERE ma_cty = ?', (ma_cty,))
    conn.commit()
    return jsonify({'success': True})


# --- API PHÒNG BAN ---
@app.route('/api/department', methods=['GET', 'POST'])
def api_department():
    conn = get_db()
    cursor = conn.cursor()
    if request.method == 'POST':
        data = request.json
        cursor.execute('''
            INSERT OR REPLACE INTO department (ma_pb, ten_pb, ma_cty, truong_phong, so_nhan_su)
            VALUES (?, ?, ?, ?, ?)
        ''', (data.get('ma_pb'), data.get('ten_pb'), data.get('ma_cty'), data.get('truong_phong'),
              data.get('so_nhan_su')))
        conn.commit()
        return jsonify({'success': True})
    else:
        cursor.execute('SELECT * FROM department')
        rows = [dict(r) for r in cursor.fetchall()]
        return jsonify(rows)


@app.route('/api/department/<ma_pb>', methods=['DELETE'])
def del_department(ma_pb):
    conn = get_db()
    conn.execute('DELETE FROM department WHERE ma_pb = ?', (ma_pb,))
    conn.commit()
    return jsonify({'success': True})


# --- API CÔNG TRÌNH ---
@app.route('/api/project', methods=['GET', 'POST'])
def api_project():
    conn = get_db()
    cursor = conn.cursor()
    if request.method == 'POST':
        data = request.json
        cursor.execute('''
            INSERT OR REPLACE INTO project (ma_ct, ten_ct, dia_diem, chu_dau_tu, trang_thai, ma_cty)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (data.get('ma_ct'), data.get('ten_ct'), data.get('dia_diem'), data.get('chu_dau_tu'),
              data.get('trang_thai'), data.get('ma_cty')))
        conn.commit()
        return jsonify({'success': True})
    else:
        cursor.execute('SELECT * FROM project')
        rows = [dict(r) for r in cursor.fetchall()]
        return jsonify(rows)


@app.route('/api/project/<ma_ct>', methods=['DELETE'])
def del_project(ma_ct):
    conn = get_db()
    conn.execute('DELETE FROM project WHERE ma_ct = ?', (ma_ct,))
    conn.commit()
    return jsonify({'success': True})


# --- API HẠNG MỤC ---
@app.route('/api/item', methods=['GET', 'POST'])
def api_item():
    conn = get_db()
    cursor = conn.cursor()
    if request.method == 'POST':
        data = request.json
        cursor.execute('''
            INSERT OR REPLACE INTO item (ma_hm, ten_hm, ma_ct, kinh_phi, tien_do)
            VALUES (?, ?, ?, ?, ?)
        ''', (data.get('ma_hm'), data.get('ten_hm'), data.get('ma_ct'), data.get('kinh_phi'), data.get('tien_do')))
        conn.commit()
        return jsonify({'success': True})
    else:
        cursor.execute('SELECT * FROM item')
        rows = [dict(r) for r in cursor.fetchall()]
        return jsonify(rows)


@app.route('/api/item/<ma_hm>', methods=['DELETE'])
def del_item(ma_hm):
    conn = get_db()
    conn.execute('DELETE FROM item WHERE ma_hm = ?', (ma_hm,))
    conn.commit()
    return jsonify({'success': True})


# --- API TRA CỨU HẠNG MỤC THEO CÔNG TY ---
@app.route('/api/search', methods=['GET'])
def api_search():
    ma_cty = request.args.get('ma_cty')
    if not ma_cty:
        return jsonify({'success': False, 'message': 'Thiếu tham số ma_cty'})

    conn = get_db()
    cursor = conn.cursor()

    query = '''
        SELECT 
            p.ten_ct,
            i.ten_hm,
            i.kinh_phi,
            i.tien_do
        FROM item i
        JOIN project p ON i.ma_ct = p.ma_ct
        WHERE p.ma_cty = ?
    '''
    cursor.execute(query, (ma_cty,))
    rows = [dict(r) for r in cursor.fetchall()]

    total_money = sum(r['kinh_phi'] for r in rows if r['kinh_phi'])

    return jsonify({
        'success': True,
        'data': rows,
        'total_money': total_money
    })


if __name__ == '__main__':
    app.run(debug=True)
