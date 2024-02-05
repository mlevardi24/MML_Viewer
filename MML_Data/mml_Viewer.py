import streamlit as st
import pandas as pd

st.set_page_config(layout='wide')

if "Filter" not in st.session_state:
    st.session_state["Filter"] = "None"

st.markdown(
    """
        <style>
            .appview-container .main .block-container {{
                padding-top: {padding_top}rem;
                padding-bottom: {padding_bottom}rem;
                }}

        </style>""".format(
        padding_top=1, padding_bottom=1
    ),
    unsafe_allow_html=True,
)

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("MML_Data/style.css")

filter = "None"
csvFile = "MML_Data/MML_Main.csv"
global data

st.sidebar.subheader("Searches:")
gameSearch = st.sidebar.text_input("Game")
chalSearch = st.sidebar.text_input("Challenge")
placeSearch = st.sidebar.text_input("Placement")
creatorSearch = st.sidebar.text_input("Creator")
verifySearch = st.sidebar.text_input("Verifier")
test = 400

def change_list():
    csvFile = "MML_Data/Unlimited.csv"

def load_data(nrows, filterName):
    global data
    global ML_table

    global verifySearch 
    st.session_state["Filter"] = filterName
    data = pd.read_csv(csvFile, nrows=nrows)
    data = data.filter(items=["#","ML SCORE","MAIN LIST","VIDEO GAME","DEVELOPER","VERSION","VERIFIER"])
    data = data.rename(columns={"#":"PLACEMENT"})
    data = data.rename(columns={"MAIN LIST":"CHALLENGE"})
    data = data.loc[data['VIDEO GAME'].isnull() == False, :]
    if filterName == "Top150":
        data = data.query('PLACEMENT <= 150')
    elif filterName == "Legacy":
        data = data.query('PLACEMENT > 150')
    elif filterName == "400Pt":
        data = data.query("`ML SCORE` == {0}".format(test))
    elif filterName == "200Pt":
        data = data.query('`ML SCORE` == 200')
    elif filterName == "100Pt":
        data = data.query('`ML SCORE` == 100')
    elif filterName == "50Pt":
        data = data.query('`ML SCORE` == 50')
    elif filterName == "25Pt":
        data = data.query('`ML SCORE` == 25')
    elif filterName == "12Pt":
        data = data.query('`ML SCORE` == 12')
    elif filterName == "6Pt":
        data = data.query('`ML SCORE` == 6')
    elif filterName == "3Pt":
        data = data.query('`ML SCORE` == 3')
    elif filterName == "0Pt":
        data = data.query('`ML SCORE` == 0')
    elif filterName == "Search":
        data = data.query("`VIDEO GAME`.str.contains('{0}', case=False)".format(gameSearch), engine='python')
        data = data.query("`CHALLENGE`.str.contains('{0}', case=False)".format(chalSearch), engine='python')
        data = data.query("`DEVELOPER`.str.contains('{0}', case=False)".format(creatorSearch), engine='python')
        data = data.query("`VERIFIER`.str.contains('{0}', case=False)".format(verifySearch), engine='python')
        if len(placeSearch) != 0:
            data = data.query("`PLACEMENT` == {0}".format(placeSearch))

    return data
    
data = load_data(400, st.session_state["Filter"])

st.title('Max Mode List (ML)')

st.divider()

st.sidebar.button("Search", on_click=load_data, args=[400, "Search"])

with st.sidebar:
    st.divider()
    st.subheader("Filters:")
    col_1, col_2, col_3 = st.columns(3)
    with col_1:
        st.button("None", on_click=load_data, args=[400, "None"])
    with col_2:
        st.button("Top 150", on_click=load_data, args=[400, "Top150"])
    with col_3:
        st.button("Legacy Modes", on_click=load_data, args=[400, "Legacy"])

    col_1, col_2, col_3 = st.columns(3)
    with col_1:
        st.button("400 Points", on_click=load_data, args=[400, "400Pt"])
        st.button("200 Points", on_click=load_data, args=[400, "200Pt"])
        st.button("100 Points", on_click=load_data, args=[400, "100Pt"])
    with col_2:
        st.button("50 Points", on_click=load_data, args=[400, "50Pt"])
        st.button("25 Points", on_click=load_data, args=[400, "25Pt"])
        st.button("12 Points", on_click=load_data, args=[400, "12Pt"])
    with col_3:
        st.button("6 Points", on_click=load_data, args=[400, "6Pt"])
        st.button("3 Points", on_click=load_data, args=[400, "3Pt"])
        st.button("0 Points", on_click=load_data, args=[400, "0Pt"])


global ML_table
ML_table = st.dataframe(data, width=2000, height=700)

st.button("Unlimited List", on_click=change_list)
