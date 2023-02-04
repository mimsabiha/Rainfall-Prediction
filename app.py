import pickle
import numpy as np
import streamlit as st
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from plotly import graph_objs as go
import csv


st.title("Rainfall Predictor")

# data = pd.read_csv("E:/3rd_yr_course/3_2/AI/Rainfall-Prediction/historical_rainfall_data.csv")
data = pd.read_csv('historical_rainfall_data.csv')
df = data["Station"]
df1 = data[{"StationIndex", "Station"}]
df1.drop_duplicates(inplace=True)

nav = st.sidebar.radio("Navigation", ["Home", "Predictor", "Contribute"])
# st.image("E:/3rd_yr_course/3_2/AI/Rainfall-Prediction/image/weather.jfif")
# loaded_model = pickle.load(open('E:/3rd_yr_course/3_2/AI/Rainfall-Prediction/trained_model.sav', 'rb'))
st.image('image//weather.jfif')
loaded_model = pickle.load(open('trained_model.sav', 'rb'))


def func():
    plt.ylim(0)
    plt.ylabel("Rainfall")
    plt.tight_layout()
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot()
    return


def prediction(monthPredict, dayPredict, yearPredict, placePredict):
    index = df1[df1["Station"] == placePredict]
    ind = index.iloc[0]["StationIndex"]
    input_data = (ind, monthPredict, dayPredict)

    # changing the input_data to numpy array
    input_data_as_numpy_array = np.asarray(input_data)

    # reshape the array as we are predicting for one instance
    input_data_reshaped = input_data_as_numpy_array.reshape(1, -1)

    predictionRainFall = loaded_model.predict(input_data_reshaped)
    return predictionRainFall[0]


if nav == "Home":

    if st.checkbox("Show Table"):
        # st.table(data)
        st.dataframe(data, width=700, height=700)
    st.header("Data visualization")
    graph = st.selectbox("What kind of graph? ", ["Year vs Rainfall", "Place vs Rainfall"])
    val = st.slider("Filter data using Years", 1950, 2050)
    data = data.loc[data["Year"] >= val]

    
    if graph == "Year vs Rainfall":
        plt.figure(figsize=(15, 8))
        plt.scatter(data["Year"], data["Rainfall"])
        st.line_chart(data["Year"])
        st.bar_chart(data['Year'])
        plt.xlabel("Year")
        func()

    if graph == "Place vs Rainfall":
        plt.figure(figsize=(15, 8))
        labels = data["Station"]
        fig = plt.scatter(data["Station"], data["Rainfall"])
        plt.xticks(rotation=90)
        plt.xlabel("Place")
        st.bar_chart(data['Station'])
        func()
    #heatmap
    #st.write("Correlation Between Features")
    fig = plt.figure(figsize=(10,5))
    #plot heat map
    g = sns.heatmap(data.corr(), cmap="YlGnBu", annot=True)
    plt.title("HeatMap(Correlation Between Features)")
    st.write(fig)
    #g=sns.heatmap(corrmat,annot=True)
    fig = plt.figure(figsize=(10,5))
    sns.boxplot(data)
    #st.write("(Distribution of Data)")
    plt.title("Boxplot(Distribution of Data)")
    plt.xlabel("Feature")
    plt.ylabel("count")
    st.write(fig)
    df3 = data.drop(columns = ['Station'])
    fig = plt.figure(figsize=(10,5))
    sns.distplot(df3)
    plt.title("The variation in the data distribution")
    plt.xlabel("Feature")
    plt.ylabel("count")
    st.write(fig)
    

if nav == "Predictor":
    st.header("Guess Rainfall")

    # st.text_input("Enter Place for Prediction")
    val = st.date_input("Enter date for prediction")
    year = val.year
    month = val.month
    day = val.day
    place = st.selectbox("Enter Place for Prediction", [
        "Place",
        "Ambagan_ctg",
        "Barisal",
        "Bhola",
        "Bogra",
        "Chandpur",
        "Chittagong",
        "chuadanga",
        "Comilla",
        "CoxsBazar",
        "Dhaka",
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
        "Sitakunda",
        "Srimangal",
        "Sylhet",
        "sydpur",
        "Tangail",
        "Teknaf",
    ])

    if st.button("Predict"):
        #print(year, month, day)
        st.success(prediction(month, day, year,place))

if nav == "Contribute":
    st.header("Contribution to our dataset")

    val = st.date_input("Enter Date")
    day = val.day
    month = val.month
    year = val.year
    place = st.selectbox("Choose Place ", [
        "Place",
        "Ambagan_ctg",
        "Barisal",
        "Bhola",
        "Bogra",
        "Chandpur",
        "Chittagong",
        "chuadanga",
        "Comilla",
        "CoxsBazar",
        "Dhaka",
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
        "Sitakunda",
        "Srimangal",
        "Sylhet",
        "sydpur",
        "Tangail",
        "Teknaf",
    ])
    rainfall = st.number_input("Enter Rainfall")
    if st.button("Submit"):
        inde = df1[df1["Station"] == place]
        ind = inde.iloc[0]["StationIndex"]
        # st.write(ind)
        new_row = {'StationIndex': ind, 'Station': place, 'Year': year, 'Month': month, 'Day': day,
                   'Rainfall': rainfall}

        column_name = ['StationIndex', 'Station', 'Year', 'Month', 'Day', 'Rainfall']  # The name of the columns
        data1 = [ind, place, year, month, day, rainfall]  # the data

        with open('historical_rainfall_data.csv', 'a') as csv_file:
            dict_object = csv.DictWriter(csv_file, fieldnames=column_name)

            dict_object.writerow(new_row)
        st.success("Added Successfully")
