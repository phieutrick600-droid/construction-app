import sqlite3


# --- 1. ĐỊNH NGHĨA CÁC LỚP ĐỐI TƯỢNG (CLASS) ---
class CongTy:
    def __init__(self, ma_cty, ten_cty, dia_chi="", so_dien_thoai="", nguoi_dai_dien=""):
        self.ma_cty = ma_cty
        self.ten_cty = ten_cty
        self.dia_chi = dia_chi
        self.so_dien_thoai = so_dien_thoai
        self.nguoi_dai_dien = nguoi_dai_dien


class PhongBan:
    def __init__(self, ma_pb, ten_pb, ma_cty="", truong_phong="", so_nhan_su=0):
        self.ma_pb = ma_pb
        self.ten_pb = ten_pb
        self.ma_cty = ma_cty
        self.truong_phong = truong_phong
        self.so_nhan_su = so_nhan_su


class CongTrinh:
    def __init__(self, ma_ct, ten_ct, dia_diem="", chu_dau_tu="", trang_thai=""):
        self.ma_ct = ma_ct
        self.ten_ct = ten_ct
        self.dia_diem = dia_diem
        self.chu_dau_tu = chu_dau_tu
        self.trang_thai = trang_thai


class HangMuc:
    def __init__(self, ma_hm, ten_hm, ma_ct="", kinh_phi=0, tien_do=""):
        self.ma_hm = ma_hm
        self.ten_hm = ten_hm
        self.ma_ct = ma_ct
        self.kinh_phi = kinh_phi
        self.tien_do = tien_do


# --- 2. TẦNG THAO TÁC DỮ LIỆU CSDL (DATABASE ACCESS LAYER) ---
DB_FILE = "construction_management.db"


def get_db_connection():
    return sqlite3.connect(DB_FILE)


def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS công_ty
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
                   )""")
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
                   )""")
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
                   )""")
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
                   )""")

    conn.commit()
    conn.close()


# --- HÀM TRUY VẤN CÔNG TY ---
def db_get_all_company():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM công_ty")
    rows = cursor.fetchall()
    conn.close()
    return [CongTy(*r) for r in rows]


def db_save_company(c: CongTy):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO công_ty VALUES (?, ?, ?, ?, ?)",
                   (c.ma_cty, c.ten_cty, c.dia_chi, c.so_dien_thoai, c.nguoi_dai_dien))
    conn.commit()
    conn.close()


def db_delete_company(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM công_ty WHERE ma_cty = ?", (id,))
    conn.commit()
    conn.close()