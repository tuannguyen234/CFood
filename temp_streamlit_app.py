import streamlit as st
from streamlit_autorefresh import st_autorefresh
from streamlit_cookies_manager import EncryptedCookieManager
import sqlite3
import google.generativeai as genai
from streamlit_option_menu import option_menu
import hashlib
import os
import time
from PIL import Image
import base64
import warnings
import logging
import mimetypes

# Ẩn cảnh báo Streamlit
# Ẩn cảnh báo của Streamlit
st.set_option('client.showErrorDetails', False)  # ✅ Ẩn lỗi chi tiết

# Giảm log lỗi Streamlit
logging.getLogger("streamlit").setLevel(logging.ERROR)

warnings.filterwarnings("ignore")




#--------setuptitle and logo--------------
st.set_page_config(
    page_title="CFood",
    page_icon="D:\code\CFood\CFood_logo.png",  # Favicon emoji
    layout="centered",  # Page layout option
)


# Load CSS từ file
def load_css():
    with open("style.css", "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Gọi hàm load CSS
load_css()

# Hiển thị tiêu đề CFood với hiệu ứng đổi màu
st.markdown('<h1 class="color-changing-text">CFood - Social Platform</h1>', unsafe_allow_html=True)
#st.image("D:\code\CFood\CFood_logo.png", use_container_width=True)
import os
import base64
import streamlit as st
from streamlit.components.v1 import html

# Đường dẫn thư mục chứa ảnh
image_folder = r"D:\code\CFood\main_images"

# Lấy danh sách ảnh trong thư mục
images = [f for f in os.listdir(image_folder) if f.endswith(('.jpg', '.jpeg', '.png'))]

# Tạo danh sách các ảnh được mã hóa base64
encoded_images = []
for image in images:
    path = os.path.join(image_folder, image)
    if not os.path.exists(path):
        st.error(f"File không tồn tại: {path}")
        continue
    try:
        with open(path, "rb") as img_file:
            encoded_string = base64.b64encode(img_file.read()).decode()
            encoded_images.append(encoded_string)
    except Exception as e:
        st.error(f"Lỗi khi xử lý hình ảnh: {e}")

# Tạo HTML và JavaScript cho slideshow
slideshow_html = f'''
<div id="slideshow-container" style="max-width: 100%; height: auto; margin: auto; text-align: center;">
    <img id="slideshow-image" src="data:image/png;base64,{encoded_images[0]}" 
         style="width: 100%; max-width: 500px; border-radius: 10px; border: 2px solid #e04f11; height: auto; object-fit: contain;">
</div>

<script>
let images = {encoded_images};
let currentIndex = 0;

function changeImage() {{
    document.getElementById("slideshow-image").src = "data:image/png;base64," + images[currentIndex];
    currentIndex = (currentIndex + 1) % images.length;
}}

setInterval(changeImage, 2000);
</script>
'''

html(slideshow_html, height=350)  # Điều chỉnh chiều cao nếu cần

# Thư mục chứa ảnh
image_folder = r"D:\code\CFood/main_images"  # Dùng `r""` để tránh lỗi escape character
products = [
    {"path": r"sub_images\\chaoo.webp", "name": "Chảo TL", "price": "391.000 VND", "link":"https://shopee.vn/product/470967085/6797560479?gads_t_sig=VTJGc2RHVmtYMTlxTFVSVVRrdENkUzJYdkg4SUFId3huV3BOemxRSlQvQ0FUR0VSelJHVndsR0VuQittNzZZWjU5MC9MeU5mUENFMUwvZHJBdnk5R1ZZd3dkVm43aHhES2NuZW5JWUVpWEtTWHBHN3hIWDVFK0RuR01HaFR4MWE&gad_source=1&gclid=Cj0KCQjw1um-BhDtARIsABjU5x4PR1NlnlxkhN5kyKR9wjjdYrBAaMZvcDMCexeSHxQXoOTR3tC3EiEaAmM4EALw_wcB"},
    {"path": r"sub_images\\dao_3.png", "name": "Bộ 3 Dao", "price": "600.000 VND","link":"https://daohoangtungdasy.com/bo-3-dao-chat-thai-loc-hoang-tung-da-sy?gad_source=1&gclid=Cj0KCQjw1um-BhDtARIsABjU5x5OJn6G9ZMcDzooxp3Z67uJaDMnNFtrIOPrcsamh5c2368KScHtP7AaAmLlEALw_wcB"},
    {"path": r"sub_images\\thớt.webp", "name": "Thớt Teak", "price": "235.000 VND","link":"https://giadungonline.vn/thot-chat-go-teak-dau-cay-kaiyo-ben-chac?variantId=135399513&gad_source=1&gclid=Cj0KCQjw1um-BhDtARIsABjU5x4FyzXi5eYLibXVHTDDRPLFjwSIwdGMi0wADeVAaqoFzmuA87tR3i8aAlj9EALw_wcB"},
]
# Tạo container chứa tất cả sản phẩm
container_html = '<div class="container">'
for product in products:
    # Kiểm tra xem file có tồn tại không
    if not os.path.exists(product["path"]):
        st.error(f"File không tồn tại: {product['path']}")
        continue
    try:
        # Đọc ảnh và mã hóa base64
        with open(product["path"], "rb") as img_file:
            encoded_string = base64.b64encode(img_file.read()).decode()
        # Thêm sản phẩm vào container
        container_html += (
            f'<div class="image-container-sub">'
            f'<a href="{product["link"]}" target="_blank">'  # Mở liên kết trong tab mới
            f'<img src="data:image/png;base64,{encoded_string}">'
            f'''<div class="text-container">{product['name']}</div>'''
            f'''<div class="price-container">Giá: {product['price']}</div>'''
            f'</div>'
        )
    except Exception as e:
        st.error(f"Lỗi khi xử lý hình ảnh: {e}")
# Đóng container
container_html += '</div>'
# Hiển thị container trong Streamlit
st.markdown(container_html, unsafe_allow_html=True)


#--------Model--------------

conn = sqlite3.connect('recipe_app.db')
conn.row_factory = sqlite3.Row

c = conn.cursor()

#--------hash_password--------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()
#--------hash_password--------------



# Create a directory to store uploaded images if it doesn't exist
if not os.path.exists('recipe_images'):
    os.makedirs('recipe_images')

def get_recipes():
    c.execute('''
        SELECT r.id, r.name, r.ingredients, r.instructions, r.image_path, u.username
        FROM recipes r
        JOIN users u ON r.user_id = u.id
    ''')
    # conn.close()
    return  c.fetchall()

#--------------------
def get_recipe_likes(recipe_id):
    c.execute('''
        SELECT COUNT(*) AS like_count
        FROM likes
        WHERE recipe_id = ?
    ''', (recipe_id,))
    result = c.fetchone()
    return result['like_count'] if result else 0
#--------------------
# Function to like a recipe
def like_recipe(user_id, recipe_id):
    # conn = get_db_connection()
    # c = conn.cursor()
    try:
        c.execute('INSERT INTO likes (user_id, recipe_id) VALUES (?, ?)', (user_id, recipe_id))
        conn.commit()
        st.success("Recipe liked successfully!")
    except sqlite3.IntegrityError:
        st.warning("You've already liked this recipe!")
        time.sleep(1)
    # finally:
    #     conn.close()

def add_comment(user_id, recipe_id, comment):
    # conn = get_db_connection()
    # c = conn.cursor()
    c.execute('INSERT INTO comments (user_id, recipe_id, comment) VALUES (?, ?, ?)', (user_id, recipe_id, comment))
    conn.commit()
    # conn.close()



# Function to get the user ID by username
def get_user_id(username):
    c.execute('SELECT id FROM users WHERE username = ?', (username,))
    return c.fetchone()[0]

# Function to submit a recipe (with image)
def submit_recipe(user_id, name, ingredients, instructions, image):
    image_path = None
    # conn = get_db_connection()
    # c = conn.cursor()
    if image is not None:
        image_path = os.path.join('recipe_images', image.name)
        with open(image_path, 'wb') as f:
            f.write(image.getbuffer())
    c.execute('INSERT INTO recipes (user_id, name, ingredients, instructions, image_path) VALUES (?, ?, ?, ?, ?)',
              (user_id, name, ingredients, instructions, image_path))
    conn.commit()

# ------------------User registration----------------------
# Function to register a new user
def register_user(email, username, password):
    # conn = get_db_connection()
    # c = conn.cursor()
    hashed_pw = hash_password(password)
    try:
        c.execute('INSERT INTO users (email, username, password) VALUES (?, ?, ?)', (email ,username, hashed_pw))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False


# Hàm kiểm tra email đã tồn tại chưa
def email_exists(email):
    conn = sqlite3.connect("recipe_app.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email = ?", (email,))
    result = c.fetchone()
    conn.close()
    return result is not None


def register():
    st.title(':green[Register]')
    email = st.text_input(':orange[Email]', placeholder='Enter Your Email')
    username = st.text_input(':orange[Username]', placeholder='Enter Your Username')
    password1 = st.text_input(':orange[Password]', placeholder='Enter Your Password', type='password')
    password2 = st.text_input(':orange[Confirm Password]', placeholder='Confirm Your Password', type='password')
    if st.button("Register"):
        if register_user(email, username, password1):
            st.success("Registration successful! You can now log in.")
        else:
            st.error("Username already exists.")


# ------------------User registration----------------------


# -----------User login-------------
def login_user(username, password):
    hashed_pw = hash_password(password)
    c.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, hashed_pw))
    return c.fetchone()
# Kiểm tra trạng thái đăng nhập
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

cookies = EncryptedCookieManager(password = 'tuan')

# Nếu không có quyền truy cập cookies, yêu cầu cấp phép
if not cookies.ready():
    st.stop()

def login():
    st.title(":green[Login]")
    username = st.text_input(':orange[Username]', placeholder='Enter Your Username')
    password = st.text_input(':orange[Password]', placeholder='Enter Your Password', type='password')

    if st.button("Login"):
        user = login_user(username, password)
        if user:
            st.success(f"Welcome, {username}!")
            st.session_state.user_id = user[0]
            st.session_state.username = username
            st.session_state.logged_in = True
            cookies['logged_in'] = 'True'
            cookies['user_id'] = str(user[0])
            cookies['username'] = username
            cookies.save()
            time.sleep(1)
            st.rerun()
        else:
            st.error("Invalid username or password.")

# -----------User login-------------


# -----------Logout function---------------
def logout():
    cookies.pop("logged_in", None)
    cookies.save()
    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.username = None
    st.success("You have been logged out.")
    st.rerun()
# -----------Logout function---------------



if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.username = None

# Login/Register navigation
def navigation():
    if 'logged_in' not in cookies:
        selected = option_menu(
            menu_title="",
            options=["Login", "Register"],
            icons=['box-arrow-in-right', 'person-plus-fill'],
            menu_icon="cast",
            default_index=0,
            orientation='horizontal')
        if selected == "Login":
            login()
        if selected == "Register":
            register()

def main():
      # Navigation
    selected = option_menu(
          menu_title="",
          options=["Chat Bot", "Feed News", "Recipes Up"],
          icons=['robot', 'newspaper', 'person-fill'],
          menu_icon="cast",
          default_index=1,
          orientation='horizontal',
          styles={
        "container": {"padding": "0!important", "background-color": "#FF6600"},
        "icon": {"color": "black", "font-size": "18px"},
        "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px"},
        "nav-link-selected": {"background-color": "#0066FF", "color": "white"},  # Active option color
    }
      )

    if selected == "Chat Bot":
        st.session_state.page = "chatbot"
    elif selected == "Feed News":
        st.session_state.page = "home"
    elif selected == "Recipes Up":
        st.session_state.page = "submit"

    # Home Page (Feed News)
    if st.session_state.page == "home":
        st.write("### Shared Recipes:")
        recipes = get_recipes()
        if recipes:
            for recipe in reversed(recipes):
                recipe_id = recipe['id']
                st.write(f"**Name:** **{recipe['name']}** (by {recipe['username']})")
                st.write(f"**Ingredients:** {recipe['ingredients']}")
                st.write(f"**Instructions:** {recipe['instructions']}")
                if recipe['image_path']:  # If an image was uploaded
                    st.image(recipe['image_path'], caption=recipe['name'], use_container_width=True)

                # Like button
                    # Display the current number of likes
                like_count = get_recipe_likes(recipe_id)
                st.write(f"Likes: {like_count}")

                #user_id = st.session_state.user_id
                user_id = cookies['user_id']  # Assuming user_id is stored in session state
                if st.button(f"👍", key=f"like_{recipe_id}"):
                    like_recipe(user_id, recipe_id)
                    st.rerun()

                # Button to show/hide comments
                if 'show_comments' not in st.session_state:
                    st.session_state.show_comments = {}

                toggle_key = f"toggle_{recipe_id}"
                if toggle_key not in st.session_state.show_comments:
                    st.session_state.show_comments[toggle_key] = False

                if st.button("Show/Hide Comments", key=f"toggle_{recipe_id}"):
                    st.session_state.show_comments[toggle_key] = not st.session_state.show_comments[toggle_key]

                # Display comments if toggled
                if st.session_state.show_comments[toggle_key]:
                    c.execute('SELECT comment, u.username FROM comments c JOIN users u ON c.user_id = u.id WHERE c.recipe_id = ?', (recipe_id,))
                    comments = c.fetchall()

                    if comments:
                        st.write("### Comments:")
                        for comment in comments:
                            st.write(f"**{comment['username']}:** {comment['comment']}")
                    else:
                        st.write("No comments yet.")

                    # Add comment
                    comment_text = st.text_input(f"Add a comment", key=f"comment_input_{recipe_id}")
                    # if st.button(f"Submit", key =  f'submit_comment{recipe_id}'):
                    if st.button(f"Submit",key = f'submit_comment{recipe_id}'):
                        if comment_text:
                            add_comment(user_id, recipe_id, comment_text)
                            st.success("Comment added!")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.warning("Please enter a comment.")
                st.write("---")
        else:
            st.write("No recipes available yet!")
        warnings.filterwarnings("ignore")

    # Submit Recipe Page
    elif st.session_state.page == "submit":
        navigation()
        if 'logged_in' in cookies:
            if "camera_open_up" not in st.session_state:
                st.session_state.camera_open_up = False
            if "camera_image_up" not in st.session_state:
                st.session_state.camera_image_up = None
            with st.form("recipe_form"):
                recipe_name = st.text_input("Recipe Name")
                ingredients = st.text_area("Ingredients")
                instructions = st.text_area("Instructions")
                recipe_image = st.file_uploader("Upload an Image", type=["png", "jpg", "jpeg",'jfif'])
                col1, col2 = st.columns([1,1])
                with col1:
                    if st.form_submit_button("📸 Mở Camera"):
                        st.session_state.camera_open_up = True 
                with col2:
                    if st.session_state.camera_open_up and st.form_submit_button("🔻 Đóng Camera"):
                        st.session_state.camera_open_up = False 
                        st.rerun()  



                camera_image_up = None
                if st.session_state.camera_open_up:
                    camera_image_up = st.camera_input("Chụp ảnh")
                    if camera_image_up:
                        st.session_state.camera_image_up=camera_image_up
                
                submitted_up = st.form_submit_button("✅ Lên món")
                cookies.save()
                if submitted_up:
                    warnings.filterwarnings("ignore")
                    if camera_image_up:
                        submit_recipe(cookies['user_id'], recipe_name, ingredients, instructions, camera_image_up)
                        st.success(f"Recipe '{recipe_name}' submitted successfully! 🎉")
                        warnings.filterwarnings("ignore")
                    else:

                        submit_recipe(cookies['user_id'], recipe_name, ingredients, instructions, recipe_image)
                        st.success(f"Recipe '{recipe_name}' submitted successfully!")
                        warnings.filterwarnings("ignore")

    # ChatBot Page
    elif st.session_state.page == "chatbot":
        #--------Model--------------
        st.markdown(
    """

    <h1>
        <span class="fire-emoji">🔥</span> 
        <span class="fire-text"></span> 
        <span class="knife-emoji"> 🔪</span>
    </h1>
    """,
    unsafe_allow_html=True
)



        USER_AVATAR = "👤"
        BOT_AVATAR = "🤖"


                # Lưu trạng thái bật/tắt camera
        if "camera_open" not in st.session_state:
            st.session_state.camera_open = False

        # Display the chatbot's title on the page
        # Chatbot response using Google Gemini
        def get_gemini_model():
            genai.configure(api_key='AIzaSyC60YzCQ4IndhZd2_qdVn5a1dzUzZ56kxI')
            model = genai.GenerativeModel('gemini-2.0-flash')
            # response = model.generate_content(question)
            return model

        def translate_role_for_streamlit(user_role):
            if user_role == "model":
                return "assistant"
            else:
                return user_role


        # Initialize chat session in Streamlit if not already present
        if "chat_session" not in st.session_state:
            st.session_state.chat_session = get_gemini_model().start_chat(history=[])

        def get_avatar_for_role(role):
            return USER_AVATAR if role == 'user' else BOT_AVATAR


        uploaded_image = st.file_uploader("Upload", type=["png", "jpg", "jpeg"])


        col1, col2 = st.columns([1,1])
        with col1:
            if st.button("📸 Á"):
                st.session_state.camera_open = True  # Khi bấm, camera mới mở
        with col2:
            if st.session_state.camera_open and st.button("🔻 Đóng Camera"):
                st.session_state.camera_open = False  # Khi bấm, camera sẽ tắt
                st.rerun()  # Refresh lại giao diện để ẩn camera



        camera_image = None
        if st.session_state.camera_open:
            camera_image = st.camera_input("Chụp ảnh")
        # Hiển thị ảnh đã tải lên hoặc chụp từ camera
        if uploaded_image:
            st.image(uploaded_image, caption="📷 Ảnh đã tải lên", use_container_width=True)
        elif camera_image:
            st.image(camera_image, caption="📸 Ảnh chụp từ camera", use_container_width=True)

        user_prompt = st.text_input('',placeholder="Rất vui được phục vụ bạn..... 😊")

        col1, col2 = st.columns([1,1])

        with col1:
            submit_button = st.button("Gửi ✅")  
        with col2:
            delete_button = st.button("Xóa 🗑️")
        if submit_button:
            image_input = None
            if uploaded_image:
                image_input = Image.open(uploaded_image)
            elif camera_image:
                image_input = Image.open(camera_image)

                # Prompt mặc định (không được in ra lịch sử chat)
            default_prompt = ''''
            Bạn là một đầu bếp chuyên nghiệp có thể gợi ý các món ăn từ nguyên liệu mà người dùng đưa vào, bao gồm cả ảnh và văn bản.  
Hãy đề xuất công thức chi tiết, bao gồm các bước chế biến và cách nấu món ăn.  

🔥 **Lưu ý quan trọng:**  
- Luôn đề xuất các dụng cụ nhà bếp phù hợp với từng công thức nấu ăn.  
- Kèm theo **link sản phẩm tài trợ** theo danh sách sau:  
  - **Chảo**: [Link](https://shopee.vn/product/470967085/6797560479?gads_t_sig=VTJGc2RHVmtYMTlxTFVSVVRrdENkUzJYdkg4SUFId3huV3BOemxRSlQvQ0FUR0VSelJHVndsR0VuQittNzZZWjU5MC9MeU5mUENFMUwvZHJBdnk5R1ZZd3dkVm43aHhES2NuZW5JWUVpWEtTWHBHN3hIWDVFK0RuR01HaFR4MWE&gad_source=1&gclid=Cj0KCQjw1um-BhDtARIsABjU5x4PR1NlnlxkhN5kyKR9wjjdYrBAaMZvcDMCexeSHxQXoOTR3tC3EiEaAmM4EALw_wcB)  
  - **Dao**: [Link](https://daohoangtungdasy.com/bo-3-dao-chat-thai-loc-hoang-tung-da-sy?gad_source=1&gclid=Cj0KCQjw1um-BhDtARIsABjU5x5OJn6G9ZMcDzooxp3Z67uJaDMnNFtrIOPrcsamh5c2368KScHtP7AaAmLlEALw_wcB)  
  - **Thớt**: [Link](https://giadungonline.vn/thot-chat-go-teak-dau-cay-kaiyo-ben-chac?variantId=135399513&gad_source=1&gclid=Cj0KCQjw1um-BhDtARIsABjU5x4FyzXi5eYLibXVHTDDRPLFjwSIwdGMi0wADeVAaqoFzmuA87tR3i8aAlj9EALw_wcB)  
            '''
            
                        # Kết hợp prompt mặc định với prompt của người dùng (nếu có)
            if user_prompt:
                full_prompt = f"{default_prompt} {user_prompt}"
            else:
                full_prompt = default_prompt
            if image_input:
                gemini_response = st.session_state.chat_session.send_message(
                     [full_prompt, image_input]
                 )
                 
            else:
            # Nếu không có hình ảnh, chỉ gửi văn bản
                gemini_response = st.session_state.chat_session.send_message(full_prompt)



            # Lưu phản hồi vào lịch sử chat
            if "chat_history" not in st.session_state:
                st.session_state.chat_history = []
                # Lưu phản hồi từ chatbot
            st.session_state.chat_history.append(("assistant", gemini_response.text))
                # Lưu prompt của người dùng (nếu có)
            if user_prompt:
                st.session_state.chat_history.append(("user", user_prompt))
                # Hiển thị lịch sử chat
            for role, message in reversed(st.session_state.chat_history):
                if role == "user":
                    with st.chat_message("user", avatar=USER_AVATAR):
                        st.markdown(message)
                elif role == "assistant":
                    with st.chat_message("assistant", avatar=BOT_AVATAR):
                        st.markdown(message)

        if delete_button:
            st.session_state.chat_session.history.clear()
            st.session_state.chat_history = []
            st.success("Chat history cleared!")
            st.success('Delete Successfully !')
            st.rerun()
        # st.rerun()


main()
warnings.filterwarnings("ignore")
if st.sidebar.button("Logout"):

    logout()
#navigation()
if st.session_state.logged_in or 'logged_in' in cookies and 5==2:

    st.sidebar.write(f"Logged in as: {cookies['username']}")

    st.session_state.page = 'submit'
    main()
    if st.sidebar.button("Logout"):
        logout()



