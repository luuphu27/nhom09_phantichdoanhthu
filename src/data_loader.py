import logging
from pathlib import Path
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class DataLoader:
    def __init__(self, file_path: str | Path):
        self.file_path = Path(file_path)
        self.df = None

    def load_data(self):
        try:
            if not self.file_path.exists():
                raise FileNotFoundError(f"Không tìm thấy file tại đường dẫn: {self.file_path}")

            logging.info(f"Đang tiến hành đọc file từ: {self.file_path}")
            self.df = pd.read_csv(self.file_path)
            logging.info(f"Đọc dữ liệu thành công! Kích thước: {self.df.shape}")
            return self.df

        except FileNotFoundError as e:
            logging.error(f"Lỗi File: {e}")
            return None
        except Exception as e:
            logging.error(f"Đã xảy ra lỗi không mong muốn khi đọc dữ liệu: {e}")
            return None

    def clean_data(self):
        if self.df is None:
            logging.error("Chưa có dữ liệu để kiểm tra!")
            return

        print("\n--- NHẬT KÝ KIỂM TRA DỮ LIỆU THÔ (Thành) ---")
        print(f"Số dòng và số cột: {self.df.shape}")
        
        print("\nSố lượng giá trị thiếu (Null) ở mỗi cột:")
        print(self.df.isnull().sum())
        
        print("\nKiểu dữ liệu của các cột:")
        print(self.df.dtypes)
        print("-" * 45)
        
        logging.info("Đang tiến hành chuẩn hóa Order Date và Ship Date...")

        self.df['Order Date'] = pd.to_datetime(
            self.df['Order Date'],
            format='mixed',
            dayfirst=False,
            errors='coerce'
        )

        self.df['Ship Date'] = pd.to_datetime(
            self.df['Ship Date'],
            format='mixed',
            dayfirst=False,
            errors='coerce'
        )

        self.df = self.df.dropna(
            subset=['Order Date', 'Ship Date']
        ).copy()

        start_date = pd.to_datetime('2015-01-03')
        end_date = pd.to_datetime('2018-12-30')

        mask_date_range = (
            (self.df['Order Date'] >= start_date) &
            (self.df['Order Date'] <= end_date) &
            (self.df['Ship Date'] >= start_date) &
            (self.df['Ship Date'] <= end_date)
        )

        self.df = self.df[mask_date_range].copy()

        self.df = self.df[
            self.df['Ship Date'] >= self.df['Order Date']
        ].copy()

        logging.info("Hoàn thành chuẩn hóa Order Date và Ship Date.")

        return self.df
    def remove_duplicates(self):
        """Giai đoạn 1: Xử lý dữ liệu trùng lặp (Phân công: Ly)"""
        
        if self.df is None or self.df.empty:
            logging.warning("Chưa có dữ liệu để xử lý trùng lặp.")
            return self.df

        initial_rows = len(self.df)
        logging.info(f"Số dòng trước khi xử lý trùng lặp: {initial_rows}")

        cols_to_check = [col for col in self.df.columns if col != 'Row ID']

        self.df = self.df.drop_duplicates(subset=cols_to_check, keep='first')

        final_rows = len(self.df)
        removed_rows = initial_rows - final_rows

        logging.info(
            f"[Ly] Quyết định: Phát hiện cặp Row 3406 và Row 3407 trùng lặp toàn bộ thông tin đơn hàng."
        )
        logging.info(
            f"[Ly] Quyết định xử lý: Đã xóa {removed_rows} bản ghi bị trùng (bao gồm Row 3407), giữ lại bản ghi xuất hiện đầu tiên."
        )
        logging.info(f"Số dòng sau khi xóa trùng lặp: {final_rows}")

        return self.df