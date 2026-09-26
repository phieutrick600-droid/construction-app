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
