# import pandas as pd
# import numpy as np
# from surprise import KNNBasic, Dataset, Reader, dump 
# import random

# # --- HÀM TẠO DỮ LIỆU TỰ ĐỘNG (600 BẢN GHI) ---
# hos = ["Nguyễn", "Trần", "Lê", "Phạm", "Hoàng", "Phan", "Vũ", "Đặng", "Bùi", "Đỗ", "Hồ", "Ngô", "Dương", "Lý", "Trương"]
# tens_dem = ["Văn", "Thị", "Anh", "Minh", "Xuân", "Hữu", "Đức", "Bảo", "Ngọc", "Phương", "Quang", "Khánh", "Tuấn"]
# tens_chinh = ["Tuấn", "Hạnh", "Dũng", "Lan", "Hương", "Nam", "Cường", "Trang", "Linh", "Quân", "Đông", "Mai", "Sơn", "Hà", "Phi", "Phúc", "Tâm", "Huy"]

# chu_de = ["Tình", "Mưa", "Nắng", "Gió", "Biển", "Phố", "Đường", "Hoa", "Mây", "Trăng", "Kỷ Niệm", "Lời Yêu", "Giấc Mơ"]
# tinh_tu = ["Xa", "Lạ", "Buồn", "Vui", "Nhớ", "Quên", "Đau", "Thương", "Sầu", "Say", "Mơ", "Lặng", "Rơi"]
# the_loai_list = ["Pop", "Rap", "R&B", "Indie", "Ballad", "Rock", "Dance", "Jazz", "Lo-fi", "Bolero"]

# data_600 = []
# used_combinations = set()

# while len(data_600) < 600:
#     # Tạo tên ca sĩ ngẫu nhiên
#     ten_cs = f"{random.choice(hos)} {random.choice(tens_dem)} {random.choice(tens_chinh)}"
#     # Tạo tên bài hát ngẫu nhiên (kèm số để đảm bảo không trùng)
#     ten_bh = f"{random.choice(chu_de)} {random.choice(tinh_tu)} ({random.randint(100, 999)})"
    
#     combo = (ten_cs, ten_bh)
#     if combo not in used_combinations:
#         the_loai = random.choice(the_loai_list)
#         data_600.append((ten_cs, ten_bh, the_loai))
#         used_combinations.add(combo)

# # Chuyển thành DataFrame
# artists = pd.DataFrame({
#     'artistID': [i for i in range(1, 601)],
#     'name': [x[0] for x in data_600],
#     'song_title': [x[1] for x in data_600],
#     'genre': [x[2] for x in data_600],
#     'Stt': [f"ID_{i}" for i in range(1, 601)]
# })
# artists.to_csv('artists.csv', index=False)

# # --- TẠO TƯƠNG TÁC CHO 50 USER (Mỗi người nghe 40 bài) ---
# user_ids, item_ids, ratings = [], [], []
# for u in range(1, 51): # Tạo 50 người dùng để "hàng xóm" đông đúc hơn
#     watched_items = random.sample(range(1, 601), 40) 
#     for item in watched_items:
#         user_ids.append(u)
#         item_ids.append(item)
#         ratings.append(random.randint(3, 5))

# df_ratings = pd.DataFrame({'userID': user_ids, 'itemID': item_ids, 'rating': ratings})

# # Huấn luyện mô hình KNN (Neighborhood-Based)
# reader = Reader(rating_scale=(1, 5))
# data_surprise = Dataset.load_from_df(df_ratings[['userID', 'itemID', 'rating']], reader)
# trainset = data_surprise.build_full_trainset()

# sim_options = {'name': 'cosine', 'user_based': True}
# model = KNNBasic(sim_options=sim_options)
# model.fit(trainset)

# dump.dump('music_model.pkl', algo=model)
# print(f" Đã tạo xong 600 bản ghi. Đã huấn luyện xong mô hình KNN!")



# code mới 
import pandas as pd
import numpy as np
import random
from surprise import KNNBasic, Dataset, Reader, dump
from surprise.model_selection import cross_validate

# 1. TẠO DỮ LIỆU BÀI HÁT (600 bản ghi)
hos       = ["Nguyễn", "Trần", "Lê", "Phạm", "Hoàng", "Phan", "Vũ", "Đặng", "Bùi", "Đỗ",
             "Hồ", "Ngô", "Dương", "Lý", "Trương"]
tens_dem  = ["Văn", "Thị", "Anh", "Minh", "Xuân", "Hữu", "Đức", "Bảo", "Ngọc", "Phương",
             "Quang", "Khánh", "Tuấn"]
tens_chinh= ["Tuấn", "Hạnh", "Dũng", "Lan", "Hương", "Nam", "Cường", "Trang", "Linh",
             "Quân", "Đông", "Mai", "Sơn", "Hà", "Phi", "Phúc", "Tâm", "Huy"]

chu_de       = ["Tình", "Mưa", "Nắng", "Gió", "Biển", "Phố", "Đường", "Hoa", "Mây",
                "Trăng", "Kỷ Niệm", "Lời Yêu", "Giấc Mơ"]
tinh_tu      = ["Xa", "Lạ", "Buồn", "Vui", "Nhớ", "Quên", "Đau", "Thương", "Sầu",
                "Say", "Mơ", "Lặng", "Rơi"]
the_loai_list= ["Pop", "Rap", "R&B", "Indie", "Ballad", "Rock", "Dance", "Jazz", "Lo-fi", "Bolero"]

data_600, used = [], set()
while len(data_600) < 600:
    ten_cs = f"{random.choice(hos)} {random.choice(tens_dem)} {random.choice(tens_chinh)}"
    ten_bh = f"{random.choice(chu_de)} {random.choice(tinh_tu)} ({random.randint(100, 999)})"
    if (ten_cs, ten_bh) not in used:
        the_loai = random.choice(the_loai_list)
        data_600.append((ten_cs, ten_bh, the_loai))
        used.add((ten_cs, ten_bh))

artists = pd.DataFrame({
    'artistID':   range(1, 601),
    'name':       [x[0] for x in data_600],
    'song_title': [x[1] for x in data_600],
    'genre':      [x[2] for x in data_600],
    'Stt':        [f"ID_{i}" for i in range(1, 601)],
})
artists.to_csv('artists.csv', index=False)
print(f"✔ Đã tạo artists.csv ({len(artists)} bài hát)")

# 2. TẠO DỮ LIỆU TƯƠNG TÁC (50 user × 40 bài) 
user_ids, item_ids, ratings_list = [], [], []
for u in range(1, 51):
    for item in random.sample(range(1, 601), 40):
        user_ids.append(u)
        item_ids.append(item)
        ratings_list.append(random.randint(3, 5))

df_ratings_full = pd.DataFrame({
    'userID': user_ids,
    'itemID': item_ids,
    'rating': ratings_list,
})

#3. LỌC DUPLICATE & LƯU FILE 
df_ratings_filtered = df_ratings_full.drop_duplicates(subset=['userID', 'itemID'])
print(f"✔ Tổng ratings: {len(df_ratings_full)} → sau lọc: {len(df_ratings_filtered)} bản ghi "
      f"({len(df_ratings_filtered)/len(df_ratings_full)*100:.1f}%)")

# Merge thêm thông tin bài hát để lưu file đầy đủ (dùng trong main.py)
df_merged = df_ratings_filtered.merge(
    artists[['artistID', 'name', 'song_title', 'genre', 'Stt']],
    left_on='itemID', right_on='artistID', how='left'
).rename(columns={'userID': 'user_id'})[
    ['user_id', 'Stt', 'rating', 'artistID', 'name', 'song_title', 'genre']
]

df_ratings_full.rename(columns={'userID': 'user_id', 'itemID': 'artistID'}) \
               .merge(artists[['artistID','name','song_title','genre','Stt']], on='artistID', how='left') \
               [['user_id','Stt','rating','artistID','name','song_title','genre']] \
               .to_csv('ratings_full.csv', index=False)

df_merged.to_csv('ratings_filtered.csv', index=False)
print("✔ Đã lưu ratings_full.csv và ratings_filtered.csv")

# 4. HUẤN LUYỆN MÔ HÌNH KNN 
reader       = Reader(rating_scale=(1, 5))
data_surprise= Dataset.load_from_df(
    df_ratings_filtered[['userID', 'itemID', 'rating']], reader
)
trainset = data_surprise.build_full_trainset()

sim_options = {'name': 'cosine', 'user_based': True}
model = KNNBasic(sim_options=sim_options)
model.fit(trainset)
print("✔ Đã huấn luyện mô hình KNN (user-based, cosine similarity)")

# ── 5. ĐÁNH GIÁ MÔ HÌNH BẰNG RMSE (5-fold cross-validation)
print("\n⏳ Đang đánh giá mô hình (5-fold CV)...")
cv_results = cross_validate(
    KNNBasic(sim_options=sim_options),
    data_surprise,
    measures=['RMSE', 'MAE'],
    cv=5,
    verbose=False,
)
rmse_mean = cv_results['test_rmse'].mean()
mae_mean  = cv_results['test_mae'].mean()
print(f"✔ RMSE trung bình (5-fold): {rmse_mean:.4f}")
print(f"✔ MAE  trung bình (5-fold): {mae_mean:.4f}")

# 6. LƯU MÔ HÌNH 
dump.dump('music_model.pkl', algo=model)
print("\nHoàn tất! Đã lưu mô hình vào music_model.pkl")
print(f" Dữ liệu: 600 bài hát, 50 users, {len(df_ratings_filtered)} ratings")
print(f" RMSE: {rmse_mean:.4f} | MAE: {mae_mean:.4f}")
