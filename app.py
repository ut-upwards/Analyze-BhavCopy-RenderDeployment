import pandas as pd
import numpy as np
import streamlit as st
import streamlit.components.v1 as components


#Setting default configuration of page
st.set_page_config(
     layout="wide",
     initial_sidebar_state="expanded",
)

hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>

"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

st.sidebar.title("Ananlyze Daily BhavCopy")
st.sidebar.write("Analyze the daily complete bhavcopy with a simple drag n drop of that csv file")

link1 = '[Go Through The Steps](https://drive.google.com/file/d/1I-jWyK6Qe1fNOs7UjAnVngM-0ZQz6iyZ/view?usp=sharing)'
st.sidebar.markdown(link1, unsafe_allow_html=True)
link2 = '[Watch Tutorial Video](https://drive.google.com/file/d/1l-fRhbiTBVxV6FPG5kjrHMHec_u63wvf/view?usp=sharing)'
st.sidebar.markdown(link2, unsafe_allow_html=True)
link3 = '[GitHub Link](https://github.com/ut-upwards)'
st.sidebar.markdown(link3, unsafe_allow_html=True)

st.sidebar.header("About the app")
st.sidebar.write("BhavCopy is a csv file that contains a summary of daily details of financial instruments. Published daily on NSE website, it is used to analyse the market for that day. The app makes it easier, saving a lot of time in analyzing the BhavCopy with certain degree of customizablity.")
link4 = '[Author](https://www.linkedin.com/in/utkarsh-sahaya/)'
st.sidebar.markdown(link4, unsafe_allow_html=True)


st.title("Analyze Daily BhavCopy")
st.header("Please go through the steps to know how to use")

components.html(
  """
  <a href="https://drive.google.com/file/d/1I-jWyK6Qe1fNOs7UjAnVngM-0ZQz6iyZ/view?usp=sharing" target=_blank> 
    <button style="padding:5px 15px 5px 15px; margin-top:3px"> Go Through The Steps</button> </a> 

  &nbsp; &nbsp; 

  <a href="https://drive.google.com/file/d/1l-fRhbiTBVxV6FPG5kjrHMHec_u63wvf/view?usp=sharing" target=_blank>
    <button style="padding:5px 15px 5px 15px; margin-top:3px">Watch Tutorial Video </button> </a>

  &nbsp; &nbsp;

  <a href="https://github.com/ut-upwards" target=_blank>
    <button style="padding:5px 15px 5px 15px; margin-top:3px">Github Link </button> </a> 
    <hr>
  
  """
)

st.subheader("Choose- 'FULL BHAVCOPY AND SECURITY DELIVERABLE DATA'  as shown in the steps/video")
file = st.file_uploader("", type=['csv'])
if file is not None:
  def load_csv():
    df = pd.read_csv(file)
    return(df)


# Selecting few parameters
st.subheader("The number of shares you want to see for each category")
n = st.selectbox('', [5, 10, 15, 20, 25, 30, 35, 40])
st.subheader("Select the minimum turnover in crores")
turnover = st.slider('', min_value=100, max_value=2000)



if st.button("Submit"):

  if file is not None:
    try:
      data = pd.read_csv(file, skipinitialspace=True)
      data.replace("-", np.nan, inplace=True)

      # Changing the Dtype of DELIV_QTY & DELIV_PER from object to numeric for further calculations
      data['DELIV_QTY'] = pd.to_numeric(data['DELIV_QTY'])
      data['DELIV_PER'] = pd.to_numeric(data['DELIV_PER'])

      # Dropping rows with nan values
      data.dropna(axis=0, how='any', inplace=True)

      # Taking only those rows where SERIES = EQ as only Equity market is being analyzed
      data = data[(data['SERIES']) == 'EQ']

      data = data.reset_index(drop=True)

      # Converting turnover_lacs columns to turnover_crores for sake of ease and simplicity
      data.rename(columns = {'TURNOVER_LACS': 'TURNOVER_CRORES'}, inplace = True)
      data['TURNOVER_CRORES'] = data['TURNOVER_CRORES']/100

      # Adding a %CHANGE column
      data['%CHANGE'] = ((data['CLOSE_PRICE']-data['PREV_CLOSE'])/data['PREV_CLOSE'])*100

      # Adding a %GAP Column
      data['%GAP'] = ((data['OPEN_PRICE']-data['PREV_CLOSE'])/data['PREV_CLOSE'])*100

      data = data.round(decimals=2)
      st.write('The following is the processed Bhavdata file that is going to be analyzed')
      st.write(data)

      percentage_delivery = 75.00 
      #turnover = 400 # Turnover in crores
      delivery_percentage = 45.00

      st.subheader('Your Customized market report')
      

      st.header('Top Gainer for the filters applied')
      df = data[['SYMBOL','%CHANGE', 'OPEN_PRICE', 'HIGH_PRICE', 'LOW_PRICE', 'CLOSE_PRICE', 'TURNOVER_CRORES', 'DELIV_PER']]
      df = df[(df['TURNOVER_CRORES']) >= turnover]
      df = df.sort_values(by=['%CHANGE'], ascending=False, ignore_index=True)
      df = df[(df['%CHANGE']) > 0.00]
      st.write(df.head(n))
      if len(df) < n :
        st.write('These are the only gainers for the filters applied')
      

      st.header('Top Losers for the filters applied')
      df = data[['SYMBOL','%CHANGE', 'OPEN_PRICE', 'HIGH_PRICE', 'LOW_PRICE', 'CLOSE_PRICE', 'TURNOVER_CRORES', 'DELIV_PER' ]]
      df = df[(df['TURNOVER_CRORES']) >= turnover]
      df = df.sort_values(by=['%CHANGE'], ascending=True, ignore_index=True)
      df = df[(df['%CHANGE']) < 0.00]
      st.write(df.head(n))
      if len(df) < n :
        st.write('These are the only loosers for the filters applied')


      st.header('Most Percentage delivery for the filters applied')
      df = data[['SYMBOL', 'DELIV_PER', 'OPEN_PRICE', 'HIGH_PRICE', 'LOW_PRICE', 'CLOSE_PRICE', 'TURNOVER_CRORES', '%CHANGE']]
      df = df[(df['TURNOVER_CRORES']) >= turnover]
      df = df.sort_values(by=['DELIV_PER'], ascending=False, ignore_index=True)
      st.write(df.head(n))
      if len(df) < n :
        st.write('These are the only shares for the filters applied')


      st.header('Least Percentage delivery for the filters applied')
      df = data[['SYMBOL', 'DELIV_PER', 'OPEN_PRICE', 'HIGH_PRICE', 'LOW_PRICE', 'CLOSE_PRICE', 'TURNOVER_CRORES', '%CHANGE']]
      df = df[(df['TURNOVER_CRORES']) >= turnover]
      df = df.sort_values(by=['DELIV_PER'], ascending=True, ignore_index=True)
      st.write(df.head(n))
      if len(df) < n :
        st.write('These are the only shares for the filters applied')


      st.header('Most active by turnover for the filters applied')
      df = data[['SYMBOL','TURNOVER_CRORES', 'OPEN_PRICE', 'HIGH_PRICE', 'LOW_PRICE', 'CLOSE_PRICE', '%CHANGE', 'DELIV_PER']]
      df = df[(df['TURNOVER_CRORES']) >= turnover] 
      st.write((df.sort_values(by=['TURNOVER_CRORES'], ascending=False, ignore_index=True).head(n)))
      if len(df) < n :
        st.write('These are the only shares for the filters applied')

      
      st.header('Least active by turnover for the filters applied')
      df = data[['SYMBOL','TURNOVER_CRORES', 'OPEN_PRICE', 'HIGH_PRICE', 'LOW_PRICE', 'CLOSE_PRICE', '%CHANGE', 'DELIV_PER']]
      df = df[(df['TURNOVER_CRORES']) >= turnover] 
      st.write((df.sort_values(by=['TURNOVER_CRORES'], ascending=True, ignore_index=True).head(n)))
      if len(df) < n :
        st.write('These are the only shares for the filters applied')


      st.header('Most active by volume for the filters applied')
      df = data[['SYMBOL', 'TTL_TRD_QNTY', 'OPEN_PRICE', 'HIGH_PRICE', 'LOW_PRICE', 'CLOSE_PRICE', 'DELIV_PER', '%CHANGE', 'TURNOVER_CRORES' ]]
      df = df[(df['TURNOVER_CRORES']) >= turnover]
      df = df.sort_values(by=['TTL_TRD_QNTY'], ascending=False, ignore_index=True)
      st.write(df[['SYMBOL', 'TTL_TRD_QNTY', 'OPEN_PRICE', 'HIGH_PRICE', 'LOW_PRICE', 'CLOSE_PRICE', 'DELIV_PER', '%CHANGE']].head(n))
      if len(df) < n :
        st.write('These are the only shares for the filters applied')
      

      st.header('Least active by volume for the filters applied')
      df = data[['SYMBOL', 'TTL_TRD_QNTY', 'OPEN_PRICE', 'HIGH_PRICE', 'LOW_PRICE', 'CLOSE_PRICE', 'DELIV_PER', '%CHANGE', 'TURNOVER_CRORES' ]]
      df = df[(df['TURNOVER_CRORES']) >= turnover]
      df = df.sort_values(by=['TTL_TRD_QNTY'], ascending=True, ignore_index=True)
      st.write(df[['SYMBOL', 'TTL_TRD_QNTY', 'OPEN_PRICE', 'HIGH_PRICE', 'LOW_PRICE', 'CLOSE_PRICE', 'DELIV_PER', '%CHANGE']].head(n))
      if len(df) < n :
        st.write('These are the only shares for the filters applied')


      st.header('Strong throughout the day')
      st.subheader('Shares with PREV_CLOSE <= LOW_PRICE <= OPEN_PRICE <= AVERAGE_PRICE <= CLOSE_PRICE')
      df = data[['SYMBOL', 'PREV_CLOSE', 'OPEN_PRICE', 'AVG_PRICE' , 'CLOSE_PRICE', 'HIGH_PRICE', 'LOW_PRICE', 'TURNOVER_CRORES', 'DELIV_PER', '%CHANGE']]
      df = df[(df['TURNOVER_CRORES']) >= turnover]
      df = df[(df['PREV_CLOSE']) <= (df['LOW_PRICE'])]
      df = df[(df['LOW_PRICE']) <= (df['OPEN_PRICE'])]
      df = df[(df['OPEN_PRICE']) <= (df['AVG_PRICE'])]
      df = df[(df['AVG_PRICE']) <= (df['CLOSE_PRICE'])]
      st.write(df[['SYMBOL', 'PREV_CLOSE', 'OPEN_PRICE', 'AVG_PRICE' , 'CLOSE_PRICE', 'HIGH_PRICE', 'LOW_PRICE', 'DELIV_PER', '%CHANGE']].head(n))
      if len(df) < n :
        st.write('These are the only shares for the filters applied')

      
      st.header('Weak throughout the day')
      st.subheader('Shares with PREV_CLOSE >= HIGH_PRICE >= OPEN_PRICE >= AVERAGE_PRICE >= CLOSE_PRICE')
      df = data[['SYMBOL', 'PREV_CLOSE', 'OPEN_PRICE', 'AVG_PRICE', 'CLOSE_PRICE', 'HIGH_PRICE', 'LOW_PRICE', 'TURNOVER_CRORES', 'DELIV_PER', '%CHANGE']]
      df = df[(df['TURNOVER_CRORES']) >= turnover]
      df = df[(df['PREV_CLOSE']) >= (df['HIGH_PRICE'])]
      df = df[(df['HIGH_PRICE']) >= (df['OPEN_PRICE'])]
      df = df[(df['OPEN_PRICE']) >= (df['AVG_PRICE'])]
      df = df[(df['AVG_PRICE']) >= (df['CLOSE_PRICE'])]
      st.write(df[['SYMBOL', 'PREV_CLOSE', 'OPEN_PRICE', 'AVG_PRICE' , 'CLOSE_PRICE', 'HIGH_PRICE', 'LOW_PRICE', 'DELIV_PER', '%CHANGE']].head(n))
      if len(df) < n :
        st.write('These are the only shares for the filters applied')


      st.header('Top Gap up shares for the filters applied')
      df = data[['SYMBOL', '%GAP', 'PREV_CLOSE', 'OPEN_PRICE', 'CLOSE_PRICE','HIGH_PRICE', 'LOW_PRICE', 'TURNOVER_CRORES', 'DELIV_PER', '%CHANGE']]
      df = df[(df['TURNOVER_CRORES']) >= turnover]
      df = df.sort_values(by=['%GAP'], ascending=False, ignore_index=True)
      df = df[(df['%GAP']) > 0.00]
      st.write(df[['SYMBOL', '%GAP', 'PREV_CLOSE', 'OPEN_PRICE', 'CLOSE_PRICE','HIGH_PRICE', 'LOW_PRICE', 'DELIV_PER', '%CHANGE']].head(n))
      if len(df) < n :
        st.write('These are the only shares for the filters applied')

      
      st.header('Top Gap down shares for the filters applied')
      df = data[['SYMBOL', '%GAP', 'PREV_CLOSE', 'OPEN_PRICE', 'CLOSE_PRICE','HIGH_PRICE', 'LOW_PRICE', 'TURNOVER_CRORES', 'DELIV_PER', '%CHANGE']]
      df = df[(df['TURNOVER_CRORES']) >= turnover]
      df = df.sort_values(by=['%GAP'], ascending=True, ignore_index=True)
      df = df[(df['%GAP']) < 0.00]
      st.write(df[['SYMBOL', '%GAP', 'PREV_CLOSE', 'OPEN_PRICE', 'CLOSE_PRICE','HIGH_PRICE', 'LOW_PRICE', 'DELIV_PER', '%CHANGE']].head(n))
      if len(df) < n :
        st.write('These are the only shares for the filters applied')


    except Exception as e:
      st.subheader('ERROR: Wrong File Uploaded')
  
  else:
    st.subheader("ERROR: No file uploaded")

