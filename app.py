import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from plotly import graph_objs as go


st.title("Rainfall Predictor")

data = pd.read_csv("historical_rainfall_data.csv")
df = data["Station"]



nav = st.sidebar.radio("Navigation",["Home","Predictor","Contribute"])
st.image("image//weather.jfif")
def func():
    plt.ylim(0)
    plt.ylabel("Rainfall")
    plt.tight_layout()
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot()
    return


if nav == "Home":
   
    if st.checkbox("Show Table"):
        #st.table(data)
        st.dataframe(data,width = 700,height = 700)
    graph = st.selectbox("What kind of graph? ",["Year vs Rainfall","Place vs Rainfall"])
    val = st.slider("Filter data using Years",1950,2050)
    data =data.loc[ data["Year"] >= val]

    

    if graph == "Year vs Rainfall":
        plt.figure(figsize = (15,10))
        plt.scatter(data["Year"],data["Rainfall"])
        plt.xlabel("Year")
        func()
    
    if graph == "Place vs Rainfall":
        plt.figure(figsize = (15,10))
        labels= data["Station"]
        fig = plt.scatter(data["Station"],data["Rainfall"])
        plt.xticks(rotation = 90)
        plt.xlabel("Place")
        func()

    #if graph == "Interactive":
        #layout = go.Layout(
        #    xaxis = dict(range = [0,2050]),
        #   yaxis = dict(range =  [0,400])
        #)
        #fig = go.Figure(data = go.Scatter( x = data["Year"], y = data["Rainfall"],mode = 'marker'), layout  == layout)
        #st.plotly_chart(fig)
        #st.bar_chart(data,y=data["Rainfall"])

if nav == "Predictor":
    st.header("Guess Rainfall")
    val = st.date_input("Enter Date for Prediction")
    pal = st.selectbox("Enter Place for Prediction",[
    "Ambagan_ctg",
    "Barisal",
    "Bhola",
    "Bogra",
    "Chandpur",
    "Chittagong",
    "chuadanga",
    "Comilla",
    "CoxsBazar",
    "Dinajpur",
    "Faridpur",
    "Feni",
    "Hatiya",
    "Ishurdi",
    "Jessore",
    "Khulna",
    "Khepupara",
    "Kutubdia",
    "Madaripur",
    "Mongla",
    "Mymensingh",
    "M.court",
    "Patuakhali",
    "Rangamati",
    "Rajshahi",
    "Rangpur",
    "Sandwip",
    "Satkhira",
    "Sitakunda"
    "Srimangal",
    "Sylhet",
    "sydpur",
    "Tangail",
    "Teknaf",
    ])
    #st.text_input("Enter Place for Prediction")


    if st.button("Predict"): 
        st.success("RainFall Or Not")

if nav == "Contribute":
    st.header("Contribution to our dataset")
    day =st.date_input("Enter Date")
    place =st.text_input("Enter Place")
    rainfall =st.number_input("Enter Rainfall")
