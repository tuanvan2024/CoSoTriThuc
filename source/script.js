let allSongs = [];
const apiBase = "http://127.0.0.1:8000";

//  Chức năng 1
async function init() {
    try {
        const res = await fetch(`${apiBase}/all-songs`);
        allSongs = await res.json();
        document.getElementById('musicGrid').innerHTML = '<p style="text-align:center; color:#999; grid-column: 1/-1;">Vui lòng chọn thể loại để khám phá âm nhạc.</p>';
    } catch (err) {
        console.error("Lỗi:", err);
    }
}

document.getElementById('userSelect').onchange = (e) => {
    const selectedId = e.target.value;
    
    const predictRes = document.getElementById('predictResult');
    if(predictRes) predictRes.innerHTML = ''; 
    
    const predictInp = document.getElementById('predictInput');
    if(predictInp) predictInp.value = '';
    const grid = document.getElementById('musicGrid');
    if(grid) {
        grid.innerHTML = `<p style="grid-column: 1/-1; text-align: center; color: #999;">
            Đã chuyển sang tài khoản ${selectedId}. Vui lòng chọn thể loại  để xem kết quả mới.
        </p>`;
    }

    const modalBody = document.getElementById('modalBody');
    if(modalBody) modalBody.innerHTML = '';
    document.getElementById('detailModal').style.display = "none";

    const viewTitle = document.getElementById('viewTitle');
    if(viewTitle) viewTitle.innerText = "Khám phá bài hát";
    const avatar = document.querySelector('.avatar');
    if(avatar) {
        avatar.src = `https://ui-avatars.com/api/?name=U${selectedId}&background=random`;
    }
    
    console.log(`Đã reset giao diện cho User #${selectedId}`);
};



function filterByGenre(genre) {
    const buttons = document.querySelectorAll('.btn-tag');
    buttons.forEach(btn => {
        if(btn.innerText === (genre === 'All' ? 'Tất cả' : genre)) btn.classList.add('active');
        else btn.classList.remove('active');
    });

    let filteredData = [];
    if (genre === 'All') {
        filteredData = allSongs; 
    } else {
        filteredData = allSongs.filter(s => s.genre === genre); 
    }

    document.getElementById('viewTitle').innerText = genre === 'All' ? "Tất cả bài hát" : `Thể loại: ${genre}`;
    render(filteredData.slice(0, 10));
}

document.getElementById('btnExplore').onclick = () => {
    document.getElementById('musicGrid').scrollIntoView({ behavior: 'smooth' });
    filterByGenre('All'); 
};


function render(data) {
    const grid = document.getElementById('musicGrid');
    if (!grid) return;

    grid.innerHTML = data.map(s => {
        const char = s.song_title ? s.song_title[0] : '?';
        const color = ["#3498db", "#e74c3c", "#9b59b6", "#f1c40f", "#1abc9c"][s.artistID % 5];
        
        return `
            <div class="song" onclick="showDetail(${s.artistID})">
                ${s.predicted_rating ? `<div class="badge">${s.predicted_rating} ⭐</div>` : ''}
                <div class="song-thumb" style="background: ${color}; color: white;">${char}</div>
                <div style="font-weight:600; margin-top:10px">${s.song_title}</div>
                <div style="font-size:13px; color:#666">${s.name}</div>
                <div style="font-size:11px; color:#c81e1e; margin-top:5px">${s.genre}</div>
            </div>
        `;
    }).join('');
}

document.getElementById('btnExplore').onclick = () => {
    document.getElementById('musicGrid').scrollIntoView({ behavior: 'smooth' });
    init();
    document.getElementById('viewTitle').innerText = "Khám phá bài hát mới";
};

//  CHỨC NĂNG 2: TÌM KIẾM 
document.getElementById('searchInput').oninput = (e) => {
    const key = e.target.value.toLowerCase().trim();
    
    // Lọc trực tiếp trên mảng allSongs
    const filtered = allSongs.filter(s => 
        s.song_title.toLowerCase().includes(key) || 
        s.name.toLowerCase().includes(key)
    );

    document.getElementById('viewTitle').innerText = key ? `Tìm thấy ${filtered.length} kết quả` : "Khám phá bài hát";
    render(filtered.slice(0, 10));
};

// Hàm thực hiện Chức năng 5: Top-N Recommendation
async function getTopN() {
    // 1. Lấy User ID đang được chọn từ dropdown
    const userId = document.getElementById('userSelect').value;
    const viewTitle = document.getElementById('viewTitle');
    const grid = document.getElementById('musicGrid');

    viewTitle.innerText = `Đang tính toán gợi ý cho tài khoản ${userId}...`;
    grid.innerHTML = '<div style="grid-column: 1/-1; text-align: center;">đang phân tích sở thích của bạn...</div>';

    try {
        const response = await fetch(`${apiBase}/recommendations/${userId}?n=10`);
        const topSongs = await response.json();

   
        viewTitle.innerText = `Top 10 bài hát phù hợp nhất với tài khoản ${userId}`;
        
        render(topSongs);
        
        grid.scrollIntoView({ behavior: 'smooth', block: 'center' });
        
    } catch (error) {
        console.error("Lỗi khi lấy gợi ý:", error);
        viewTitle.innerText = "Không thể kết nối với hệ thống ";
    }
}

document.getElementById('btnTopN').onclick = getTopN;

const btnHeroSuggest = document.querySelector('.btn-outline');
if(btnHeroSuggest) btnHeroSuggest.onclick = getTopN;

// CHỨC NĂNG 6: DỰ ĐOÁN RATING 
document.getElementById('btnPredict').onclick = async () => {
    const user = document.getElementById('userSelect').value;
    const title = document.getElementById('predictInput').value.trim();
    const resDiv = document.getElementById('predictResult');

    if (!title) {
        resDiv.innerHTML = `<span style="color:orange;">Vui lòng nhập tên bài hát!</span>`;
        return;
    }

    resDiv.innerHTML = `<span style="color:#999;">Đang dự đoán...</span>`;

    try {
        const res = await fetch(`${apiBase}/predict?user_id=${user}&song_title=${encodeURIComponent(title)}`);
        const data = await res.json();

        if (data.error) {
            resDiv.innerHTML = `<span style="color:red;"> ${data.error}</span>`;
        } else {
            resDiv.innerHTML = `Hệ thống dự đoán <b>Tài khoản ${user}</b> sẽ chấm bài <b>${data.song_title}</b> là: <b style="color:green; font-size:18px;">${data.predicted_rating} ⭐</b>`;
        }
    } catch (err) {
        resDiv.innerHTML = `<span style="color:red;"> Lỗi kết nối Server!</span>`;
    }
};

// --- CHỨC NĂNG 3 & 4: 
async function showDetail(id) {
    const song = allSongs.find(s => s.artistID == id);
    const res = await fetch(`${apiBase}/similar/${id}`);
    const similar = await res.json();

    const body = document.getElementById('modalBody');
    body.innerHTML = `
        <div style="display: flex; flex-direction: column; align-items: center; text-align: center; margin-bottom: 25px;">
            <div style="width: 100px; height: 100px; background: #f0f0f0; border-radius: 15px; display: flex; align-items: center; justify-content: center; font-size: 50px; margin-bottom: 20px; box-shadow: 0 4px 10px rgba(0,0,0,0.05);">
                ${song.song_title[0]}
            </div>
            <div>
                <h2 style="margin: 0 0 10px 0; font-size: 28px;">${song.song_title}</h2>
                <p style="margin: 5px 0; font-size: 16px;">Ca sĩ: <b>${song.name}</b> | Thể loại: <b>${song.genre}</b></p>
                <p style="font-size: 14px; color: #777; max-width: 400px; margin: 10px auto 0;">
                    Mô tả: Đây là một bản nhạc đầy cảm xúc, mã số lưu trữ ${song.artistID}.
                </p>
            </div>
        </div>
        <hr style="border: 0; border-top: 1px solid #eee;">
        <div style="text-align: center; margin-top: 25px;">
            <h4 style="margin-bottom: 20px;">Bài hát tương tự cùng dòng ${song.genre}</h4>
            <div style="display: flex; justify-content: center; flex-wrap: wrap; gap: 15px;">
                ${similar.map(s => `
                    <div class="song" style="box-shadow: none; border: 1px solid #eee; width: 180px; text-align: center; cursor: pointer;" onclick="showDetail(${s.artistID})">
                        <div style="font-weight: 600; font-size: 14px; margin-bottom: 5px;">${s.song_title}</div>
                        <div style="font-size: 12px; color: #888;">${s.name}</div>
                    </div>
                `).join('')}
            </div>
        </div>
    `;

    document.getElementById('detailModal').style.display = "block";
}
document.querySelector('.close-modal').onclick = () => {
    document.getElementById('detailModal').style.display = "none";
};

window.onclick = (e) => {
    if (e.target.id === 'detailModal') document.getElementById('detailModal').style.display = "none";
};


init();