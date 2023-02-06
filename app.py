import pickle
import numpy as np
import streamlit as st
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from plotly import graph_objs as go
import csv
from pathlib import Path
import streamlit_authenticator as stauth


st.title("Rainfall Predictor")

#data = pd.read_csv("H:/ai/project/historical_rainfall_data.csv")
data = pd.read_csv('historical_rainfall_data.csv')
df = data["Station"]
df1= data[{"StationIndex","Station"}]
df1.drop_duplicates(inplace = True)


nav = st.sidebar.radio("Navigation", ["Home", "Predictor", "Contribute"])
# st.image("H:/ai/project/weather.jfif")
# loaded_model = pickle.load(open('H:/ai/project/trained_model.sav', 'rb'))
st.image('image//weather.jfif')
loaded_model = pickle.load(open('trained_model.sav', 'rb'))


def func():
    plt.ylim(0)
    plt.ylabel("Rainfall")
    plt.tight_layout()
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot()
    return


def prediction(monthPredict, dayPredict, yearPredict,place):

    inde = df1[df1["Station"] == place]
    ind=inde.iloc[0]["StationIndex"]  
    input_data = (ind,monthPredict, dayPredict)

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
        plt.xlabel("Year")
        func()

    if graph == "Place vs Rainfall":
        plt.figure(figsize=(15, 8))
        labels = data["Station"]
        fig = plt.scatter(data["Station"], data["Rainfall"])
        plt.xticks(rotation=90)
        plt.xlabel("Place")
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
        s = prediction(month, day, year,place) 
        if s<=1 :
            p="Wow it's Sunny day"
            st.success( p )
            st.image('image//sunny.jpg')
        elif s>1 and s<=10:
            p = "Light Rain"
            st.success( p )
            st.image('image//Light.jpeg')
        elif s>10 and s <=22 :
            p = "Moderate Rain"
            st.success( p )
            st.image('image//Moderate.jfif')
        elif s>22 and s<=44 :
            p = "Moderate Heavy Rain"
            st.success( p )
            st.image('image//ModerateHeavy.jfif')
        elif s <= 88:
            p ="Heavy Rain"
            st.success( p )
            st.image('image//Heavy.jfif')
        else :
            p = "Very Heavy Rain"
            st.success( p )
            st.image('image//VeryHeavy.jpg')
        st.balloons()
if nav == "Contribute":
    # ---------user authentication---------
    names = ["Admin", "Aipr"]
    usernames = ["admin", "person"]

    file_path = Path(__file__).parent/"hashed_pw.pkl"
    with file_path.open("rb") as file:
        hashed_passwords = pickle.load(file)

    credentials = {"usernames": {}}

    for uname, name, pwd in zip(usernames, names, hashed_passwords):
        user_dict = {"name": name, "password": pwd}
        credentials["usernames"].update({uname: user_dict})

    authenticator = stauth.Authenticate(credentials, "cokkie_name", "random_key", cookie_expiry_days=30)

    name , authentication_status, username =authenticator.login("Login","main")
    authenticator.logout("Logout","sidebar")


    if authentication_status == False :
        st.error("Username/password is wrong")
    if authentication_status == None:
        st.warning("Pleas enter username and password")
    if authentication_status:
        st.header("Contribution to our dataset")

        val =st.date_input("Enter Date")
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
        rainfall =st.number_input("Enter Rainfall")


        if st.button("Submit"):
            inde = df1[df1["Station"] == place]
            ind=inde.iloc[0]["StationIndex"]
            #st.write(ind)
            new_row = {'StationIndex':ind,'Station': place, 'Year':year, 'Month':month, 'Day':day ,'Rainfall':rainfall}

            column_name = ['StationIndex', 'Station', 'Year', 'Month','Day', 'Rainfall'] #The name of the columns
            data1 = [ind,place,year,month,day,rainfall] #the data

            with open('historical_rainfall_data.csv', 'a') as csv_file:
                dict_object = csv.DictWriter(csv_file, fieldnames=column_name)

                dict_object.writerow(new_row)
            st.success("Added Successfully")

    # ----------Request access form------------
    if not authentication_status:
        st.header(":mailbox: Request Access")
        access_form="""
        <form action="https://formsubmit.co/kabir73826@gmail.com" method="POST">
        <input type="hidden" name="_captcha" value="false">
        <input type="text" name="name" placeholder="your name" required>
        <input type="email" name="email" placeholder="your email" required>
        <textarea name="message" placeholder="State your interest"></textarea>
        <button type="submit">Send</button>
        </form>
        """
        st.markdown(access_form,unsafe_allow_html=True)

        def local_css(file_name):
            with open(file_name) as f:
                st.markdown(f"<style>{f.read()}</style>",unsafe_allow_html = True)

        local_css("style/style.css")

