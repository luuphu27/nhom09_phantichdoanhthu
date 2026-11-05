
"""Chuẩn hóa Order Date và Ship Date cho dự án phân tích doanh thu."""

import logging
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)


class DateCleaner:
    """Chuẩn hóa và kiểm tra hai cột ngày của bộ dữ liệu đơn hàng."""

    DATE_COLUMNS = ("Order Date", "Ship Date")
    START_DATE = pd.Timestamp("2015-01-03")
    END_DATE = pd.Timestamp("2018-12-30")

    def __init__(self, df: pd.DataFrame) -> None:
        if not isinstance(df, pd.DataFrame):
            raise TypeError("df phải là một pandas DataFrame.")

        missing_columns = [
            column for column in self.DATE_COLUMNS if column not in df.columns
        ]

        if missing_columns:
            raise KeyError(
                "Thiếu cột cần chuẩn hóa: " + ", ".join(missing_columns)
            )

        # Tạo bản sao để không làm thay đổi dữ liệu gốc.
        self.df = df.copy()
        self.report: dict[str, int] = {}

    def clean_dates(self) -> pd.DataFrame:
        """Chuẩn hóa ngày tháng và loại bỏ các dòng không hợp lệ."""

        rows_before = len(self.df)

        logger.info("Bắt đầu chuẩn hóa Order Date và Ship Date...")

        # Bước 1: Chuẩn hóa định dạng ngày tháng.
        for column in self.DATE_COLUMNS:
            raw_dates = self.df[column].astype("string").str.strip()

            self.df[column] = pd.to_datetime(
                raw_dates,
                format="mixed",
                dayfirst=True,
                errors="coerce",
            )

        # Bước 2: Loại bỏ những dòng có ngày thiếu hoặc không hợp lệ.
        invalid_date_mask = self.df[
            list(self.DATE_COLUMNS)
        ].isna().any(axis=1)

        invalid_date_rows = int(invalid_date_mask.sum())

        self.df = self.df.loc[~invalid_date_mask].copy()

        # Bước 3: Kiểm tra khoảng thời gian hợp lệ.
        in_range_mask = (
            self.df["Order Date"].between(
                self.START_DATE, self.END_DATE
            )
            & self.df["Ship Date"].between(
                self.START_DATE, self.END_DATE
            )
        )

        out_of_range_rows = int((~in_range_mask).sum())

        self.df = self.df.loc[in_range_mask].copy()

        # Bước 4: Đảm bảo ngày giao hàng không trước ngày đặt hàng.
        wrong_order_mask = (
            self.df["Ship Date"] < self.df["Order Date"]
        )

        ship_before_order_rows = int(wrong_order_mask.sum())

        self.df = self.df.loc[~wrong_order_mask].copy()

        # Bước 5: Đánh lại chỉ số dòng.
        self.df.reset_index(drop=True, inplace=True)

        # Bước 6: Thống kê kết quả làm sạch.
        self.report = {
            "rows_before": rows_before,
            "invalid_date_rows": invalid_date_rows,
            "out_of_range_rows": out_of_range_rows,
            "ship_before_order_rows": ship_before_order_rows,
            "rows_after": len(self.df),
            "rows_removed": rows_before - len(self.df),
        }

        logger.info("Hoàn thành chuẩn hóa ngày tháng.")
        logger.info("Số dòng ban đầu: %s", rows_before)
        logger.info("Dòng có ngày thiếu/không hợp lệ: %s", invalid_date_rows)
        logger.info("Dòng ngoài khoảng thời gian: %s", out_of_range_rows)
        logger.info(
            "Dòng có Ship Date trước Order Date: %s",
            ship_before_order_rows,
        )
        logger.info("Số dòng còn lại: %s", len(self.df))

        return self.df


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    current_dir = Path(__file__).resolve().parent

    if current_dir.name.lower() == "src":
        project_root = current_dir.parent
    else:
        project_root = current_dir

    data_path = project_root / "data" / "train.csv"

    if not data_path.exists():
        raise FileNotFoundError(
            "Không tìm thấy data/train.csv. "
            "Hãy kiểm tra lại đường dẫn dữ liệu."
        )

    original_df = pd.read_csv(data_path)

    cleaner = DateCleaner(original_df)
    cleaned_df = cleaner.clean_dates()

    print("\n--- KẾT QUẢ KIỂM TRA NGÀY THÁNG ---")
    print(cleaner.report)

    print("\nKiểu dữ liệu sau chuẩn hóa:")
    print(cleaned_df[list(DateCleaner.DATE_COLUMNS)].dtypes)

    print("\n5 dòng đầu sau chuẩn hóa:")
    print(cleaned_df[list(DateCleaner.DATE_COLUMNS)].head())
