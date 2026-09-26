from flask import Flask, render_template, jsonify, request
from models import init_db
from services import CompanyService, DepartmentService, ProjectService, ItemService

app = Flask(__name__)
init_db()

@app.route("/")
def home():
    return render_template("index.html")

# --- API CÔNG TY ---
@app.route("/api/company", methods=["GET"])
def get_companies():
    return jsonify([c.__dict__ for c in CompanyService.get_all()])

@app.route("/api/company", methods=["POST", "PUT"])
def save_company():
    try:
        CompanyService.save(request.json)
        return jsonify({"msg": "OK"})
    except ValueError as e:
        return jsonify({"msg": str(e)}), 400

@app.route("/api/company/<id>", methods=["PUT", "DELETE"])
def handle_company_id(id):
    if request.method == "DELETE":
        CompanyService.delete(id)
    else:
        CompanyService.save(request.json)
    return jsonify({"msg": "OK"})

# --- API PHÒNG BAN ---
@app.route("/api/department", methods=["GET"])
def get_depts():
    return jsonify([d.__dict__ for d in DepartmentService.get_all()])

@app.route("/api/department", methods=["POST", "PUT"])
def save_dept():
    try:
        DepartmentService.save(request.json)
        return jsonify({"msg": "OK"})
    except ValueError as e:
        return jsonify({"msg": str(e)}), 400

@app.route("/api/department/<id>", methods=["PUT", "DELETE"])
def handle_dept_id(id):
    if request.method == "DELETE":
        DepartmentService.delete(id)
    else:
        DepartmentService.save(request.json)
    return jsonify({"msg": "OK"})

# --- API CÔNG TRÌNH ---
@app.route("/api/project", methods=["GET"])
def get_projects():
    return jsonify([p.__dict__ for p in ProjectService.get_all()])

@app.route("/api/project", methods=["POST", "PUT"])
def save_project():
    try:
        ProjectService.save(request.json)
        return jsonify({"msg": "OK"})
    except ValueError as e:
        return jsonify({"msg": str(e)}), 400

@app.route("/api/project/<id>", methods=["PUT", "DELETE"])
def handle_project_id(id):
    if request.method == "DELETE":
        ProjectService.delete(id)
    else:
        ProjectService.save(request.json)
    return jsonify({"msg": "OK"})

# --- API HẠNG MỤC ---
@app.route("/api/item", methods=["GET"])
def get_items():
    return jsonify([i.__dict__ for i in ItemService.get_all()])

@app.route("/api/item", methods=["POST", "PUT"])
def save_item():
    try:
        ItemService.save(request.json)
        return jsonify({"msg": "OK"})
    except ValueError as e:
        return jsonify({"msg": str(e)}), 400

@app.route("/api/item/<id>", methods=["PUT", "DELETE"])
def handle_item_id(id):
    if request.method == "DELETE":
        ItemService.delete(id)
    else:
        ItemService.save(request.json)
    return jsonify({"msg": "OK"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
