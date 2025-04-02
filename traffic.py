import streamlit as st
import pandas as pd
import random
import plotly.express as px
from datetime import datetime, timedelta
link_URL = 'https://b6bb-42-114-213-202.ngrok-free.app/'
# Ngày bắt đầu (10/03/2025)
START_DATE = datetime(2025, 3, 10, 0, 0) 

# Ngày hiện tại (thời gian thực)
TODAY = datetime.now()
TODAY = TODAY - timedelta(days=2)  # 1 ngày trước

# Khởi tạo session state để lưu dữ liệu truy cập
if "visits" not in st.session_state:
    st.session_state.visits = pd.DataFrame(columns=["timestamp", "visits"])

# Khởi tạo thời gian hiện tại nếu chưa có
if "current_time" not in st.session_state:
    st.session_state.current_time = START_DATE

# Hàm tạo dữ liệu truy cập ngẫu nhiên
def generate_traffic():
    if st.session_state.current_time >= TODAY:
        st.warning("⏳ Đã đến thời gian hiện tại, không thể tạo thêm dữ liệu!")
        return  # Không tạo dữ liệu quá thời gian hiện tại

    nuvisits = random.randint(10, 200)  
    time_increment = timedelta(hours=5)  
    st.session_state.current_time += time_increment

    if st.session_state.current_time > TODAY:
        st.session_state.current_time = TODAY

    new_data = pd.DataFrame({
        "timestamp": [st.session_state.current_time],
        "visits": [nuvisits]
    })
    st.session_state.visits = pd.concat([st.session_state.visits, new_data], ignore_index=True)

# Giao diện ứng dụng
st.title("📊 Web Traffic Analytics")

# Nút thêm dữ liệu
if st.button("Thêm dữ liệu truy cập 🔄"):
    generate_traffic()

# Hiển thị dữ liệu truy cậ
st.write("### 🗂️ Dữ liệu truy cập theo từng mốc 5 tiếng:")
st.dataframe(st.session_state.visits.sort_values(by="timestamp"))

# Tạo mảng thời gian liên tục từ 10/03/2025 đến hôm nay với khoảng cách 5 tiếng
time_range = pd.date_range(start=START_DATE, end=TODAY, freq="5H")

# Đảm bảo dữ liệu không bị thiếu thời gian
if not st.session_state.visits.empty:
    visits_by_time = st.session_state.visits.set_index("timestamp").resample("5H").sum().reset_index()
    visits_by_time = visits_by_time.set_index("timestamp").reindex(time_range, fill_value=0).reset_index()
    visits_by_time.columns = ["timestamp", "visits"]

    # Vẽ biểu đồ với Plotly
    fig = px.line(
        visits_by_time, 
        x="timestamp", 
        y="visits", 
        title="📈 Biểu đồ số lượng truy cập (cập nhật mỗi 5 tiếng)", 
        markers=True, 
        line_shape="linear"
    )

    # Cố định trục Y từ 0 - 200
    fig.update_yaxes(range=[0, 200])

    # Hiển thị biểu đồ trong Streamlit
    st.plotly_chart(fig, use_container_width=True)

    # Thông báo trục Y cố định
    st.write("⚠️ **Lưu ý:** Trục Y được cố định từ **0 đến 200**.")
