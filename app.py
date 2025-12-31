import streamlit as st
import json
import os

# إعدادات الصفحة
st.set_page_config(layout="wide", page_title="Tournament Predictor")

# --- قاموس اللغات ---
texts = {
    "English": {
        "login_title": "🔐 Login",
        "user_label": "Enter your name:",
        "user_placeholder": "e.g. John Doe",
        "btn_user": "Login as User",
        "btn_admin": "Login as Admin",
        "admin_err": "Incorrect Admin Secret",
        "user_err": "Please enter your name",
        "logout": "Logout",
        "admin_dash": "📊 Admin Dashboard",
        "no_data": "No predictions recorded yet.",
        "user_pred": "Predictions for:",
        "save_btn": "✅ Save My Predictions",
        "save_success": "Saved successfully! Admin can now see it.",
        "champ_label": "CHAMPION",
        "r16": "Round of 16",
        "qf": "Quarter Finals",
        "sf": "Semi-Finals",
        "final": "🏆 THE FINAL",
        "lang_label": "Choose Language / اختر اللغة"
    },
    "العربية": {
        "login_title": "🔐 تسجيل الدخول",
        "user_label": "أدخل اسمك:",
        "user_placeholder": "مثال: أحمد محمد",
        "btn_user": "دخول كمستخدم",
        "btn_admin": "دخول كمسؤول (Admin)",
        "admin_err": "كلمة سر الأدمن غير صحيحة",
        "user_err": "يرجى إدخال الاسم أولاً",
        "logout": "تسجيل الخروج",
        "admin_dash": "📊 لوحة تحكم الإدارة",
        "no_data": "لا يوجد توقعات مسجلة بعد.",
        "user_pred": "توقعات المستخدم:",
        "save_btn": "✅ حفظ توقعاتي",
        "save_success": "تم الحفظ بنجاح! سيراها الأدمن.",
        "champ_label": "البطل",
        "r16": "دور الـ 16",
        "qf": "ربع النهائي",
        "sf": "نصف النهائي",
        "final": "🏆 النهائي",
        "lang_label": "اختر اللغة / Choose Language"
    }
}

# --- إدارة الحالة (Session State) ---
if 'lang' not in st.session_state:
    st.session_state.lang = "العربية"
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# اختيار اللغة في الشاشة الرئيسية
selected_lang = st.sidebar.selectbox(texts[st.session_state.lang]["lang_label"], ["العربية", "English"], 
                                     index=0 if st.session_state.lang == "العربية" else 1)
st.session_state.lang = selected_lang
T = texts[st.session_state.lang] # اختصار للوصول للنصوص

# --- دالة حفظ البيانات ---
def save_predictions(user_name, predictions):
    data = {}
    if os.path.exists("data.json"):
        with open("data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    data[user_name] = predictions
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# --- شاشة تسجيل الدخول ---
if not st.session_state.logged_in:
    st.markdown(f"<h1 style='text-align: center;'>{T['login_title']}</h1>", unsafe_allow_html=True)
    user_input = st.text_input(T["user_label"], placeholder=T["user_placeholder"])
    col_l, col_r = st.columns(2)
    with col_l:
        if st.button(T["btn_user"]):
            if user_input:
                st.session_state.logged_in, st.session_state.user_name, st.session_state.is_admin = True, user_input, False
                st.rerun()
            else: st.error(T["user_err"])
    with col_r:
        if st.button(T["btn_admin"]):
            if user_input == "admin123": # كلمة سر الأدمن
                st.session_state.logged_in, st.session_state.user_name, st.session_state.is_admin = True, "Admin", True
                st.rerun()
            else: st.error(T["admin_err"])
    st.stop()

# --- لوحة الأدمن ---
if st.session_state.is_admin:
    st.title(T["admin_dash"])
    if st.sidebar.button(T["logout"]):
        st.session_state.logged_in = False
        st.rerun()
    if os.path.exists("data.json"):
        with open("data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        for user, preds in data.items():
            with st.expander(f"{T['user_pred']} {user}"):
                st.json(preds)
    else: st.info(T["no_data"])
    st.stop()

# --- شاشة التوقعات (المستخدم) ---
st.sidebar.write(f"👤 {st.session_state.user_name}")
if st.sidebar.button(T["logout"]):
    st.session_state.logged_in = False
    st.rerun()

# --- CSS لتحسين الشكل ---
st.markdown("""
<style>
    [data-testid="stAppViewContainer"] { background-color: #0f0f0f; color: white; }
    .stRadio > div { flex-direction: row; justify-content: center; background: #1e1e1e; border-radius: 5px; padding: 5px; }
    hr { border-top: 1px solid #333; }
</style>
""", unsafe_allow_html=True)

def match_ui(t1, t2, date, key):
    st.markdown(f"<p style='text-align:center; color:grey; font-size:0.8rem;'>{date}</p>", unsafe_allow_html=True)
    winner = st.radio(f"W_{key}", [t1, t2], key=key, index=None, label_visibility="collapsed")
    return winner if winner else "TBD"

st.markdown(f"<h1 style='text-align: center;'>🏆 {T['champ_label']}</h1>", unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns([1.5, 1.2, 2, 1.2, 1.5])

with col1:
    st.write(f"### {T['r16']}")
    w1 = match_ui("MAL 🇲🇱", "TUN 🇹🇳", "Jan 3", "m1")
    w2 = match_ui("SEN 🇸🇳", "SUD 🇸🇩", "Jan 3", "m2")
    w3 = match_ui("EGY 🇪🇬", "BEN 🇧🇯", "Jan 5", "m3")
    w4 = match_ui("CIV 🇨🇮", "BUR 🇧🇫", "Jan 6", "m4")

with col5:
    st.write(f"### {T['r16']}")
    w5 = match_ui("ALG 🇩🇿", "COD 🇨🇩", "Jan 6", "m5")
    w6 = match_ui("NGA 🇳🇬", "MOZ 🇲🇿", "Jan 5", "m6")
    w7 = match_ui("RSA 🇿🇦", "CMR 🇨🇲", "Jan 4", "m7")
    w8 = match_ui("MAR 🇲🇦", "TAN 🇹🇿", "Jan 4", "m8")

with col2:
    st.write(f"### {T['qf']}")
    wq1 = match_ui(w1, w2, "Jan 9", "wq1")
    wq4 = match_ui(w3, w4, "Jan 10", "wq4")

with col4:
    st.write(f"### {T['qf']}")
    wq3 = match_ui(w5, w6, "Jan 10", "wq3")
    wq2 = match_ui(w7, w8, "Jan 9", "wq2")

with col3:
    st.write(f"### {T['sf']}")
    ws1 = match_ui(wq1, wq4, "Jan 14", "ws1")
    ws2 = match_ui(wq3, wq2, "Jan 14", "ws2")
    st.write("---")
    st.markdown(f"<h2 style='text-align:center;'>{T['final']}</h2>", unsafe_allow_html=True)
    champion = match_ui(ws1, ws2, "Jan 18", "final")

if st.button(T["save_btn"]):
    save_predictions(st.session_state.user_name, {"champion": champion, "full_bracket": [w1, w2, w3, w4, w5, w6, w7, w8]})
    st.success(T["save_success"])
    if champion != "TBD": st.balloons()