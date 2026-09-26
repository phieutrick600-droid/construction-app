import sqlite3
from flask import Flask, jsonify, render_template_string, request

app = Flask(__name__)


def init_db():
    conn = sqlite3.connect("construction.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS project (
            ma_ct TEXT PRIMARY KEY,
            ten_ct TEXT NOT NULL,
            dia_diem TEXT,
            chu_dau_tu TEXT,
            trang_thai TEXT
        )
    """
    )
    conn.commit()
    conn.close()


init_db()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LÒ KHẢI CONSTRUCTION - Quản Lý Công Trình</title>
    <!-- Bootstrap 5 CSS & FontAwesome Icons -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        body { background-color: #f4f6f9; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        .navbar-brand { font-weight: bold; font-size: 1.4rem; letter-spacing: 1px; }
        .card { border-radius: 12px; border: none; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
        .table-hover tbody tr:hover { background-color: #f1f5f9; }
        .badge-status { font-size: 0.9rem; padding: 6px 12px; border-radius: 20px; }
    </style>
</head>
<body>

    <!-- Header Navbar -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark shadow-sm py-3 mb-4">
        <div class="container">
            <a class="navbar-brand text-warning" href="#">
                <i class="fa-solid fa-building-user me-2"></i>LÒ KHẢI CONSTRUCTION
            </a>
            <span class="navbar-text text-white-50">Hệ Thống Quản Lý Công Trình</span>
        </div>
    </nav>

    <div class="container pb-5">
        <div class="row g-4">
            <!-- Form Thêm / Sửa Công Trình -->
            <div class="col-lg-4">
                <div class="card p-4">
                    <h5 class="card-title fw-bold text-primary mb-3" id="formTitle">
                        <i class="fa-solid fa-plus-circle me-2"></i>Thêm Công Trình
                    </h5>
                    <form id="projectForm">
                        <div class="mb-3">
                            <label class="form-label fw-semibold">Mã công trình</label>
                            <input type="text" id="ma_ct" class="form-control" placeholder="VD: CTR01" required>
                        </div>
                        <div class="mb-3">
                            <label class="form-label fw-semibold">Tên công trình</label>
                            <input type="text" id="ten_ct" class="form-control" placeholder="VD: Đô thị Masteri" required>
                        </div>
                        <div class="mb-3">
                            <label class="form-label fw-semibold">Địa điểm</label>
                            <input type="text" id="dia_diem" class="form-control" placeholder="VD: Điện Biên">
                        </div>
                        <div class="mb-3">
                            <label class="form-label fw-semibold">Chủ đầu tư</label>
                            <input type="text" id="chu_dau_tu" class="form-control" placeholder="VD: LÒ KHẢI CONSTRUCTION">
                        </div>
                        <div class="mb-3">
                            <label class="form-label fw-semibold">Trạng thái / Tiến độ</label>
                            <input type="text" id="trang_thai" class="form-control" placeholder="VD: 80% hoặc Đang thi công">
                        </div>
                        
                        <div class="d-grid gap-2">
                            <button type="button" id="btnSave" onclick="saveProject()" class="btn btn-primary fw-semibold">
                                <i class="fa-solid fa-floppy-disk me-1"></i> Lưu Công Trình
                            </button>
                            <button type="button" id="btnCancel" onclick="resetForm()" class="btn btn-outline-secondary d-none">
                                Hủy Bỏ
                            </button>
                        </div>
                    </form>
                </div>
            </div>

            <!-- Danh sách công trình -->
            <div class="col-lg-8">
                <div class="card p-4">
                    <div class="d-flex justify-content-between align-items-center mb-3">
                        <h5 class="card-title fw-bold text-secondary m-0">
                            <i class="fa-solid fa-list-check me-2"></i>Danh Sách Công Trình
                        </h5>
                        <span class="badge bg-secondary" id="totalCount">0 công trình</span>
                    </div>

                    <div class="table-responsive">
                        <table class="table table-hover align-middle">
                            <thead class="table-light">
                                <tr>
                                    <th>Mã CT</th>
                                    <th>Tên Công Trình</th>
                                    <th>Địa Điểm</th>
                                    <th>Chủ Đầu Tư</th>
                                    <th>Trạng Thái</th>
                                    <th class="text-center">Thao Tác</th>
                                </tr>
                            </thead>
                            <tbody id="projectTable">
                                <!-- Dữ liệu sẽ load vào đây -->
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        let isEditing = false;

        async function loadProjects() {
            const res = await fetch('/api/projects');
            const data = await res.json();
            const tbody = document.getElementById('projectTable');
            document.getElementById('totalCount').innerText = `${data.length} công trình`;
            tbody.innerHTML = '';
            
            data.forEach(p => {
                tbody.innerHTML += `
                    <tr>
                        <td class="fw-bold text-primary">${p[0]}</td>
                        <td class="fw-semibold">${p[1]}</td>
                        <td>${p[2] || '-'}</td>
                        <td>${p[3] || '-'}</td>
                        <td><span class="badge bg-info text-dark badge-status">${p[4] || '-'}</span></td>
                        <td class="text-center">
                            <button class="btn btn-sm btn-outline-warning me-1" onclick="editProject('${p[0]}', '${p[1]}', '${p[2]||''}', '${p[3]||''}', '${p[4]||''}')">
                                <i class="fa-solid fa-pen"></i>
                            </button>
                            <button class="btn btn-sm btn-outline-danger" onclick="deleteProject('${p[0]}')">
                                <i class="fa-solid fa-trash"></i>
                            </button>
                        </td>
                    </tr>
                `;
            });
        }

        async function saveProject() {
            const ma_ct = document.getElementById('ma_ct').value.trim();
            const ten_ct = document.getElementById('ten_ct').value.trim();
            
            if(!ma_ct || !ten_ct) {
                alert('Vui lòng nhập đầy đủ Mã và Tên công trình!');
                return;
            }

            const payload = {
                ma_ct: ma_ct,
                ten_ct: ten_ct,
                dia_diem: document.getElementById('dia_diem').value.trim(),
                chu_dau_tu: document.getElementById('chu_dau_tu').value.trim(),
                trang_thai: document.getElementById('trang_thai').value.trim(),
            };

            const url = isEditing ? `/api/projects/${ma_ct}` : '/api/projects';
            const method = isEditing ? 'PUT' : 'POST';

            const res = await fetch(url, {
                method: method,
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(payload)
            });

            if(res.ok) {
                resetForm();
                loadProjects();
            } else {
                const err = await res.json();
                alert(err.message || 'Có lỗi xảy ra!');
            }
        }

        function editProject(ma, ten, diaDiem, chuDauTu, trangThai) {
            isEditing = true;
            document.getElementById('ma_ct').value = ma;
            document.getElementById('ma_ct').disabled = true; // Không sửa mã CT
            document.getElementById('ten_ct').value = ten;
            document.getElementById('dia_diem').value = diaDiem;
            document.getElementById('chu_dau_tu').value = chuDauTu;
            document.getElementById('trang_thai').value = trangThai;

            document.getElementById('formTitle').innerHTML = '<i class="fa-solid fa-pen-to-square me-2"></i>Cập Nhật Công Trình';
            document.getElementById('btnSave').className = 'btn btn-warning fw-semibold';
            document.getElementById('btnSave').innerHTML = '<i class="fa-solid fa-check me-1"></i> Cập Nhật';
            document.getElementById('btnCancel').classList.remove('d-none');
        }

        async function deleteProject(ma_ct) {
            if(confirm(`Bạn có chắc chắn muốn xóa công trình [${ma_ct}] không?`)) {
                await fetch(`/api/projects/${ma_ct}`, { method: 'DELETE' });
                loadProjects();
            }
        }

        function resetForm() {
            isEditing = false;
            document.getElementById('projectForm').reset();
            document.getElementById('ma_ct').disabled = false;
            document.getElementById('formTitle').innerHTML = '<i class="fa-solid fa-plus-circle me-2"></i>Thêm Công Trình';
            document.getElementById('btnSave').className = 'btn btn-primary fw-semibold';
            document.getElementById('btnSave').innerHTML = '<i class="fa-solid fa-floppy-disk me-1"></i> Lưu Công Trình';
            document.getElementById('btnCancel').classList.add('d-none');
        }

        loadProjects();
    </script>
</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE)


@app.route("/api/projects", methods=["GET"])
def get_projects():
    conn = sqlite3.connect("construction.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM project")
    data = cursor.fetchall()
    conn.close()
    return jsonify(data)


@app.route("/api/projects", methods=["POST"])
def add_project():
    data = request.json
    conn = sqlite3.connect("construction.db")
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO project VALUES (?, ?, ?, ?, ?)",
            (
                data["ma_ct"],
                data["ten_ct"],
                data["dia_diem"],
                data["chu_dau_tu"],
                data["trang_thai"],
            ),
        )
        conn.commit()
        return jsonify({"message": "Thêm thành công!"})
    except sqlite3.IntegrityError:
        return jsonify({"message": "Mã công trình đã tồn tại!"}), 400
    finally:
        conn.close()


@app.route("/api/projects/<ma_ct>", methods=["PUT"])
def update_project(ma_ct):
    data = request.json
    conn = sqlite3.connect("construction.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE project 
        SET ten_ct = ?, dia_diem = ?, chu_dau_tu = ?, trang_thai = ?
        WHERE ma_ct = ?
    """,
        (
            data["ten_ct"],
            data["dia_diem"],
            data["chu_dau_tu"],
            data["trang_thai"],
            ma_ct,
        ),
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Cập nhật thành công!"})


@app.route("/api/projects/<ma_ct>", methods=["DELETE"])
def delete_project(ma_ct):
    conn = sqlite3.connect("construction.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM project WHERE ma_ct = ?", (ma_ct,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Xóa thành công!"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
