import pandas as pd
import joblib
from surprise import Dataset, Reader, KNNBasic
from surprise import accuracy
from surprise.model_selection import train_test_split


# BƯỚC 3, 4, 5, 6 – HUẤN LUYỆN MÔ HÌNH KNN + ĐÁNH GIÁ

print("=" * 50)
print("HUAN LUYEN MO HINH KNN - MUSIC")
print("=" * 50)

# Bước 3: Load dữ liệu đã lọc & chia train/val
df = pd.read_csv("ratings_filtered.csv")
print(f"Du lieu sau loc: {len(df)} dong")

reader   = Reader(rating_scale=(1, 5))
data     = Dataset.load_from_df(df[['user_id', 'song_title', 'rating']], reader)

trainset, testset = train_test_split(data, test_size=0.2, random_state=42)
print(f"Train      : {trainset.n_ratings} ratings")
print(f"Validation : {len(testset)} ratings")
print()

# Bước 4: Cấu hình & huấn luyện KNN
print("Bắt đầu khởi tạo KNN")

sim_options = {
    'name': 'cosine',
    'user_based': True
}

model = KNNBasic(
    k=20,
    min_k=3,
    sim_options=sim_options,
    verbose=True
)

model.fit(trainset)
print("Hoàn thành!")
print()


# Bước 5: Đánh giá RMSE & MAE

print(" Đánh giá mô hình trên tập Validation ")
predictions = model.test(testset)
rmse = accuracy.rmse(predictions)
mae  = accuracy.mae(predictions)
print(f"RMSE : {rmse:.4f}")
print(f"MAE  : {mae:.4f}")
print()

# Bước 6: Huấn luyện lại trên FULL dữ liệu & lưu
print("Huấn luyện trên toàn dữ liệu")
full_trainset = data.build_full_trainset()
model.fit(full_trainset)
print("Xong")

artifact = {
    "model":             model,
    "min_user_ratings":  5,
    "min_song_ratings":  2,
    "rmse_val":          round(rmse, 4),
    "mae_val":           round(mae,  4),
}

joblib.dump(artifact, "music_model.pkl")
print()
print("Đã Lưu vào: music_model.pkl")
print(" Xong và đánh giá")
