# Tianchi Capital Inflow and Outflow Prediction

本项目用于天池“资金流入流出预测”比赛课程设计。项目使用传统机器学习方法，读取比赛下载数据，训练模型并生成比赛提交文件 `submission.csv`。

> 说明：本仓库不包含比赛原始数据。请从比赛官网下载数据后，放入 `data/` 文件夹。

## 项目结构

```text
Tianchi-Capital-Inflow-and-Outflow-Challenge/
├── data/                     # 放置比赛数据，不上传原始数据
│   └── README.md
├── src/
│   ├── data_loader.py         # 数据读取
│   ├── feature_engineering.py # 特征工程
│   ├── train.py               # 模型训练
│   ├── predict.py             # 预测生成提交文件
│   └── utils.py               # 工具函数
├── models/                   # 保存模型
├── output/                   # 生成 submission.csv
├── main.py                   # 一键运行入口
├── requirements.txt
├── README.md
└── .gitignore
```

## 数据准备

请把比赛下载并解压后的文件放入 `data/` 文件夹，例如：

```text
data/
├── user_balance_table.csv 或 user_balance_table.zip
├── user_profile_table.csv
├── mfd_day_share_interest.csv
└── mfd_bank_shibor.csv
```

## 运行方法

安装依赖：

```bash
pip install -r requirements.txt
```

运行项目：

```bash
python main.py
```

运行结束后生成：

```text
output/submission.csv
```

该文件可直接提交到比赛平台。

## 方法说明

本项目未使用深度学习模型，符合课程要求。主要流程包括：

1. 聚合每日申购金额和赎回金额；
2. 构造日期特征，如星期、月份、是否周末等；
3. 构造滞后特征，如前 1 天、前 3 天、前 7 天等；
4. 构造滑动窗口统计特征，如 7 天、14 天、30 天均值和标准差；
5. 融合万份收益率和 Shibor 利率特征；
6. 分别训练申购金额和赎回金额预测模型；
7. 预测 2014 年 9 月 1 日至 2014 年 9 月 30 日的数据并生成提交文件。
