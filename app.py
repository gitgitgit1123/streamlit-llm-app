from dotenv import load_dotenv

load_dotenv()

import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

# -------------------------
# ④ 翻訳関数（戻り値あり）
# -------------------------
def translate_text(input_text: str, expert_type: str) -> str:
    """入力テキストと選択言語（専門家タイプ）をもとに翻訳結果を返す"""

    # 専門家ロール（システムメッセージ）の切り替え
    if expert_type == "英語翻訳の専門家":
        system_prompt = (
            "You are a professional translator specialized in English translation. "
            "Translate the user's input text into **English** naturally and accurately."
        )
    else:  # 中国語
        system_prompt = (
            "You are a professional translator specialized in Chinese translation. "
            "Translate the user's input text into **Chinese** naturally and accurately."
        )

    llm = ChatOpenAI(
        model="gpt-4o-mini",  # 例：軽量モデル
        temperature=0.0,
        api_key=st.secrets["OPENAI_API_KEY"]  # ← secrets.toml を使う想定
    )

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=input_text)
    ]

    result = llm(messages)
    return result.content


# -------------------------
# Streamlit UI 部分
# -------------------------
st.title("🌏 シンプル翻訳 Web アプリ（英語／中国語）")

# ⑤ Webアプリの説明
st.write("""
### 📝 アプリの使い方
1. 下のテキスト入力欄に翻訳したい文章を入力してください  
2. 翻訳言語（英語 or 中国語）をラジオボタンで選んでください  
3. 「翻訳する」ボタンを押すと、専門家による翻訳結果が表示されます  
""")

# 入力フォーム
input_text = st.text_area("翻訳したい文章を入力してください：", height=120)

# ラジオボタン（③ LLMの専門家ロール切替）
expert_type = st.radio(
    "翻訳先の言語を選択してください：",
    ("英語翻訳の専門家", "中国語翻訳の専門家")
)

# 実行ボタン
if st.button("翻訳する"):
    if input_text.strip():
        translated = translate_text(input_text, expert_type)
        st.subheader("🔍 翻訳結果")
        st.write(translated)
    else:
        st.warning("テキストを入力してください。")