import streamlit as st
import google.generativeai as genai
from PIL import Image
from streamlit_mic_recorder import mic_recorder
import os

# --- الحل الجذري لمشكلة الـ 404 ---
# بنجبر المكتبة تستخدم النسخة المستقرة v1 بدل v1beta اللي بتعمل Error
os.environ["GOOGLE_GENERATIVE_AI_NETWORK_ENDPOINT"] = "generativelanguage.googleapis.com"

# حط الـ API Key بتاعك هنا
MY_API_KEY = "AIzaSyCOdFVcx0W2pdlfh5uDTq-v5DN2zD2ZfWU" 

genai.configure(api_key=MY_API_KEY)

# استخدام دالة اختيار الموديل مع تحديد الإصدار
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    generation_config={"temperature": 0.7}
)

# --- الواجهة (نفس الشكل اللي بتحبه) ---
st.set_page_config(page_title="X ASSISTANT v2", layout="wide")
st.markdown("<h1 style='text-align:center; color:#00f2fe;'>⚡ X ASSISTANT v2</h1>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض المحادثة
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# القائمة الجانبية (صور وصوت)
with st.sidebar:
    st.title("⚙️ الإعدادات")
    img_file = st.file_uploader("📸 ارفع صورة", type=["jpg", "png", "jpeg"])
    st.write("🎤 سجل صوتك:")
    audio = mic_recorder(start_prompt="بدء التسجيل", stop_prompt="إرسال", key='mic')

# معالجة المدخلات
if prompt := st.chat_input("اسألني أي حاجة يا Harreef..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # هنا بنبعث الطلب للموديل
            if img_file:
                img = Image.open(img_file)
                response = model.generate_content([prompt, img])
            else:
                response = model.generate_content(prompt)
            
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            # لو حصل 404 تاني، الكود ده هيعرضلك الموديلات المتاحة فعلاً عندك
            st.error("السيرفر لسه معاند!")
            st.write("الموديلات اللي السيرفر شايفها هي:")
            models = [m.name for m in genai.list_models()]
            st.write(models)
                                      
