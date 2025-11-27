import streamlit as st  # フロントエンドを扱うstreamlitの機能をインポート
import os
from openai import OpenAI  # OpenAIのChatGPTの機能をインポート
from dotenv import load_dotenv  # ローカル環境用に.envファイルを読み込むためのライブラリ

# OpenAI APIの設定（Streamlit Cloud用とローカル用の両方に対応）
try:
    api_key = st.secrets["OPENAI_API_KEY"]
except Exception:
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")

# OpenAIの機能をclientに代入
client = OpenAI(api_key=api_key)

# chatGPTが可能な文章のテイストの設定一覧を作成
content_kind_of = [
    "中立的で客観的な文章",
    "分かりやすい、簡潔な文章",
    "親しみやすいトーンの文章",
    "専門用語をできるだけ使わない、一般読者向けの文章",
    "言葉の使い方にこだわり、正確な表現を心がけた文章",
    "ユーモアを交えた文章",
    "シンプルかつわかりやすい文法を使った文章",
    "面白く、興味深い内容を伝える文章",
    "具体的でイメージしやすい表現を使った文章",
    "人間味のある、感情や思いを表現する文章",
    "引用や参考文献を適切に挿入した、信頼性の高い文章",
    "読み手の興味を引きつけるタイトルやサブタイトルを使った文章",
    "統計データや図表を用いたわかりやすい文章",
    "独自の見解や考え方を示した、論理的な文章",
    "問題提起から解決策までを網羅した、解説的な文章",
    "ニュース性の高い、旬なトピックを取り上げた文章",
    "エンターテイメント性のある、軽快な文章",
    "読者の関心に合わせた、専門的な内容を深く掘り下げた文章",
    "人物紹介やインタビューを取り入れた、読み物的な文章",
]

# ChatGPTにリクエストする関数
def run_gpt(content_text_to_gpt, content_kind_of_to_gpt, content_maxStr_to_gpt):
    request_to_gpt = (
        content_text_to_gpt
        + " また、これを記事として読めるように、記事のタイトル、目次、内容の順番で出力してください。"
        + "内容は" + content_maxStr_to_gpt + "文字以内で出力してください。"
        + "また、文章は" + content_kind_of_to_gpt + "にしてください。"
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": request_to_gpt},
        ],
    )

    output_content = response.choices[0].message.content.strip()
    return output_content

# Streamlit UI
st.title('GPTに記事書かせるアプリ')
output_content = st.empty()

select_box = ["シンプルモード", "箇条書きモード"]
radio_select = st.sidebar.radio("入力モード", select_box)

if radio_select == select_box[0]:
    content_text_to_gpt = st.sidebar.text_input("書かせたい内容を入力してください！")
else:
    content_text_to_gpt_list = [
        st.sidebar.text_input("書かせたい内容を箇条書きで入力してください", placeholder="箇条書き１つ目"),
        st.sidebar.text_input("項目2つ目"),
        st.sidebar.text_input("項目3つ目"),
        st.sidebar.text_input("項目4つ目"),
        st.sidebar.text_input("項目5つ目"),
    ]

    content_text_to_gpt_array = [c for c in content_text_to_gpt_list if c != ""]
    content_text_to_gpt = ""
    if content_text_to_gpt_array:
        content_text_to_gpt = "記事にしてほしい内容を箇条書きにすると、" + "、".join(content_text_to_gpt_array) + " です。"

content_kind_of_to_gpt = st.sidebar.selectbox("文章の種類", options=content_kind_of)
content_maxStr_to_gpt = str(st.sidebar.slider('記事の最大文字数', 100, 3000, 1000))
warning_text = st.sidebar.empty()

if st.sidebar.button('記事を書かせる'):
    if content_text_to_gpt != "":
        output_content.write("GPT生成中")
        warning_text.write("")
        output_content_text = run_gpt(content_text_to_gpt, content_kind_of_to_gpt, content_maxStr_to_gpt)
        output_content.write(output_content_text)
        st.download_button(
            label='記事内容 Download',
            data=output_content_text,
            file_name='out_put.txt',
            mime='text/plain',
        )
    else:
        warning_text.write("書かせたい内容が入力されていません")
