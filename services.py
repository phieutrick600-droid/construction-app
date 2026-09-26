from models import (
    CongTy, db_get_all_company, db_save_company, db_delete_company
)


class CompanyService:
    @staticmethod
    def get_all():
        # Gọi xuống Tầng CSDL
        return db_get_all_company()

    @staticmethod
    def save(data):
        # Kiểm tra logic Nghiệp vụ
        if not data.get("ma_cty") or not data.get("ten_cty"):
            raise ValueError("Mã công ty và Tên công ty không được để trống!")

        # Khởi tạo đối tượng Class
        company = CongTy(
            ma_cty=data["ma_cty"],
            ten_cty=data["ten_cty"],
            dia_chi=data.get("dia_chi", ""),
            so_dien_thoai=data.get("so_dien_thoai", ""),
            nguoi_dai_dien=data.get("nguoi_dai_dien", "")
        )

        # Chuyển đối tượng xuống Tầng CSDL để lưu
        db_save_company(company)

    @staticmethod
    def delete(id):
        db_delete_company(id)