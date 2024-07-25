import streamlit as st


def sideBar():
    with st.sidebar:
        st.markdown('''
            # st 함수
            - [st.text() 함수](#8c208f26)
            - [st.color_picker() 함수](#color_picker_header)
        ''', unsafe_allow_html=True)


def body():
    st.title("st.text() 함수")
    
    code='''
        st.write('Hello, *World!* :sunglasses:')
    '''
    st.code(code, language='python')
    
    st.title("color_picker() 함수",anchor="color_picker_header")
    

    st.markdown(''' ------------------------------ ''')

    with st.echo():
        st.header("컬러픽커 예시")
        color = st.color_picker("컬러픽커", "#00f900")
        st.write("The current color is", color)
        
    st.markdown(''' ------------------------------ ''')
    

def main():
    sideBar()
    with st.container():
        body()
        

if __name__ == '__main__':
    main()

