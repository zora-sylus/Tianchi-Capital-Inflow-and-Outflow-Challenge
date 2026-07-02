# data 文件夹说明

请将天池比赛下载并解压后的数据文件放到本文件夹中。

需要的文件名通常包括：

- user_balance_table.csv 或 user_balance_table.zip
- user_profile_table.csv
- mfd_day_share_interest.csv
- mfd_bank_shibor.csv

本 GitHub 项目不上传比赛原始数据。运行 `python main.py` 时，程序会自动读取本文件夹中的数据并生成 `output/submission.csv`。
