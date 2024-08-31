import streamlit as st
import pandas as pd
from back_image import add_bg_from_local
import db
from streamlit_autorefresh import st_autorefresh
from streamlit_option_menu import option_menu
from PIL import Image
from datetime import datetime


st.set_page_config(page_title="Alarm Manager", page_icon="👓")
hide_menu = """ 
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
        padding-left: 0rem;
        padding-right: 0rem;
        }
    </style>
    """
st.markdown(hide_menu, unsafe_allow_html=True)

class EventX:
    def __init__(self, id: str, pos: str, status: str, etime: str, hold: str, reset: str):
        super().__init__()
        add_bg_from_local('./images/bw.png')
        self.id = id
        self.pos = pos
        self.status = status
        self.etime = etime
        self.hold = hold
        self.reset = reset
        self.build()

    def hold_send(self):
        db.holdDB(self.id)  

    def reset_send(self):
        db.resetDB(self.id)  

    def build(self):
        c_time = datetime.now()
        d_time = datetime(int(self.etime[0:4]), int(self.etime[5:7]), int(self.etime[8:10]), int(self.etime[11:13]), int(self.etime[14:16]), int(self.etime[17:19]))
        diff_time = str(c_time - d_time)
        container = st.container(border=True,)
        container.title(self.pos)
        container.subheader(f'현재상태 : {self.status}', divider='rainbow')
        container.text(f'경과시간 : {diff_time[0:-7]}')
        container.write(f'확인 : {self.hold}---리셋 : {self.reset}')

        with container.container():
            c1, c2 = st.expander("⚠️원격제어(주의)").columns(2)
            with c1:
                st.button(f"{self.pos} 확인", on_click=self.hold_send, use_container_width=True)  
            with c2:              
                st.button(f"{self.pos} 리셋", on_click=self.reset_send, use_container_width=True) 

class TotalX:
    def __init__(self, id: str, pos: str, status: str, etime: str):
        super().__init__()
        add_bg_from_local('./images/bw.png')
        self.id = id
        self.pos = pos
        self.status = status
        self.etime = etime
        self.build()

    def build(self):
        c_time = datetime.now()
        d_time = datetime(int(self.etime[0:4]), int(self.etime[5:7]), int(self.etime[8:10]), int(self.etime[11:13]), int(self.etime[14:16]), int(self.etime[17:19]))
        diff_time = str(c_time - d_time)
        container = st.container(border=True,)
        if self.status == 'Alarm':
            container.subheader(f':red[{self.pos}]', divider='red')
            container.write(f'현재상태 : :blue[{self.status}]')
            container.write(f'경과시간 : :blue[{diff_time[0:-7]}]')
        elif self.status == 'Running':
            container.subheader(f':blue[{self.pos}]', divider='blue')
            container.write(f'현재상태 : :blue[{self.status}]')
            container.write(f'경과시간 : :blue[{diff_time[0:-7]}]')
        else:
            container.subheader(f':grey[{self.pos}]', divider='grey')
            container.write(f'현재상태 : :blue[{self.status}]')
            container.write(f'경과시간 : :blue[{diff_time[0:-7]}]')    
        with container.container():
            with st.expander("위치도면"):
                st.image(f"./images/{self.id}.png", use_column_width="auto")

def done():
    st.markdown("""
                <meta http-equiv="refresh" content="0; url='https://www.google.com'" />
                """, unsafe_allow_html=True
            )   


if __name__ == "__main__":
    st.title("스마트안전관리시스템")
    add_bg_from_local('./images/bg_c.jpg')
    password = st.text_input("비밀번호(4자리)를 입력하세요", type='password', key='1')
    login = st.checkbox("Login")
    cancel = st.button("취 소", use_container_width = True)  

    if cancel:
        done()
    if login or password == '1':
        add_bg_from_local('./images/bw.png')
        st.success("Login successfully.")
        st.write("😊 핸드폰은 'Close'버튼을 눌러 종료하세요")
        select = option_menu(
            menu_title="",
            options=["알람", "전체", "종 료"],
            icons=["house", "book"],
            orientation="horizontal"
            )

        if select == "알람":
            st_autorefresh(interval=5000, key="reload_count")
            data = db.readAll()
            data.sort(key=lambda x: x["id"])

            for i in range(len(data)):
                id = data[i]["id"]
                pos = data[i]["pos"]
                status = data[i]["status"]
                etime = data[i]["etime"]
                hold = data[i]["hold"]
                reset = data[i]["reset"]

                if status == 'Alarm':
                    EventX(id, pos, status, etime, hold, reset) 

        if select == "전체":
            st_autorefresh(interval=5000, key="reload_count")
            data = db.readAll()
            data.sort(key=lambda x: x["id"])

            for i in range(len(data)):
                id = data[i]["id"]
                pos = data[i]["pos"]
                status = data[i]["status"]
                etime = data[i]["etime"]
                TotalX(id, pos, status, etime)  

        if select == "종 료":
            done()            