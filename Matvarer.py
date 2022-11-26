import pandas as pd
import streamlit as st
from datetime import datetime
from datetime import date
import os 
import schedule
import time


def create_time():
    current_time = datetime.now().strftime("%H:%M:%S")
    with open('readme.txt', 'w') as f:
        f.write(current_time)
        
def show_time():
    with open('readme.txt') as f:
        lines = f.readlines()
    return lines

schedule.every().hour.at(":00").do(create_time)


while True:
    schedule.run_pending()
    time.sleep(5)
    h = show_time()
    st.write(h)

    
def Registrer_vare():
    Dato = datetime.now().strftime("%d-%m-%Y")
    Dato_tekst = datetime.now().strftime("%d-%b-%Y")
    Dag = datetime.now().day
    Month = datetime.now().month
    Year = datetime.now().year
    Datetime_Idag = date(Year,Month,Dag)
    New_row = [Ny_vare,Dato,Dato_tekst]
    new_df = pd.DataFrame([New_row],columns=["Vare","Dato åpnet","Dato åpnet "])
    try:
        df = df = pd.read_excel("Overview.xlsx")[["Vare","Dato åpnet"]]
        df = pd.concat([df,new_df]).reset_index()[["Vare","Dato åpnet"]]
        df["Dag"] = [df["Dato åpnet"][i].split("-")[0] for i in range(len(df))]
        df["Month"] = [df["Dato åpnet"][i].split("-")[1] for i in range(len(df))]
        df["Year"] = [df["Dato åpnet"][i].split("-")[2] for i in range(len(df))]
        df["Formatted date"] = [date(int(df["Year"][i]),int(df["Month"][i]),int(df["Dag"][i])) for i in range(len(df))]
        df["Dager i kjøleskapet"] = (df["Formatted date"] - Datetime_Idag)
        df["Dager i kjøleskapet"] = [df["Dager i kjøleskapet"][i].days for i in range(len(df))]
        df.to_excel("Overview.xlsx")
    except:
        new_df["Dag"] = [new_df["Dato åpnet"][i].split("-")[0] for i in range(len(new_df))]
        new_df["Month"] = [new_df["Dato åpnet"][i].split("-")[1] for i in range(len(new_df))]
        new_df["Year"] = [new_df["Dato åpnet"][i].split("-")[2] for i in range(len(new_df))]
        new_df["Formatted date"] = [date(int(new_df["Year"][i]),int(new_df["Month"][i]),int(new_df["Dag"][i])) for i in range(len(new_df))]
        new_df["Dager i kjøleskapet"] = (new_df["Formatted date"] - Datetime_Idag)
        new_df["Dager i kjøleskapet"] = [new_df["Dager i kjøleskapet"][i].days for i in range(len(new_df))]
        new_df.to_excel("Overview.xlsx")

st.title("Oversikt over mat")

#st.image("Først.jpg")

option = st.radio(
      'Velg modus',
             ('Vis oversikt','Registrer vare', 'Nullstill'))

if option == 'Registrer vare':
    Ny_vare = st.text_input("Ny vare")
    Registrer = st.button('Registrer matvare')
    if Registrer:
        Registrer_vare()
        st.write("Vare registrert!")



        
elif option == "Vis oversikt":
    if "Overview.xlsx" in os.listdir():
        col1, col2 = st.columns(2)
    
        with col1:
           st.header("Oversikt")
           if "Overview.xlsx" in os.listdir():
               df = pd.read_excel("Overview.xlsx")[["Vare","Dato åpnet"]]
               st.table(df)

        with col2:
            st.header("Registrte varer")
            st.metric(label="Antall", value=len(df))
#'st.image("https://static.streamlit.io/examples/dog.jpg")


    else:
        st.write("Finnes ingen fil")


if option == 'Nullstill':
    slett = st.button("Reset fil")
    if slett:
        try:
            os.remove("Overview.xlsx")
        except:
            st.write("Allerede nullstilt")
       
    
