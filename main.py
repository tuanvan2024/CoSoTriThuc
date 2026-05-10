import pandas as pd
from surprise import dump
import random
from fastapi import FastAPI
import fastapi.middleware.cors

app = FastAPI()
app.add_middleware(
    fastapi.middleware.cors.CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mapping 4 user demo ứng với 4 thành viên nhóm
DEMO_USERS = {
    1: {"label": "VHT",  "name": "Vũ Hữu Tuấn"},
    2: {"label": "DDQT", "name": "Dư Đỗ Quỳnh Trang"},
    3: {"label": "NVL",  "name": "Lê Văn Lợi"},
    4: {"label": "NTH",  "name": "Nguyễn Trung Hiếu"},
}

# Load dữ liệu bài hát
try:
    df = pd.read_csv('artists.csv')
    df['artistID'] = df['artistID'].astype(int)
    print("Hệ thống: Đã nạp artists.csv thành công!")
except Exception as e:
    print(f"Lỗi: Không tìm thấy file artists.csv! {e}")
    df = pd.DataFrame()

# Load dữ liệu ratings đã lọc (dùng để biết bài nào user đã nghe)
try:
    df_ratings = pd.read_csv('ratings_filtered.csv')
    df_ratings['artistID'] = df_ratings['artistID'].astype(int)
    print("Hệ thống: Đã nạp ratings_filtered.csv thành công!")
except Exception as e:
    df_ratings = pd.DataFrame(columns=['user_id', 'artistID', 'rating', 'genre'])
    print(f"Cảnh báo: Không tìm thấy ratings_filtered.csv! {e}")

# Load mô hình AI
try:
    _, model = dump.load('music_model.pkl')
    print("Hệ thống: Đã nạp mô hình AI (music_model.pkl) thành công!")
except Exception as e:
    model = None
    print(f"Cảnh báo: Chưa có file mô hình. Hãy chạy train_model.py trước! {e}")


# ── Chức năng 1 & 2: Lấy toàn bộ danh sách bài hát 
@app.get("/all-songs")
def get_all_songs():
    return df.to_dict(orient='records')


#  Chức năng 6: Danh sách user demo kèm thông tin profile 
@app.get("/demo/users")
def get_demo_users():
    result = []
    for user_id, info in DEMO_USERS.items():
        if not df_ratings.empty:
            user_data = df_ratings[df_ratings['user_id'] == user_id]
            n_ratings  = len(user_data)
            avg_rating = round(user_data['rating'].mean(), 2) if n_ratings > 0 else 0.0
            top_genres = user_data['genre'].value_counts().head(2).index.tolist() if n_ratings > 0 else []
        else:
            n_ratings  = 0
            avg_rating = 0.0
            top_genres = []

        result.append({
            "user_id":    user_id,
            "label":      info["label"],
            "name":       info["name"],
            "n_ratings":  n_ratings,
            "avg_rating": avg_rating,
            "top_genres": top_genres,
        })
    return result


#  Chức năng 5: Gợi ý Top-N bài hát cá nhân hóa (chỉ bài CHƯA nghe) 
@app.get("/recommendations/{user_id}")
def get_recommendations(user_id: int, n: int = 10):
    # Lấy tập bài user đã rating → loại khỏi danh sách gợi ý
    if not df_ratings.empty:
        rated_items = set(df_ratings[df_ratings['user_id'] == user_id]['artistID'].tolist())
    else:
        rated_items = set()

    # Chỉ dự đoán trên bài CHƯA nghe
    candidate_ids = [s for s in df['artistID'].unique() if s not in rated_items]

    predictions = []
    if model:
        for s_id in candidate_ids:
            est = model.predict(uid=user_id, iid=int(s_id)).est
            predictions.append((s_id, est))
    else:
        for s_id in candidate_ids:
            score = 3.0 + ((user_id * int(s_id)) % 20) / 10.0
            predictions.append((s_id, score))

    predictions.sort(key=lambda x: x[1], reverse=True)

    # Lấy Top-N
    top_songs = []
    for s_id, est in predictions[:n]:
        song_info = df[df['artistID'] == s_id].iloc[0].to_dict()
        song_info['predicted_rating'] = round(est, 2)
        top_songs.append(song_info)

    return top_songs


# Chức năng 7: Dự đoán rating cho cặp (User, Song)
@app.get("/predict")
def predict_rating(user_id: int, song_title: str):
    keyword = song_title.lower().strip()
    match = df[df['song_title'].str.lower().str.contains(keyword, case=False, na=False)]

    if match.empty:
        return {"error": f"Không tìm thấy bài hát '{song_title}'!"}

    if model is None:
        return {"error": "Mô hình chưa được load! Hãy chạy train_model.py trước."}

    song      = match.iloc[0]
    song_id   = int(song['artistID'])
    full_title = song['song_title']
    prediction = model.predict(uid=user_id, iid=song_id)

    return {
        "song_title":       full_title,
        "predicted_rating": round(prediction.est, 2),
    }


#  Chức năng 4: Gợi ý bài hát tương tự cùng thể loại
@app.get("/similar/{song_id}")
def get_similar_songs(song_id: int):
    try:
        target_song = df[df['artistID'] == song_id].iloc[0]
        genre   = target_song['genre']
        similar = df[(df['genre'] == genre) & (df['artistID'] != song_id)]
        return similar.sample(n=min(len(similar), 4)).to_dict(orient='records')
    except Exception:
        return []
