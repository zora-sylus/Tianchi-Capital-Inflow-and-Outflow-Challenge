from src.data_loader import load_all_data
from src.feature_engineering import prepare_daily_table, build_supervised_features
from src.train import train_models
from src.predict import recursive_predict
from src.utils import ensure_dirs


def main():
    ensure_dirs()
    print("1. 正在读取 data 文件夹中的比赛数据...")
    balance, profile, interest, shibor = load_all_data()

    print("2. 正在聚合每日申购和赎回数据...")
    daily = prepare_daily_table(balance, interest=interest, shibor=shibor)

    print("3. 正在构造机器学习特征...")
    feature_df = build_supervised_features(daily)

    print("4. 正在训练传统机器学习模型...")
    models, feature_cols, scores = train_models(feature_df)
    print("验证集 MAE：", scores)

    print("5. 正在预测 2014-09-01 至 2014-09-30...")
    out_path, sub = recursive_predict(daily, models, feature_cols)

    print("完成！提交文件已生成：", out_path)
    print(sub.head())


if __name__ == "__main__":
    main()
