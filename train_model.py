import pandas as pd
import numpy as np
from surprise import KNNBasic, Dataset, Reader, dump 
import random

# --- HÀM TẠO DỮ LIỆU TỰ ĐỘNG (600 BẢN GHI) ---
hos = ["Nguyễn", "Trần", "Lê", "Phạm", "Hoàng", "Phan", "Vũ", "Đặng", "Bùi", "Đỗ", "Hồ", "Ngô", "Dương", "Lý", "Trương"]
tens_dem = ["Văn", "Thị", "Anh", "Minh", "Xuân", "Hữu", "Đức", "Bảo", "Ngọc", "Phương", "Quang", "Khánh", "Tuấn"]
tens_chinh = ["Tuấn", "Hạnh", "Dũng", "Lan", "Hương", "Nam", "Cường", "Trang", "Linh", "Quân", "Đông", "Mai", "Sơn", "Hà", "Phi", "Phúc", "Tâm", "Huy"]

chu_de = ["Tình", "Mưa", "Nắng", "Gió", "Biển", "Phố", "Đường", "Hoa", "Mây", "Trăng", "Kỷ Niệm", "Lời Yêu", "Giấc Mơ"]
tinh_tu = ["Xa", "Lạ", "Buồn", "Vui", "Nhớ", "Quên", "Đau", "Thương", "Sầu", "Say", "Mơ", "Lặng", "Rơi"]
the_loai_list = ["Pop", "Rap", "R&B", "Indie", "Ballad", "Rock", "Dance", "Jazz", "Lo-fi", "Bolero"]

data_600 = []
used_combinations = set()

while len(data_600) < 600:
    # Tạo tên ca sĩ ngẫu nhiên
    ten_cs = f"{random.choice(hos)} {random.choice(tens_dem)} {random.choice(tens_chinh)}"
    # Tạo tên bài hát ngẫu nhiên (kèm số để đảm bảo không trùng)
    ten_bh = f"{random.choice(chu_de)} {random.choice(tinh_tu)} ({random.randint(100, 999)})"
    
    combo = (ten_cs, ten_bh)
    if combo not in used_combinations:
        the_loai = random.choice(the_loai_list)
        data_600.append((ten_cs, ten_bh, the_loai))
        used_combinations.add(combo)

# Chuyển thành DataFrame
artists = pd.DataFrame({
    'artistID': [i for i in range(1, 601)],
    'name': [x[0] for x in data_600],
    'song_title': [x[1] for x in data_600],
    'genre': [x[2] for x in data_600],
    'Stt': [f"ID_{i}" for i in range(1, 601)]
})
artists.to_csv('artists.csv', index=False)

# --- TẠO TƯƠNG TÁC CHO 50 USER (Mỗi người nghe 40 bài) ---
user_ids, item_ids, ratings = [], [], []
for u in range(1, 51): # Tạo 50 người dùng để "hàng xóm" đông đúc hơn
    watched_items = random.sample(range(1, 601), 40) 
    for item in watched_items:
        user_ids.append(u)
        item_ids.append(item)
        ratings.append(random.randint(3, 5))

df_ratings = pd.DataFrame({'userID': user_ids, 'itemID': item_ids, 'rating': ratings})

# Huấn luyện mô hình KNN (Neighborhood-Based)
reader = Reader(rating_scale=(1, 5))
data_surprise = Dataset.load_from_df(df_ratings[['userID', 'itemID', 'rating']], reader)
trainset = data_surprise.build_full_trainset()

sim_options = {'name': 'cosine', 'user_based': True}
model = KNNBasic(sim_options=sim_options)
model.fit(trainset)

dump.dump('music_model.pkl', algo=model)
print(f" Đã tạo xong 600 bản ghi. Đã huấn luyện xong mô hình KNN!")