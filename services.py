from models import get_db_connection, Company, Department, Project, Item, User

class CompanyService:
    @staticmethod
    def get_all():
        conn = get_db_connection()
        rows = conn.execute("SELECT * FROM cong_ty").fetchall()
        conn.close()
        return [Company(r["ma_cty"], r["ten_cty"], r["dia_chi"], r["so_dien_thoai"], r["nguoi_dai_dien"]) for r in rows]

    @staticmethod
    def save(data):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT ma_cty FROM cong_ty WHERE ma_cty = ?", (data.get("ma_cty"),))
        if cursor.fetchone():
            cursor.execute("""
                UPDATE cong_ty SET ten_cty=?, dia_chi=?, so_dien_thoai=?, nguoi_dai_dien=? WHERE ma_cty=?
            """, (data.get("ten_cty"), data.get("dia_chi"), data.get("so_dien_thoai"), data.get("nguoi_dai_dien"), data.get("ma_cty")))
        else:
            cursor.execute("""
                INSERT INTO cong_ty VALUES (?, ?, ?, ?, ?)
            """, (data.get("ma_cty"), data.get("ten_cty"), data.get("dia_chi"), data.get("so_dien_thoai"), data.get("nguoi_dai_dien")))
        conn.commit()
        conn.close()

    @staticmethod
    def delete(ma_cty):
        conn = get_db_connection()
        conn.execute("DELETE FROM cong_ty WHERE ma_cty = ?", (ma_cty,))
        conn.commit()
        conn.close()

class DepartmentService:
    @staticmethod
    def get_all():
        conn = get_db_connection()
        rows = conn.execute("SELECT * FROM phong_ban").fetchall()
        conn.close()
        return [Department(r["ma_pb"], r["ten_pb"], r["ma_cty"], r["truong_phong"], r["so_nhan_su"]) for r in rows]

    @staticmethod
    def save(data):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT ma_pb FROM phong_ban WHERE ma_pb = ?", (data.get("ma_pb"),))
        if cursor.fetchone():
            cursor.execute("""
                UPDATE phong_ban SET ten_pb=?, ma_cty=?, truong_phong=?, so_nhan_su=? WHERE ma_pb=?
            """, (data.get("ten_pb"), data.get("ma_cty"), data.get("truong_phong"), data.get("so_nhan_su"), data.get("ma_pb")))
        else:
            cursor.execute("""
                INSERT INTO phong_ban VALUES (?, ?, ?, ?, ?)
            """, (data.get("ma_pb"), data.get("ten_pb"), data.get("ma_cty"), data.get("truong_phong"), data.get("so_nhan_su")))
        conn.commit()
        conn.close()

    @staticmethod
    def delete(ma_pb):
        conn = get_db_connection()
        conn.execute("DELETE FROM phong_ban WHERE ma_pb = ?", (ma_pb,))
        conn.commit()
        conn.close()

class ProjectService:
    @staticmethod
    def get_all():
        conn = get_db_connection()
        rows = conn.execute("SELECT * FROM cong_trinh").fetchall()
        conn.close()
        return [Project(r["ma_ct"], r["ten_ct"], r["dia_diem"], r["chu_dau_tu"], r["trang_thai"]) for r in rows]

    @staticmethod
    def save(data):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT ma_ct FROM cong_trinh WHERE ma_ct = ?", (data.get("ma_ct"),))
        if cursor.fetchone():
            cursor.execute("""
                UPDATE cong_trinh SET ten_ct=?, dia_diem=?, chu_dau_tu=?, trang_thai=? WHERE ma_ct=?
            """, (data.get("ten_ct"), data.get("dia_diem"), data.get("chu_dau_tu"), data.get("trang_thai"), data.get("ma_ct")))
        else:
            cursor.execute("""
                INSERT INTO cong_trinh VALUES (?, ?, ?, ?, ?)
            """, (data.get("ma_ct"), data.get("ten_ct"), data.get("dia_diem"), data.get("chu_dau_tu"), data.get("trang_thai")))
        conn.commit()
        conn.close()

    @staticmethod
    def delete(ma_ct):
        conn = get_db_connection()
        conn.execute("DELETE FROM cong_trinh WHERE ma_ct = ?", (ma_ct,))
        conn.commit()
        conn.close()

class ItemService:
    @staticmethod
    def get_all():
        conn = get_db_connection()
        rows = conn.execute("SELECT * FROM hang_muc").fetchall()
        conn.close()
        return [Item(r["ma_hm"], r["ten_hm"], r["ma_ct"], r["kinh_phi"], r["tien_do"]) for r in rows]

    @staticmethod
    def save(data):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT ma_hm FROM hang_muc WHERE ma_hm = ?", (data.get("ma_hm"),))
        if cursor.fetchone():
            cursor.execute("""
                UPDATE hang_muc SET ten_hm=?, ma_ct=?, kinh_phi=?, tien_do=? WHERE ma_hm=?
            """, (data.get("ten_hm"), data.get("ma_ct"), data.get("kinh_phi"), data.get("tien_do"), data.get("ma_hm")))
        else:
            cursor.execute("""
                INSERT INTO hang_muc VALUES (?, ?, ?, ?, ?)
            """, (data.get("ma_hm"), data.get("ten_hm"), data.get("ma_ct"), data.get("kinh_phi"), data.get("tien_do")))
        conn.commit()
        conn.close()

    @staticmethod
    def delete(ma_hm):
        conn = get_db_connection()
        conn.execute("DELETE FROM hang_muc WHERE ma_hm = ?", (ma_hm,))
        conn.commit()
        conn.close()
# --- GIỮ NGUYÊN CODE CŨ CỦA BẠN BÊN TRÊN ---

# BỔ SUNG: UserService xử lý Đăng nhập & Đăng ký
class UserService:
    @staticmethod
    def register(username, password, full_name):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password, full_name) VALUES (?, ?, ?)",
                           (username, password, full_name))
            conn.commit()
            return True, "Đăng ký tài khoản thành công! Vui lòng đăng nhập."
        except Exception as e:
            return False, "Tên đăng nhập đã tồn tại trên hệ thống!"
        finally:
            conn.close()

    @staticmethod
    def check_login(username, password):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        row = cursor.fetchone()
        conn.close()
        if row:
            return User(row['id'], row['username'], row['password'], row['full_name'])
        return None
