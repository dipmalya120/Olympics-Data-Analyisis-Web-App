import streamlit as st
import numpy as np
import pandas as pd
import preprocessor, helper
import plotly.express as px
import matplotlib.pyplot as plt 
import seaborn as sns
import plotly.figure_factory as ff

df = pd.read_excel('athlete_events.xlsx')
region_df = pd.read_excel('noc_regions.xlsx')

df = preprocessor.preprocess(df,region_df)

st.sidebar.markdown("<h1 style='text-align: center;'>Olympics Analysis</h>", unsafe_allow_html=True)
st.sidebar.image('Olympics-Logo-1986.png')

user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally','Overall Analysis','Country-wise Analysis','Athlete-wise Analysis')
)

# Medal Tally
if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years,country = helper.country_year_list(df)
    
    selected_year = st.sidebar.selectbox('Select Year', years)
    selected_country = st.sidebar.selectbox('Select Year', country)
    
    medal_tally = helper.fetch_medal_tally(df,selected_year,selected_country)

    # year-wise and country-wise analysis
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.markdown("## Overall Medal Tally")
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.markdown("## Medal Tally in " + str(selected_year) + " Olympics")
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.markdown("## "+selected_country + " overall performance")
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.markdown("## "+selected_country + " performance in " + str(selected_year) + " Olympics")
    st.table(medal_tally)
    
# Overall Analysis
if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.markdown("## **Top Statistics**")
    col1,col2,col3 = st.columns(3)
    with col1:
        st.markdown("### Editions")
        st.subheader(editions)
    with col2:
        st.markdown("### Hosts")
        st.subheader(cities)
    with col3:
        st.markdown("### Sports")
        st.subheader(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("### Events")
        st.subheader(events)
    with col2:
        st.markdown("### Nations")
        st.subheader(nations)
    with col3:
        st.markdown("### Athletes")
        st.subheader(athletes)

    st.text('''
    ''')
    st.text('''
    ''')
    st.markdown('## Insights')

    # Participating Nations over the years
    nations_over_time = helper.data_over_time(df,'region')
    fig = px.line(nations_over_time, x="Edition", y="region", labels={"Edition":"Year", "region":"Countries"})
    st.markdown("<h3 style='text-align: center;'>Participating Nations over the years</h3>", unsafe_allow_html=True)
    st.plotly_chart(fig)

    # Events over the years
    events_over_time = helper.data_over_time(df, 'Event')
    fig = px.line(events_over_time, x="Edition", y="Event", labels={"Edition":"Year", "Event":"Events"})
    st.markdown("<h3 style='text-align: center;'>Events over the years</h3>", unsafe_allow_html=True)
    st.plotly_chart(fig)

    # Athletes over the years
    athlete_over_time = helper.data_over_time(df, 'Name')
    fig = px.line(athlete_over_time, x="Edition", y="Name", labels={"Edition":"Year", "Name":"Participants"})
    st.markdown("<h3 style='text-align: center;'>Athletes over the years</h3>", unsafe_allow_html=True)
    st.plotly_chart(fig)

    # Events per Sport over time 
    st.markdown("<h3 style='text-align: center;'>Events per Sport over time</h3>", unsafe_allow_html=True)
    fig,ax = plt.subplots(figsize=(12,12))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),annot=True)
    st.pyplot(fig)

    # Most successful Athletes
    st.markdown("### Most successful Athletes")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')

    selected_sport = st.selectbox('Select a Sport',sport_list)
    x = helper.most_successful(df,selected_sport)
    st.table(x)

# Country-wise Analysis
if user_menu == 'Country-wise Analysis':

    st.sidebar.title('Country-wise Analysis')

    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country = st.sidebar.selectbox('Select a Country',country_list)

    # Medal Tally over the years
    country_df = helper.yearwise_medal_tally(df,selected_country)
    fig = px.line(country_df, x="Year", y="Medal")
    st.markdown("<h3 style='text-align: center;'>"+selected_country+" Medal Tally over the years</h3>", unsafe_allow_html=True)
    st.plotly_chart(fig)

    # Sport-wise performance
    st.markdown("<h3 style='text-align: center;'>"+selected_country+" Sport-wise performance</h3>", unsafe_allow_html=True)
    pt = helper.country_event_heatmap(df,selected_country)
    fig, ax = plt.subplots(figsize=(10,10))
    ax = sns.heatmap(pt,annot=True)
    st.pyplot(fig)

    # Top 10 athletes
    st.markdown("### Top 10 athletes of "+selected_country, unsafe_allow_html=True)
    top10_df = helper.most_successful_countrywise(df,selected_country)
    st.table(top10_df)

# Athlete-wise Analysis
if user_menu == 'Athlete-wise Analysis':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    # Distribution of Age
    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=800, height=400)
    st.markdown("<h3 style='text-align: center;'>Distribution of Age</h3>", unsafe_allow_html=True)
    st.plotly_chart(fig)

    # Sport-wise Distribution of Age (Gold Medalists)
    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=800, height=600)
    st.markdown("<h3 style='text-align: center;'>Sport-wise Distribution of Age (Gold Medalists)</h3>", unsafe_allow_html=True)
    st.plotly_chart(fig)

    # Height Vs Weight (Sport-wise)
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    st.markdown("<h3 style='text-align: center;'>Height Vs Weight (Sport-wise)</h3>", unsafe_allow_html=True)
    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = helper.weight_v_height(df,selected_sport)
    fig,ax = plt.subplots(figsize=(8,10))
    ax = sns.scatterplot(temp_df['Weight'],temp_df['Height'],hue=temp_df['Medal'],s=50)
    st.pyplot(fig)

    st.text('''
    ''')
    st.text('''
    ''')

    # Men v Women participation over the years
    st.markdown("<h3 style='text-align: center;'>Men v Women participation over the years</h3>", unsafe_allow_html=True)
    final = helper.men_vs_women(df)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    fig.update_layout(autosize=False, width=800, height=600)
    st.plotly_chart(fig)
