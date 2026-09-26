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
    <title>Quản Lý Công Trình</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 30px; }
        .form-group { margin-bottom: 10px; }
        label { display: inline-block; width: 120px; }
        input { padding: 5px; width: 250px; }
        button { padding: 6px 12px; cursor: pointer; margin-top: 10px; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f4f4f4; }
    </style>
</head>
<body>
    <h2>Hệ Thống Quản Lý Công Trình Xây Dựng</h2>
    <form id="projectForm">
        <div class="form-group"><label>Mã công trình:</label><input type="text" id="ma_ct" required></div>
        <div class="form-group"><label>Tên công trình:</label><input type="text" id="ten_ct" required></div>
        <div class="form-group"><label>Địa điểm:</label><input type="text" id="dia_diem"></div>
        <div class="form-group"><label>Chủ đầu tư:</label><input type="text" id="chu_dau_tu"></div>
        <div class="form-group"><label>Trạng thái:</label><input type="text" id="trang_thai"></div>
        <button type="button" onclick="addProject()">Thêm Công Trình</button>
    </form>

    <table>
        <thead>
            <tr><th>Mã CT</th><th>Tên Công Trình</th><th>Địa Điểm</th><th>Chủ Đầu Tư</th><th>Trạng Thái</th></tr>
        </thead>
        <tbody id="projectTable"></tbody>
    </table>

    <script>
        async function loadProjects() {
            const res = await fetch('/api/projects');
            const data = await res.json();
            const tbody = document.getElementById('projectTable');
            tbody.innerHTML = '';
            data.forEach(p => {
                tbody.innerHTML += `<tr><td>${p[0]}</td><td>${p[1]}</td><td>${p[2]||''}</td><td>${p[3]||''}</td><td>${p[4]||''}</td></tr>`;
            });
        }

        async function addProject() {
            const payload = {
                ma_ct: document.getElementById('ma_ct').value,
                ten_ct: document.getElementById('ten_ct').value,
                dia_diem: document.getElementById('dia_diem').value,
                chu_dau_tu: document.getElementById('chu_dau_tu').value,
                trang_thai: document.getElementById('trang_thai').value,
            };
            await fetch('/api/projects', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(payload)
            });
            loadProjects();
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
    conn.close()
    return jsonify({"message": "OK"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)