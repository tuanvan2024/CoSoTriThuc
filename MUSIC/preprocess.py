import pandas as pd
# BƯỚC 2 – LỌC DỮ LIỆU (Filter user & item)
df = pd.read_csv("ratings_full.csv")
print("=" * 50)
print("Lọc dữ liệu - MUSIC")
print("=" * 50)
print(f"Trước lọc: {len(df)} dong | "
      f"{df['user_id'].nunique()} users | "
      f"{df['song_title'].nunique()} bai hat")
print()

# Ngưỡng lọc
MIN_USER_RATINGS = 5  
MIN_SONG_RATINGS = 2   

# Lọc user ít hoạt động
user_counts = df.groupby('user_id')['rating'].count()
valid_users = user_counts[user_counts >= MIN_USER_RATINGS].index
print(f"Users co >= {MIN_USER_RATINGS} rating: {len(valid_users)} / {df['user_id'].nunique()}")

# Lọc bài hát ít rating
song_counts = df.groupby('song_title')['rating'].count()
valid_songs = song_counts[song_counts >= MIN_SONG_RATINGS].index
print(f"Bài hát có >= {MIN_SONG_RATINGS} rating: {len(valid_songs)} / {df['song_title'].nunique()}")

# Áp dụng lọc
df_filtered = df[
    df['user_id'].isin(valid_users) &
    df['song_title'].isin(valid_songs)
].reset_index(drop=True)

print()
print(f"Sau lọc : {len(df_filtered)} dong | "
      f"{df_filtered['user_id'].nunique()} users | "
      f"{df_filtered['song_title'].nunique()} bai hat")
print(f"Tỉ lệ giữ lại: {len(df_filtered)/len(df)*100:.1f}%")

# Lưu file đã lọc
df_filtered.to_csv("ratings_filtered.csv", index=False)
print()
print("Đã lưu: ratings_filtered.csv")
print(" Hoàn thành bước lọc dữ liệu!")
