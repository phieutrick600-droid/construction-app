import sqlite3

DB_NAME = "construction_management.db"


def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Bảng Công Ty
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cong_ty (
            ma_cty TEXT PRIMARY KEY,
            ten_cty TEXT NOT NULL,
            dia_chi TEXT,
            so_dien_thoai TEXT,
            nguoi_dai_dien TEXT
        )
    """)

    # 2. Bảng Phòng Ban
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS phong_ban (
            ma_pb TEXT PRIMARY KEY,
            ten_pb TEXT NOT NULL,
            ma_cty TEXT,
            truong_phong TEXT,
            so_nhan_su INTEGER
        )
    """)

    # 3. Bảng Công Trình
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cong_trinh (
            ma_ct TEXT PRIMARY KEY,
            ten_ct TEXT NOT NULL,
            dia_diem TEXT,
            chu_dau_tu TEXT,
            trang_thai TEXT
        )
    """)

    # 4. Bảng Hạng Mục
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS hang_muc (
            ma_hm TEXT PRIMARY KEY,
            ten_hm TEXT NOT NULL,
            ma_ct TEXT,
            kinh_phi REAL,
            tien_do TEXT
        )
    """)

    # 5. Bảng Users
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            full_name TEXT NOT NULL,
            role TEXT DEFAULT 'admin'
        )
    """)

    # --- CHÈN DỮ LIỆU MẪU BAN ĐẦU (Nếu chưa có) ---
    cursor.execute("SELECT COUNT(*) FROM cong_ty")
    if cursor.fetchone()[0] == 0:
        # Mẫu Công Ty
        cursor.execute("""
            INSERT INTO cong_ty (ma_cty, ten_cty, dia_chi, so_dien_thoai, nguoi_dai_dien)
            VALUES 
            ('CTY01', 'Công ty Cổ phần Xây dựng Lò Khải', 'Điện Biên', '0865539242', 'Lò Văn Khải'),
            ('CTY02', 'Tập đoàn Xây dựng Đặt Hàng', 'Hà Nội', '0912345678', 'Nguyễn Văn A')
        """)

        # Mẫu Phòng Ban
        cursor.execute("""
            INSERT INTO phong_ban (ma_pb, ten_pb, ma_cty, truong_phong, so_nhan_su)
            VALUES 
            ('PB01', 'Phòng Kỹ thuật & Thi công', 'CTY01', 'Lò Văn Khải', 15),
            ('PB02', 'Phòng Kế hoạch - Tài chính', 'CTY01', 'Trần Thị B', 8)
        """)

        # Mẫu Công Trình
        cursor.execute("""
            INSERT INTO cong_trinh (ma_ct, ten_ct, dia_diem, chu_dau_tu, trang_thai)
            VALUES 
            ('CT01', 'Xây dựng Trường học Mường Thanh', 'Điện Biên', 'Sở GD&ĐT Điện Biên', 'Đang thi công'),
            ('CT02', 'Cầu bê tông Kênh 1', 'Sơn La', 'UBND Huyện', 'Hoàn thành')
        """)

        # Mẫu Hạng Mục
        cursor.execute("""
            INSERT INTO hang_muc (ma_hm, ten_hm, ma_ct, kinh_phi, tien_do)
            VALUES 
            ('HM01', 'Thi công móng và phần ngầm', 'CT01', 500000000, '100%'),
            ('HM02', 'Xây thô tầng 1 & tầng 2', 'CT01', 800000000, '45%')
        """)

    conn.commit()
    conn.close()


# --- Model Objects ---
class Company:
    def __init__(self, ma_cty, ten_cty, dia_chi, so_dien_thoai, nguoi_dai_dien):
        self.ma_cty = ma_cty
        self.ten_cty = ten_cty
        self.dia_chi = dia_chi
        self.so_dien_thoai = so_dien_thoai
        self.nguoi_dai_dien = nguoi_dai_dien


class Department:
    def __init__(self, ma_pb, ten_pb, ma_cty, truong_phong, so_nhan_su):
        self.ma_pb = ma_pb
        self.ten_pb = ten_pb
        self.ma_cty = ma_cty
        self.truong_phong = truong_phong
        self.so_nhan_su = so_nhan_su


class Project:
    def __init__(self, ma_ct, ten_ct, dia_diem, chu_dau_tu, trang_thai):
        self.ma_ct = ma_ct
        self.ten_ct = ten_ct
        self.dia_diem = dia_diem
        self.chu_dau_tu = chu_dau_tu
        self.trang_thai = trang_thai


class Item:
    def __init__(self, ma_hm, ten_hm, ma_ct, kinh_phi, tien_do):
        self.ma_hm = ma_hm
        self.ten_hm = ten_hm
        self.ma_ct = ma_ct
        self.kinh_phi = kinh_phi
        self.tien_do = tien_do


class User:
    def __init__(self, id, username, password, full_name, role="admin"):
        self.id = id
        self.username = username
        self.password = password
        self.full_name = full_name
        self.role = role


# Tự động khởi tạo DB khi import
init_db()
