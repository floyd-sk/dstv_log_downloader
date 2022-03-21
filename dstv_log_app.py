import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

st.title('DStv Premiership Log Table Downloader')

st.image('resources/dstv.jpg',use_column_width=True)

st.markdown("""
This app performs simple webscraping of DStv premiership log tables from the EuroSport website and makes the tables downloadable as a CSV file customizable by team(s) and season.
* **Python libraries:** base64, pandas, streamlit
* **Data source:** [EuroSport website](https://www.eurosport.com/)
""")

st.sidebar.header('Select Season and Team(s) of choice:')
#selected_season = st.sidebar.selectbox('Season', list(["2020/21", "2019/20", "2018/19", "2017/18", "2016/17", "2015/16", "2014/15", "2013/14", "2012/13"]))
selected_season = st.sidebar.selectbox('Season', list(["2021-2022", "2020-2021"]))

#def load_data(season):
    #url = 'https://www.psl.co.za/matchcentre?type=Log'
    #html = pd.read_html(url, header = 0)
    #df = html[1]
    #df.rename(columns={'2020/21 2019/20 2018/19 2017/18 2016/17 2015/16 2014/15 2013/14 2012/13': 'Team'}, inplace=True)
    #df['Team'] = df['Team'].str.replace('\d+', '') #Replace numerical values in team names
    #df.columns = df.columns.str.strip() #Removes whitespace both-ends
    #teamstats = df
    #return teamstats # Same as df
#teamstats = load_data(selected_season)

def load_data(season):
    url = "https://www.eurosport.com/football/dstv-premiership/" + str(season) + "/standing.shtml"
    html = pd.read_html(url, header = 0)
    df = html[0]
    df = df.drop(['Unnamed: 0', 'Last 5', '+/-'], axis=1)
    #df.rename(columns={'2020/21 2019/20 2018/19 2017/18 2016/17 2015/16 2014/15 2013/14 2012/13': 'Team'}, inplace=True)
    #df['Team'] = df['Team'].str.replace('\d+', '') #Replace numerical values in team names
    df.columns = df.columns.str.strip() #Removes whitespace both-ends
    teamstats = df
    return teamstats # Same as df
teamstats = load_data(selected_season)

# Sidebar - Team selection
sorted_unique_team = sorted(teamstats.Teams.unique())
selected_team = st.sidebar.multiselect('Team', sorted_unique_team, sorted_unique_team)

# Filtering data
df_selected_team = teamstats[(teamstats.Teams.isin(selected_team))]

st.write("---")

st.header('Preview Log Table')
st.write('Team(s) Selected: ' + str(df_selected_team.shape[0]))
#st.write('Team(s) Selected: ' + str(df_selected_team.shape[0]) + ' rows and ' + str(df_selected_team.shape[1]) + ' columns.') to be looked at...
st.dataframe(df_selected_team)

# Download DStv Premiership Log Table
# https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="{selected_season}_dstv_log_table.csv">Download CSV File</a>'
    return href

st.markdown(filedownload(df_selected_team), unsafe_allow_html=True)

st.write("---")

st.info('Contact Developer')

# Floyd
st.markdown("<h3 style='text-align: center;'>Floyd Skakane</h3>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Aspiring Data Scientist</p>", unsafe_allow_html=True)
st.image('resources/Floyd.jpeg', width=120)
st.markdown("<a href='http://www.linkedin.com/in/floyd-skakane-0179a597/' target='_blank'>LinkedIn</a>", unsafe_allow_html=True)
st.markdown("<a href='https://github.com/floyd-sk' target='_blank'>GitHub</a>", unsafe_allow_html=True)

#---------------------------------------------------IGNORE----------------------------------------------------#

# Heatmap
#if st.button('Intercorrelation Heatmap'):
    #st.set_option('deprecation.showPyplotGlobalUse', False)
    #st.header('Intercorrelation Matrix Heatmap')
    #df_selected_team.to_csv('output.csv',index=False)
    #df = pd.read_csv('output.csv')

    #corr = df.corr()
    #mask = np.zeros_like(corr)
    #mask[np.triu_indices_from(mask)] = True
    #with sns.axes_style("white"):
        #f, ax = plt.subplots(figsize=(7, 5))
        #ax = sns.heatmap(corr, mask=mask, vmax=1, square=True)
    #st.pyplot()

#---------------------------------------------------IGNORE------------------------------------------------------#