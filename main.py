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

# 1. Load dữ liệu từ file của Tuấn
try:
    df = pd.read_csv('artists.csv')
    df['artistID'] = df['artistID'].astype(int)
except Exception as e:
    print(f"Lỗi: Không tìm thấy file artists.csv! {e}")


try:
    _, model = dump.load('music_model.pkl')
    print("Hệ thống: Đã nạp mô hình AI (music_model.pkl) thành công!")
except Exception as e:
    model = None
    print(f"Cảnh báo: Chưa có file mô hình. Hãy chạy train_model.py trước! {e}")



# Chức năng 1 & 2:Lấy toàn bộ danh sách bài hát
@app.get("/all-songs")
def get_all_songs():
    return df.to_dict(orient='records')

# Chức năng 6:Dự đoán rating cho cặp (User, Song)
@app.get("/predict")
def predict_rating(user_id: int, song_title: str):
    keyword = song_title.lower().strip()
    match = df[df['song_title'].str.lower().str.contains(keyword, case=False, na=False)]
    
    if match.empty:
        return {"error": f"Không tìm thấy bài hát '{song_title}'!"}
    
    #  Thêm kiểm tra model trước khi dùng
    if model is None:
        return {"error": "HT chưa được load! Hãy chạy train_model.py trước."}
    
    song = match.iloc[0]
    song_id = int(song['artistID'])
    full_title = song['song_title']
    prediction = model.predict(uid=user_id, iid=song_id)
    
    return {
        "song_title": full_title,
        "predicted_rating": round(prediction.est, 2)
    }
    

# Chức năng 5: Gợi ý Top-N bài hát cá nhân hóa cho một User
@app.get("/recommendations/{user_id}")
def get_recommendations(user_id: int, n: int = 10):
    all_song_ids = df['artistID'].unique()
    
    predictions = []
    
    if model:
        for s_id in all_song_ids:
            est = model.predict(uid=user_id, iid=int(s_id)).est
            predictions.append((s_id, est))
    else:
        for s_id in all_song_ids:
            score = 3.0 + ((user_id * int(s_id)) % 20) / 10.0
            predictions.append((s_id, score))
    predictions.sort(key=lambda x: x[1], reverse=True)
    
    # 4. Lấy ra N bài hát đứng đầu (Top-N)
    top_n_ids = [x[0] for x in predictions[:n]]
    
    top_songs = []
    for s_id in top_n_ids:
        song_info = df[df['artistID'] == s_id].iloc[0].to_dict()
        # Gán thêm điểm dự đoán vào để hiển thị lên giao diện
        song_info['predicted_rating'] = round(next(x[1] for x in predictions if x[0] == s_id), 2)
        top_songs.append(song_info)
        
    return top_songs

# Chức năng 4:Gợi ý bài hát tương tự cùng thể loại
@app.get("/similar/{song_id}")
def get_similar_songs(song_id: int):
    try:
        target_song = df[df['artistID'] == song_id].iloc[0]
        genre = target_song['genre']
        similar = df[(df['genre'] == genre) & (df['artistID'] != song_id)]
    
        return similar.sample(n=min(len(similar), 4)).to_dict(orient='records')
    except:
        return []