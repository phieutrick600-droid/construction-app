import sqlite3

DB_NAME = "construction_management.db"


def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS cong_ty
                   (
                       ma_cty
                       TEXT
                       PRIMARY
                       KEY,
                       ten_cty
                       TEXT
                       NOT
                       NULL,
                       dia_chi
                       TEXT,
                       so_dien_thoai
                       TEXT,
                       nguoi_dai_dien
                       TEXT
                   )
                   """)
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS phong_ban
                   (
                       ma_pb
                       TEXT
                       PRIMARY
                       KEY,
                       ten_pb
                       TEXT
                       NOT
                       NULL,
                       ma_cty
                       TEXT,
                       truong_phong
                       TEXT,
                       so_nhan_su
                       INTEGER
                   )
                   """)
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS cong_trinh
                   (
                       ma_ct
                       TEXT
                       PRIMARY
                       KEY,
                       ten_ct
                       TEXT
                       NOT
                       NULL,
                       dia_diem
                       TEXT,
                       chu_dau_tu
                       TEXT,
                       trang_thai
                       TEXT
                   )
                   """)
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS hang_muc
                   (
                       ma_hm
                       TEXT
                       PRIMARY
                       KEY,
                       ten_hm
                       TEXT
                       NOT
                       NULL,
                       ma_ct
                       TEXT,
                       kinh_phi
                       REAL,
                       tien_do
                       TEXT
                   )
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


import sqlite3


class User:
    def __init__(self, id, username, password, full_name, role="admin"):
        self.id = id
        self.username = username
        self.password = password
        self.full_name = full_name
        self.role = role


# --- GIỮ NGUYÊN CODE CŨ CỦA BẠN BÊN TRÊN ---

# BỔ SUNG: Class User
class User:
    def __init__(self, id, username, password, full_name):
        self.id = id
        self.username = username
        self.password = password
        self.full_name = full_name


# Cập nhật hàm khởi tạo DB (Thêm tạo bảng users)
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Bảng users
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS users
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       username
                       TEXT
                       UNIQUE
                       NOT
                       NULL,
                       password
                       TEXT
                       NOT
                       NULL,
                       full_name
                       TEXT
                       NOT
                       NULL
                   )
                   ''')

    # 2. Bảng công ty (cong_ty)
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS cong_ty
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       ten_cong_ty
                       TEXT
                       NOT
                       NULL,
                       ma_so_thue
                       TEXT,
                       dia_chi
                       TEXT
                   )
                   ''')

    # 3. Bảng phòng ban (phong_ban)
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS phong_ban
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       ten_phong_ban
                       TEXT
                       NOT
                       NULL,
                       cong_ty_id
                       INTEGER,
                       FOREIGN
                       KEY
                   (
                       cong_ty_id
                   ) REFERENCES cong_ty
                   (
                       id
                   )
                       )
                   ''')

    # 4. Bảng dự án (du_an)
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS du_an
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       ten_du_an
                       TEXT
                       NOT
                       NULL,
                       dia_diem
                       TEXT,
                       phong_ban_id
                       INTEGER,
                       FOREIGN
                       KEY
                   (
                       phong_ban_id
                   ) REFERENCES phong_ban
                   (
                       id
                   )
                       )
                   ''')

    # 5. Bảng hạng mục (hang_muc)
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS hang_muc
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       ten_hang_muc
                       TEXT
                       NOT
                       NULL,
                       chi_phi
                       REAL,
                       du_an_id
                       INTEGER,
                       FOREIGN
                       KEY
                   (
                       du_an_id
                   ) REFERENCES du_an
                   (
                       id
                   )
                       )
                   ''')

    conn.commit()
    conn.close()


# Tự động gọi khởi tạo bảng
init_db()
