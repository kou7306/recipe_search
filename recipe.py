import streamlit as st
import openai
import os

CHATGPT_API_KEY = os.environ["CHATGPT_API_KEY"]
openai.api_key = CHATGPT_API_KEY

responses = [""]
r = ""

def Ans_ChatGPT(question,responses):
  completion = openai.ChatCompletion.create(
    model = "gpt-3.5-turbo",
    messages=[
      {"role": "system", "content": "You are a cooking professional"},
      {"role" : "user","content" : question}  
    ],
    stream = True
  )
  # responseに出力していく
  # response = completion.choices[0].message.content
  response = ""
  for chunk in completion:
    if chunk:
      content = chunk['choices'][0]['delta'].get('content')
      if content:
        response += content
        responses[0] += content
        yield response

    
  
  

st.title('レシピ検索')
markdown = """
余った食材で料理を作ろう！！
"""


st.markdown(markdown)
ingredients = st.text_input('食材を句読点（、）で区切って入力')

if "flag" not in st.session_state:
  st.session_state.flag = 0 #flag記憶の作成、検索ボタンが押されたかどうか
search = st.button("検索") #検索ボタン

line = "-" * 100 



if(st.session_state["flag"] ==0 and search and len(ingredients)==0): #何も入力されていない
  st.text("食材を入力してください")
if(st.session_state["flag"] ==0 and search and len(ingredients)!=0 ): #検索実行
  timeHolder = st.empty()
  st.session_state["flag"] += 1 #検索フラグセット
  st.session_state["ingredients"] = ingredients #検索している食材情報を記憶
  a = st.session_state["ingredients"]
  question = f"{a}を使った料理のレシピを1個表示して。ただし、最初にその料理名を書き、料理名の直後に"":""と書いた後、改行し、材料とその量を箇条書きにしてから、作り方を書いて。"
  ans = Ans_ChatGPT(question,responses)
  for talk in ans:
    timeHolder.text(talk)
  
  
  st.session_state["recipe"] = responses[0] #料理のレシピを記憶
  
  target = ':'
  idx = responses[0].find(target)
  r+=responses[0][:idx]
  st.session_state["ans_except"]=r #過去の料理名を記憶
  
if(st.session_state["flag"]>1):
  
  
  st.text(st.session_state["recipe"])
  # st.text(st.session_state["ans_except"])
  st.text(f"\n\n\n\n\n{line}\n\n\n")
  timeHolder = st.empty()
  a = st.session_state["ingredients"]
  b= st.session_state["ans_except"]
  question = f"{b}といったこれらの料理以外で、{a}を使った料理のレシピを1個表示して。ただし、最初にその料理名を書き、料理名の直後に"":""と書いた後、改行し、材料とその量を箇条書きにしてから、作り方を書いて。"
  ans = Ans_ChatGPT(question,responses)
  for talk in ans:
    timeHolder.text(talk)
  # st.text(f"\n\n\n\n\n{line}\n\n\n")
  # st.text(st.session_state["recipe"])
  st.session_state["recipe"] = st.session_state["recipe"] + "\n\n\n\n\n" + line + "\n\n\n" +  responses[0]
  target = ':'
  idx = responses[0].find(target)
  r+=responses[0][:idx]
  st.session_state["ans_except"] = st.session_state["ans_except"] + "," + r #除くものに追加
  st.session_state["flag"] += 1
  if(st.session_state["flag"]==4):
    st.session_state["flag"]=0
if(st.session_state["flag"]>0):
  if(st.session_state["flag"]==1):
    st.session_state["flag"] += 1
  st.button("もっと見る")
    
