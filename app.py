import streamlit as st
import pandas as pd

st.set_page_config(page_title="تحديد المسار الدراسي", layout="centered")

st.markdown("""
    <style>
    .main, .stRadio, .stAlert, .stMarkdown {
        direction: rtl;
        text-align: right;
    }
    div[data-testid="stRadio"] > label {
        font-size: 18px;
        font-weight: bold;
        color: #1E3A8A;
    }
    .stButton>button {
        width: 100%;
        background-color: #1E3A8A;
        color: white;
        font-size: 20px;
        font-weight: bold;
        border-radius: 10px;
        padding: 12px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("تحديد المسار الدراسي")
st.caption("ابتكار الطالبة: حبيبة أحمد رمضان - الصف الأول الثانوي")
st.write("أجب عن الأسئلة الـ 30 التالية بدقة لاكتشاف المسار الأكاديمي والمهني الأنسب لقدراتك وميولك النفسية.")
st.divider()

SHEET_URL = "https://google.com"

try:
    df_questions = pd.read_excel(SHEET_URL, sheet_name="الورقة1")
    df_tracks = pd.read_excel(SHEET_URL, sheet_name="الورقة2")
except Exception as e:
    st.error("حدث خطأ في الاتصال بقاعدة البيانات. تأكد من اتصالك بالإنترنت.")
    st.stop()

user_answers = []

for index, row in df_questions.iterrows():
    st.subheader(f"السؤال {index + 1}: {row['السؤال']}")
    options = [
        row['الاختيار أ'],
        row['الاختيار ب'],
        row['الاختيار ج'],
        row['الاختيار د']
    ]
    choice = st.radio("اختر الإجابة الأقرب لشخصيتك:", options, key=f"q_{index}", index=None)
    user_answers.append(choice)
    st.write("")

if st.button("تحليل الإجابات وإظهار المسار المناسب"):
    if None in user_answers:
        st.warning("من فضلك أجب على جميع الأسئلة الـ 30 أولاً قبل عرض النتيجة.")
    else:
        s0 = 0
        s1 = 0
        s2 = 0
        s3 = 0
        
        for index, row in df_questions.iterrows():
            ans = user_answers[index]
            if ans == row['الاختيار أ']:
                s0 = s0 + 1
            elif ans == row['الاختيار ب']:
                s1 = s1 + 1
            elif ans == row['الاختيار ج']:
                s2 = s2 + 1
            elif ans == row['الاختيار د']:
                s3 = s3 + 1

        scores = [s0, s1, s2, s3]
        best_track_idx = scores.index(max(scores))
        best_track = df_tracks.iloc[best_track_idx]

        st.balloons()
        st.success(f"المسار الأنسب لك هو: **{best_track['إسم المسار']}**")
        st.info(f"**الكليات المناسبة لك:**\n\n {best_track['الكليات المناسبة']}")
        st.warning(f"**نصيحة التفوق والبدء:**\n\n {best_track['نصيحة التفوق']}")

        st.subheader("تحليل توافقك مع جميع المسارات:")
        chart_data = pd.DataFrame({
            "المسار": df_tracks['إسم المسار'],
            "النسبة المئوية (%)": [(scores[i] / len(df_questions)) * 100 for i in range(4)]
        })
        st.bar_chart(chart_data.set_index("المسار"))
                
