from flask import Flask, render_template, jsonify, request
from models import init_db
from services import CompanyService

app = Flask(__name__)
init_db()

@app.route("/")
def home():
    # Trả về giao diện HTML cho Máy khách (Client)
    return render_template("index.html")

# API CÔNG TY (Giao tiếp với Tầng Nghiệp vụ)
@app.route("/api/company", methods=["GET"])
def get_companies():
    data = CompanyService.get_all()
    # Chuyển đổi danh sách đối tượng sang dạng List Dict để trả về JSON
    return jsonify([c.__dict__ for c in data])

@app.route("/api/company", methods=["POST"])
def save_company():
    try:
        CompanyService.save(request.json)
        return jsonify({"status": "success", "msg": "Lưu thành công"})
    except ValueError as e:
        return jsonify({"status": "error", "msg": str(e)}), 400

@app.route("/api/company/<id>", methods=["DELETE"])
def delete_company(id):
    CompanyService.delete(id)
    return jsonify({"status": "success", "msg": "Đã xóa"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)