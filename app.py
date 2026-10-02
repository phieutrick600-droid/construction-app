from flask import Flask, render_template, request, jsonify, session, redirect, url_for
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
        
        # Bảng Công trình (ĐÃ BỔ SUNG MA_CTY)
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

# --- ROUTES NỀN TẢNG ---
@app.route('/')
def index():
    user_fullname = session.get('user', 'phieutrick600@gmail.com')
    return render_template('index.html', user_fullname=user_fullname)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

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
        ''', (data.get('ma_cty'), data.get('ten_cty'), data.get('dia_chi'), data.get('so_dien_thoai'), data.get('nguoi_dai_dien')))
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
        ''', (data.get('ma_pb'), data.get('ten_pb'), data.get('ma_cty'), data.get('truong_phong'), data.get('so_nhan_su')))
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
        ''', (data.get('ma_ct'), data.get('ten_ct'), data.get('dia_diem'), data.get('chu_dau_tu'), data.get('trang_thai'), data.get('ma_cty')))
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

# --- API TRA CỨU ĐÃ ĐƯỢC CỦA TỐI ƯU SQL ---
@app.route('/api/search', methods=['GET'])
def api_search():
    ma_cty = request.args.get('ma_cty')
    if not ma_cty:
        return jsonify({'success': False, 'message': 'Thiếu tham số ma_cty'})

    conn = get_db()
    cursor = conn.cursor()
    
    # JOIN từ item -> project theo ma_cty
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
