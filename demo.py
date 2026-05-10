import pandas as pd
import joblib
# BƯỚC 7 – THỬ GỢI Ý CHO USER (DEMO)
print("=" * 50)
print("Demo gói Y bài hát - MUSIC ")
print("=" * 50)

# Load model và dữ liệu
artifact  = joblib.load("music_model.pkl")
model     = artifact["model"]
print(f"Đã nạp model! (RMSE val = {artifact['rmse_val']})")
print()

df = pd.read_csv("ratings_filtered.csv")
all_songs = df['song_title'].unique().tolist()


# Danh sách user demo

demo_users = df['user_id'].value_counts().head(5).index.tolist()
print("Danh sách  user demo (có nhiều rating nhất):")
for uid in demo_users:
    n   = len(df[df['user_id'] == uid])
    avg = df[df['user_id'] == uid]['rating'].mean()
    print(f"  User {uid:>3} — {n} ratings — avg: {avg:.2f} sao")
print()

# Gợi ý Top-10 cho 2 user đầu

TOP_N = 10

for user_id in demo_users[:2]:
    rated_songs = df[df['user_id'] == user_id]['song_title'].tolist()
    unrated     = [s for s in all_songs if s not in rated_songs]

    preds  = [(s, model.predict(user_id, s).est) for s in unrated]
    top_n  = sorted(preds, key=lambda x: x[1], reverse=True)[:TOP_N]

    print(f"Tốp {TOP_N} gợi ý cho User {user_id}:")
    for i, (song, score) in enumerate(top_n, 1):
        print(f"  {i:>2}. {song:<40} — dự đoán: {score:.2f} sao")
    print()


# Dự đoán rating cho 1 cặp (user, bài hát) cụ thể

print("Dự đoán rating cho 1 cặp(user, bài hát) ")
test_user = demo_users[0]
test_song = df['song_title'].iloc[0]
pred      = model.predict(test_user, test_song)
print(f"Hệ thống dự đoán  User {test_user} sẽ chấm '{test_song}' là: {pred.est:.2f} sao")
print()
print("=>Hoàn thành gói y!")
