from pathlib import Path
import zipfile
import pandas as pd
from .utils import DATA_DIR


def _find_file(candidates):
    for name in candidates:
        p = DATA_DIR / name
        if p.exists():
            return p
    return None


def _read_csv_or_zip(base_names):
    csv_path = _find_file([f"{n}.csv" for n in base_names])
    if csv_path is not None:
        return pd.read_csv(csv_path)

    zip_path = _find_file([f"{n}.zip" for n in base_names])
    if zip_path is not None:
        with zipfile.ZipFile(zip_path) as zf:
            csv_members = [m for m in zf.namelist() if m.lower().endswith(".csv")]
            if not csv_members:
                raise FileNotFoundError(f"压缩包 {zip_path.name} 中没有 csv 文件")
            with zf.open(csv_members[0]) as f:
                return pd.read_csv(f)

    names = ", ".join([f"{n}.csv/.zip" for n in base_names])
    raise FileNotFoundError(f"data 文件夹中没有找到：{names}")


def load_all_data():
    balance = _read_csv_or_zip(["user_balance_table", "user_balance_table(1)", "user_balance_table(2)"])

    try:
        profile = _read_csv_or_zip(["user_profile_table", "user_profile_table(1)", "user_profile_table(2)"])
    except FileNotFoundError:
        profile = None

    try:
        interest = _read_csv_or_zip(["mfd_day_share_interest", "mfd_day_share_interest(1)", "mfd_day_share_interest(2)"])
    except FileNotFoundError:
        interest = None

    try:
        shibor = _read_csv_or_zip(["mfd_bank_shibor", "mfd_bank_shibor(1)", "mfd_bank_shibor(2)"])
    except FileNotFoundError:
        shibor = None

    return balance, profile, interest, shibor
