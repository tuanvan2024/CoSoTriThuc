import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# BƯỚC 1 – THỐNG KÊ MÔ TẢ DỮ LIỆU

# Load dữ liệu bài hát
df_songs = pd.read_csv("artists.csv")

print("=" * 50)
print("Thống kê mô tả- MUSIC")
print("=" * 50)
print(f"Tổng số bài hát : {len(df_songs)}")
print(f"Số ca sĩ     : {df_songs['name'].nunique()}")
print(f"Số thể loại     : {df_songs['genre'].nunique()}")
print(f"Các thể loại    : {df_songs['genre'].unique().tolist()}")
print()

# Tạo dữ liệu rating giả lập
# 50 users, mỗi user nghe 40 bài, rating 3–5 sao

np.random.seed(42)
N_USERS   = 50
N_RATINGS = 40

song_ids = df_songs['Stt'].tolist()

records = []
for user_id in range(1, N_USERS + 1):
    chosen = np.random.choice(song_ids, size=N_RATINGS, replace=False)
    for stt in chosen:
        rating = np.random.randint(3, 6)
        records.append({"user_id": user_id, "Stt": stt, "rating": rating})

df_ratings = pd.DataFrame(records)
df = df_ratings.merge(df_songs, on="Stt", how="left")

# Lưu lại để các file sau dùng
df.to_csv("ratings_full.csv", index=False)

print(f"Da tao du lieu rating: {len(df)} ban ghi")
print(f"  User  : {df['user_id'].nunique()}")
print(f"Bài hát: {df['song_title'].nunique()}")
print()
print("Thống kê cột rating ")
print(df['rating'].describe())
print()

# Biểu đồ 1: Phân phối rating
plt.figure(figsize=(8, 4))
df['rating'].hist(bins=5, color='salmon', edgecolor='black')
plt.title("Phân phố rating bài hát")
plt.xlabel("Rating (3-5 sao)")
plt.ylabel("So luot")
plt.tight_layout()
plt.savefig("hist_rating.png", dpi=150)
plt.show()
print("Đã lưu: hist_rating.png")

# Biểu đồ 2: Số bài hát theo thể loại
plt.figure(figsize=(8, 4))
df_songs['genre'].value_counts().plot(kind='bar', color='steelblue', edgecolor='black')
plt.title("Số bài hát theo thể loại")
plt.xlabel("Thể loại")
plt.ylabel("Số bài")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig("hist_genre.png", dpi=150)
plt.show()
print("Đã lưu: hist_genre.png")

# Biểu đồ 3: Số rating mỗi user
ratings_per_user = df.groupby('user_id')['rating'].count()
plt.figure(figsize=(8, 4))
ratings_per_user.hist(bins=10, color='mediumseagreen', edgecolor='black')
plt.title("Phân phố số rating theo user")
plt.xlabel("Số lượt rating")
plt.ylabel("Số user")
plt.tight_layout()
plt.savefig("hist_rating_per_user.png", dpi=150)
plt.show()
print("Đã Lưu: hist_rating_per_user.png")

print()
print(" Hoàn thành thống kê!")
