import sqlite3
from flask import Flask, jsonify, render_template_string, request

app = Flask(__name__)


# --- KHỞI TẠO CƠ SỞ DỮ LIỆU ---
def init_db():
    conn = sqlite3.connect("construction_management.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS công_ty (
            ma_cty TEXT PRIMARY KEY,
            ten_cty TEXT NOT NULL,
            dia_chi TEXT,
            so_dien_thoai TEXT,
            nguoi_dai_dien TEXT
        )
    """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS phong_ban (
            ma_pb TEXT PRIMARY KEY,
            ten_pb TEXT NOT NULL,
            ma_cty TEXT,
            truong_phong TEXT,
            so_nhan_su INTEGER
        )
    """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS cong_trinh (
            ma_ct TEXT PRIMARY KEY,
            ten_ct TEXT NOT NULL,
            dia_diem TEXT,
            chu_dau_tu TEXT,
            trang_thai TEXT
        )
    """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS hang_muc (
            ma_hm TEXT PRIMARY KEY,
            ten_hm TEXT NOT NULL,
            ma_ct TEXT,
            kinh_phi REAL,
            tien_do TEXT
        )
    """
    )

    conn.commit()
    conn.close()


init_db()

# --- GIAO DIỆN HTML ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LÒ KHẢI CONSTRUCTION - Management System</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        body { background-color: #f4f6f9; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        .navbar-brand { font-weight: bold; font-size: 1.4rem; letter-spacing: 1px; }
        .card { border-radius: 12px; border: none; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
        .nav-tabs .nav-link { font-weight: 600; color: #495057; border-radius: 8px 8px 0 0; cursor: pointer; }
        .nav-tabs .nav-link.active { background-color: #ffffff; color: #0d6efd; border-bottom: 3px solid #0d6efd; }
        .tab-pane { display: none; }
        .tab-pane.active { display: block; }
        .table-hover tbody tr:hover { background-color: #f1f5f9; }
    </style>
</head>
<body>

    <!-- Header Navbar -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark shadow-sm py-3 mb-4">
        <div class="container">
            <a class="navbar-brand text-warning" href="#">
                <i class="fa-solid fa-building-user me-2"></i>LÒ KHẢI CONSTRUCTION
            </a>
            <span class="navbar-text text-white-50">Hệ Thống Quản Lý Doanh Nghiệp & Xây Dựng</span>
        </div>
    </nav>

    <div class="container pb-5">
        <!-- Navigation Tabs -->
        <ul class="nav nav-tabs mb-4" id="mainTabs">
            <li class="nav-item">
                <button class="nav-link active" onclick="switchTab('company')">
                    <i class="fa-solid fa-building me-2"></i>Quản lý Công ty
                </button>
            </li>
            <li class="nav-item">
                <button class="nav-link" onclick="switchTab('dept')">
                    <i class="fa-solid fa-sitemap me-2"></i>Quản lý Phòng ban
                </button>
            </li>
            <li class="nav-item">
                <button class="nav-link" onclick="switchTab('project')">
                    <i class="fa-solid fa-helmet-safety me-2"></i>Quản lý Công trình
                </button>
            </li>
            <li class="nav-item">
                <button class="nav-link" onclick="switchTab('item')">
                    <i class="fa-solid fa-list-check me-2"></i>Quản lý Hạng mục
                </button>
            </li>
        </ul>

        <!-- Tab Contents -->
        <!-- TAB 1: CÔNG TY -->
        <div class="tab-pane active" id="pane-company">
            <div class="row g-4">
                <div class="col-lg-4">
                    <div class="card p-4">
                        <h5 class="card-title fw-bold text-primary mb-3"><i class="fa-solid fa-plus-circle me-2"></i>Thêm Công Ty</h5>
                        <form id="companyForm">
                            <div class="mb-2"><label class="form-label">Mã Công Ty</label><input type="text" id="ma_cty" class="form-control" required></div>
                            <div class="mb-2"><label class="form-label">Tên Công Ty</label><input type="text" id="ten_cty" class="form-control" required></div>
                            <div class="mb-2"><label class="form-label">Địa Chỉ/Địa Điểm</label><input type="text" id="dia_chi_cty" class="form-control"></div>
                            <div class="mb-2"><label class="form-label">Số Điện Thoại</label><input type="text" id="sdt_cty" class="form-control"></div>
                            <div class="mb-3"><label class="form-label">Người Đại Diện</label><input type="text" id="nguoi_dd" class="form-control"></div>
                            <button type="button" onclick="saveCompany()" class="btn btn-primary w-100 fw-bold">Lưu Thông Tin</button>
                        </form>
                    </div>
                </div>
                <div class="col-lg-8">
                    <div class="card p-4">
                        <h5 class="card-title fw-bold text-secondary mb-3"><i class="fa-solid fa-table me-2"></i>Danh Sách Công Ty</h5>
                        <table class="table table-hover align-middle">
                            <thead class="table-light">
                                <tr><th>Mã CTY</th><th>Tên Công Ty</th><th>Địa Chỉ</th><th>SĐT</th><th>Đại Diện</th><th>Thao Tác</th></tr>
                            </thead>
                            <tbody id="companyTable"></tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>

        <!-- TAB 2: PHÒNG BAN -->
        <div class="tab-pane" id="pane-dept">
            <div class="row g-4">
                <div class="col-lg-4">
                    <div class="card p-4">
                        <h5 class="card-title fw-bold text-primary mb-3"><i class="fa-solid fa-plus-circle me-2"></i>Thêm Phòng Ban</h5>
                        <form id="deptForm">
                            <div class="mb-2"><label class="form-label">Mã Phòng Ban</label><input type="text" id="ma_pb" class="form-control" required></div>
                            <div class="mb-2"><label class="form-label">Tên Phòng Ban</label><input type="text" id="ten_pb" class="form-control" required></div>
                            <div class="mb-2"><label class="form-label">Thuộc Công Ty (Mã)</label><input type="text" id="ma_cty_pb" class="form-control"></div>
                            <div class="mb-2"><label class="form-label">Trưởng Phòng</label><input type="text" id="truong_phong" class="form-control"></div>
                            <div class="mb-3"><label class="form-label">Số Lượng Nhân Sự</label><input type="number" id="so_nhan_su" class="form-control"></div>
                            <button type="button" onclick="saveDept()" class="btn btn-primary w-100 fw-bold">Lưu Thông Tin</button>
                        </form>
                    </div>
                </div>
                <div class="col-lg-8">
                    <div class="card p-4">
                        <h5 class="card-title fw-bold text-secondary mb-3"><i class="fa-solid fa-table me-2"></i>Danh Sách Phòng Ban</h5>
                        <table class="table table-hover align-middle">
                            <thead class="table-light">
                                <tr><th>Mã PB</th><th>Tên Phòng Ban</th><th>Mã CTY</th><th>Trưởng Phòng</th><th>Nhân Sự</th><th>Thao Tác</th></tr>
                            </thead>
                            <tbody id="deptTable"></tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>

        <!-- TAB 3: CÔNG TRÌNH -->
        <div class="tab-pane" id="pane-project">
            <div class="row g-4">
                <div class="col-lg-4">
                    <div class="card p-4">
                        <h5 class="card-title fw-bold text-primary mb-3"><i class="fa-solid fa-plus-circle me-2"></i>Thêm Công Trình</h5>
                        <form id="projectForm">
                            <div class="mb-2"><label class="form-label">Mã Công Trình</label><input type="text" id="ma_ct" class="form-control" required></div>
                            <div class="mb-2"><label class="form-label">Tên Công Trình</label><input type="text" id="ten_ct" class="form-control" required></div>
                            <div class="mb-2"><label class="form-label">Địa Điểm</label><input type="text" id="dia_diem_ct" class="form-control"></div>
                            <div class="mb-2"><label class="form-label">Chủ Đầu Tư</label><input type="text" id="chu_dau_tu" class="form-control"></div>
                            <div class="mb-3"><label class="form-label">Trạng Thái/Tiến Độ</label><input type="text" id="trang_thai_ct" class="form-control"></div>
                            <button type="button" onclick="saveProject()" class="btn btn-primary w-100 fw-bold">Lưu Thông Tin</button>
                        </form>
                    </div>
                </div>
                <div class="col-lg-8">
                    <div class="card p-4">
                        <h5 class="card-title fw-bold text-secondary mb-3"><i class="fa-solid fa-table me-2"></i>Danh Sách Công Trình</h5>
                        <table class="table table-hover align-middle">
                            <thead class="table-light">
                                <tr><th>Mã CT</th><th>Tên Công Trình</th><th>Địa Điểm</th><th>Chủ Đầu Tư</th><th>Trạng Thái</th><th>Thao Tác</th></tr>
                            </thead>
                            <tbody id="projectTable"></tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>

        <!-- TAB 4: HẠNG MỤC -->
        <div class="tab-pane" id="pane-item">
            <div class="row g-4">
                <div class="col-lg-4">
                    <div class="card p-4">
                        <h5 class="card-title fw-bold text-primary mb-3"><i class="fa-solid fa-plus-circle me-2"></i>Thêm Hạng Mục</h5>
                        <form id="itemForm">
                            <div class="mb-2"><label class="form-label">Mã Hạng Mục</label><input type="text" id="ma_hm" class="form-control" required></div>
                            <div class="mb-2"><label class="form-label">Tên Hạng Mục</label><input type="text" id="ten_hm" class="form-control" required></div>
                            <div class="mb-2"><label class="form-label">Thuộc Công Trình (Mã)</label><input type="text" id="ma_ct_hm" class="form-control"></div>
                            <div class="mb-2"><label class="form-label">Kinh Phí (VND)</label><input type="number" id="kinh_phi" class="form-control"></div>
                            <div class="mb-3"><label class="form-label">Tiến Độ Thi Công</label><input type="text" id="tien_do" class="form-control"></div>
                            <button type="button" onclick="saveItem()" class="btn btn-primary w-100 fw-bold">Lưu Thông Tin</button>
                        </form>
                    </div>
                </div>
                <div class="col-lg-8">
                    <div class="card p-4">
                        <h5 class="card-title fw-bold text-secondary mb-3"><i class="fa-solid fa-table me-2"></i>Danh Sách Hạng Mục</h5>
                        <table class="table table-hover align-middle">
                            <thead class="table-light">
                                <tr><th>Mã HM</th><th>Tên Hạng Mục</th><th>Mã CT</th><th>Kinh Phí</th><th>Tiến Độ</th><th>Thao Tác</th></tr>
                            </thead>
                            <tbody id="itemTable"></tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>

    </div>

    <script>
        // Hàm chuyển Tab trực tiếp
        function switchTab(tabName) {
            // Ẩn tất cả nội dung tab
            document.querySelectorAll('.tab-pane').forEach(el => el.classList.remove('active'));
            // Bỏ active ở tất cả các nút
            document.querySelectorAll('#mainTabs .nav-link').forEach(el => el.classList.remove('active'));

            // Hiển thị tab được chọn
            document.getElementById('pane-' + tabName).classList.add('active');
            
            // Active nút bấm tương ứng
            const btnIndex = {'company': 0, 'dept': 1, 'project': 2, 'item': 3}[tabName];
            document.querySelectorAll('#mainTabs .nav-link')[btnIndex].classList.add('active');

            // Load dữ liệu tab tương ứng
            if(tabName === 'company') loadCompany();
            if(tabName === 'dept') loadDept();
            if(tabName === 'project') loadProject();
            if(tabName === 'item') loadItem();
        }

        // --- CÔNG TY ---
        async function loadCompany() {
            const res = await fetch('/api/company');
            const data = await res.json();
            const tbody = document.getElementById('companyTable');
            tbody.innerHTML = '';
            data.forEach(c => {
                tbody.innerHTML += `<tr>
                    <td class="fw-bold">${c[0]}</td><td>${c[1]}</td><td>${c[2]||'-'}</td><td>${c[3]||'-'}</td><td>${c[4]||'-'}</td>
                    <td><button class="btn btn-sm btn-outline-danger" onclick="deleteRecord('/api/company', '${c[0]}', loadCompany)"><i class="fa-solid fa-trash"></i></button></td>
                </tr>`;
            });
        }
        async function saveCompany() {
            const payload = {
                ma_cty: document.getElementById('ma_cty').value, ten_cty: document.getElementById('ten_cty').value,
                dia_chi: document.getElementById('dia_chi_cty').value, so_dien_thoai: document.getElementById('sdt_cty').value,
                nguoi_dai_dien: document.getElementById('nguoi_dd').value
            };
            if(!payload.ma_cty || !payload.ten_cty) { alert('Vui lòng nhập Mã và Tên công ty!'); return; }
            await fetch('/api/company', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(payload) });
            document.getElementById('companyForm').reset();
            loadCompany();
        }

        // --- PHÒNG BAN ---
        async function loadDept() {
            const res = await fetch('/api/department');
            const data = await res.json();
            const tbody = document.getElementById('deptTable');
            tbody.innerHTML = '';
            data.forEach(d => {
                tbody.innerHTML += `<tr>
                    <td class="fw-bold">${d[0]}</td><td>${d[1]}</td><td>${d[2]||'-'}</td><td>${d[3]||'-'}</td><td>${d[4]||0}</td>
                    <td><button class="btn btn-sm btn-outline-danger" onclick="deleteRecord('/api/department', '${d[0]}', loadDept)"><i class="fa-solid fa-trash"></i></button></td>
                </tr>`;
            });
        }
        async function saveDept() {
            const payload = {
                ma_pb: document.getElementById('ma_pb').value, ten_pb: document.getElementById('ten_pb').value,
                ma_cty: document.getElementById('ma_cty_pb').value, truong_phong: document.getElementById('truong_phong').value,
                so_nhan_su: document.getElementById('so_nhan_su').value
            };
            if(!payload.ma_pb || !payload.ten_pb) { alert('Vui lòng nhập Mã và Tên phòng ban!'); return; }
            await fetch('/api/department', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(payload) });
            document.getElementById('deptForm').reset();
            loadDept();
        }

        // --- CÔNG TRÌNH ---
        async function loadProject() {
            const res = await fetch('/api/project');
            const data = await res.json();
            const tbody = document.getElementById('projectTable');
            tbody.innerHTML = '';
            data.forEach(p => {
                tbody.innerHTML += `<tr>
                    <td class="fw-bold">${p[0]}</td><td>${p[1]}</td><td>${p[2]||'-'}</td><td>${p[3]||'-'}</td><td><span class="badge bg-info text-dark">${p[4]||'-'}</span></td>
                    <td><button class="btn btn-sm btn-outline-danger" onclick="deleteRecord('/api/project', '${p[0]}', loadProject)"><i class="fa-solid fa-trash"></i></button></td>
                </tr>`;
            });
        }
        async function saveProject() {
            const payload = {
                ma_ct: document.getElementById('ma_ct').value, ten_ct: document.getElementById('ten_ct').value,
                dia_diem: document.getElementById('dia_diem_ct').value, chu_dau_tu: document.getElementById('chu_dau_tu').value,
                trang_thai: document.getElementById('trang_thai_ct').value
            };
            if(!payload.ma_ct || !payload.ten_ct) { alert('Vui lòng nhập Mã và Tên công trình!'); return; }
            await fetch('/api/project', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(payload) });
            document.getElementById('projectForm').reset();
            loadProject();
        }

        // --- HẠNG MỤC ---
        async function loadItem() {
            const res = await fetch('/api/item');
            const data = await res.json();
            const tbody = document.getElementById('itemTable');
            tbody.innerHTML = '';
            data.forEach(i => {
                tbody.innerHTML += `<tr>
                    <td class="fw-bold">${i[0]}</td><td>${i[1]}</td><td>${i[2]||'-'}</td><td>${i[3]? Number(i[3]).toLocaleString() : 0} VNĐ</td><td>${i[4]||'-'}</td>
                    <td><button class="btn btn-sm btn-outline-danger" onclick="deleteRecord('/api/item', '${i[0]}', loadItem)"><i class="fa-solid fa-trash"></i></button></td>
                </tr>`;
            });
        }
        async function saveItem() {
            const payload = {
                ma_hm: document.getElementById('ma_hm').value, ten_hm: document.getElementById('ten_hm').value,
                ma_ct: document.getElementById('ma_ct_hm').value, kinh_phi: document.getElementById('kinh_phi').value,
                tien_do: document.getElementById('tien_do').value
            };
            if(!payload.ma_hm || !payload.ten_hm) { alert('Vui lòng nhập Mã và Tên hạng mục!'); return; }
            await fetch('/api/item', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(payload) });
            document.getElementById('itemForm').reset();
            loadItem();
        }

        // --- HÀM XÓA CHUNG ---
        async function deleteRecord(endpoint, id, callback) {
            if(confirm('Bạn có chắc chắn muốn xóa bản ghi này?')) {
                await fetch(`${endpoint}/${id}`, { method: 'DELETE' });
                callback();
            }
        }

        // Khởi tạo tab đầu tiên
        loadCompany();
    </script>
</body>
</html>
"""


# --- BACKEND FLASK ---
@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE)


@app.route("/api/company", methods=["GET", "POST"])
def handle_company():
    conn = sqlite3.connect("construction_management.db")
    cursor = conn.cursor()
    if request.method == "POST":
        d = request.json
        cursor.execute(
            "INSERT INTO công_ty VALUES (?, ?, ?, ?, ?)",
            (
                d["ma_cty"],
                d["ten_cty"],
                d["dia_chi"],
                d["so_dien_thoai"],
                d["nguoi_dai_dien"],
            ),
        )
        conn.commit()
        conn.close()
        return jsonify({"msg": "OK"})
    cursor.execute("SELECT * FROM công_ty")
    res = cursor.fetchall()
    conn.close()
    return jsonify(res)


@app.route("/api/company/<id>", methods=["DELETE"])
def delete_company(id):
    conn = sqlite3.connect("construction_management.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM công_ty WHERE ma_cty = ?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"msg": "OK"})


@app.route("/api/department", methods=["GET", "POST"])
def handle_department():
    conn = sqlite3.connect("construction_management.db")
    cursor = conn.cursor()
    if request.method == "POST":
        d = request.json
        cursor.execute(
            "INSERT INTO phong_ban VALUES (?, ?, ?, ?, ?)",
            (
                d["ma_pb"],
                d["ten_pb"],
                d["ma_cty"],
                d["truong_phong"],
                d["so_nhan_su"],
            ),
        )
        conn.commit()
        conn.close()
        return jsonify({"msg": "OK"})
    cursor.execute("SELECT * FROM phong_ban")
    res = cursor.fetchall()
    conn.close()
    return jsonify(res)


@app.route("/api/department/<id>", methods=["DELETE"])
def delete_department(id):
    conn = sqlite3.connect("construction_management.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM phong_ban WHERE ma_pb = ?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"msg": "OK"})


@app.route("/api/project", methods=["GET", "POST"])
def handle_project():
    conn = sqlite3.connect("construction_management.db")
    cursor = conn.cursor()
    if request.method == "POST":
        d = request.json
        cursor.execute(
            "INSERT INTO cong_trinh VALUES (?, ?, ?, ?, ?)",
            (
                d["ma_ct"],
                d["ten_ct"],
                d["dia_diem"],
                d["chu_dau_tu"],
                d["trang_thai"],
            ),
        )
        conn.commit()
        conn.close()
        return jsonify({"msg": "OK"})
    cursor.execute("SELECT * FROM cong_trinh")
    res = cursor.fetchall()
    conn.close()
    return jsonify(res)


@app.route("/api/project/<id>", methods=["DELETE"])
def delete_project(id):
    conn = sqlite3.connect("construction_management.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cong_trinh WHERE ma_ct = ?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"msg": "OK"})


@app.route("/api/item", methods=["GET", "POST"])
def handle_item():
    conn = sqlite3.connect("construction_management.db")
    cursor = conn.cursor()
    if request.method == "POST":
        d = request.json
        cursor.execute(
            "INSERT INTO hang_muc VALUES (?, ?, ?, ?, ?)",
            (d["ma_hm"], d["ten_hm"], d["ma_ct"], d["kinh_phi"], d["tien_do"]),
        )
        conn.commit()
        conn.close()
        return jsonify({"msg": "OK"})
    cursor.execute("SELECT * FROM hang_muc")
    res = cursor.fetchall()
    conn.close()
    return jsonify(res)


@app.route("/api/item/<id>", methods=["DELETE"])
def delete_item(id):
    conn = sqlite3.connect("construction_management.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM hang_muc WHERE ma_hm = ?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"msg": "OK"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
