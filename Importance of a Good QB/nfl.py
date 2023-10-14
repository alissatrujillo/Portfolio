import streamlit as st  
import pandas as pd  
import numpy as np
import datetime

import nfl_data_py as nfl

## cd "ali/Documents/Grad/DSC 680/Projects/Project 2"

st.title('Quarterback Rating Data')

c1, c2 = st.columns([2,3])

def load_data(year):
    pbp = nfl.import_pbp_data([year])
    qbr = nfl.import_qbr(range(year-4, year+1))
    df_players = nfl.import_weekly_rosters([year])
    df_teams = nfl.import_team_desc()
    return pbp, qbr, df_players, df_teams

data_load_state = st.text('')

pbp, qbr, df_players, df_teams = load_data(2023)

data_load_state.text('')

today = datetime.date.today()
current_year = today.year

c1.subheader('Top QBR by Year')

yr = c1.selectbox(
   "Year",
   ("2023", "2022", "2021", "2020", "2019", "2018", "2017"),
   index=0,
   placeholder=str(current_year),
)

def get_qbr(year=current_year):
    qbr = nfl.import_qbr([year])
    reg_season = qbr.loc[qbr['season_type'] == 'Regular']
    starters = reg_season[~reg_season['rank'].isna()]
    qb_clean = starters[['rank', 'headshot_href', 'name_display', 'qbr_total']]
    qb_clean.rename(columns = {'rank':'Rank', 'headshot_href':'QB', 'name_display':'', 
                               'qbr_total':'QBR'}, inplace=True)
    qb_clean['Rank'] = qb_clean['Rank'].apply(np.floor)
    return qb_clean

try:
    year = int(yr)
except:
    year = current_year

qb_clean = get_qbr(year)

c1.dataframe(data=qb_clean, width=500, height=500,
            column_config={
                "QB": st.column_config.ImageColumn("QB", width=40,
                                                     help="Streamlit app preview screenshots"
                )
            },
            hide_index=True,
        )

#######

c2.subheader('QBR Over the Years')

top_player = qb_clean[''].iloc[0]
players = qb_clean['']

def multiyear_qbr(player=top_player):
    multi_year = []
    years_active = []
    
    for i in range(2006, current_year+1):
        qbr = nfl.import_qbr([i])
        reg_season = qbr.loc[qbr['season_type'] == 'Regular']
        player_data = reg_season[reg_season.isin([player]).any(axis=1)]
        
        try:
            current_qbr = player_data['qbr_total'].iloc[0]
        except:
            continue
            
        try:
            recent_team = player_data['team'].iloc[0]
        except:
            continue
        
        multi_year.append(current_qbr)
        years_active.append(i)
    
    player_df = pd.DataFrame({'Years Active': years_active, 'QBR': multi_year})
    player_df['Years Active'] = player_df['Years Active'].astype(str)
        
    return player_df, recent_team

qb = c2.selectbox(
   "Choose a Player:",
   (players),
   index=0,
   placeholder=str(top_player),
)

qbr_time, team = multiyear_qbr(qb)

team_colors = {'Cardinals': '#97233F',
               'Falcons': '#A71930',
               'Ravens': '#241773',
               'Bills': '#00338D',
               'Panthers': '#0085CA',
               'Bears': '#C83803',
               'Bengals': '#FB4F14',
               'Browns': '#311D00',
               'Cowboys': '#003594',
               'Broncos': '#FB4F14',
               'Lions': '#0076B6',
               'Packers': '#203731',
               'Texans': '#03202F',
               'Colts': '#002C5F',
               'Jaguars': '#D7A22A',
               'Chiefs': '#E31837',
               'Raiders': '#A5ACAF',
               'Chargers': '#0080C6',
               'Rams': '#003594',
               'Dolphins': '#008E97',
               'Vikings': '#4F2683',
               'Patriots': '#002244',
               'Saints': '#D3BC8D',
               'Giants': '#0B2265',
               'Jets': '#125740',
               'Eagles': '#004C54',
               'Steelers': '#FFB612',
               '49ers': '#AA0000',
               'Seahawks': '#69BE28',
               'Buccaneers': '#D50A0A',
               'Titans': '#4B92DB',
               'Commanders': '#5A1414'}

c2.line_chart(qbr_time, x='Years Active', y='QBR', color=team_colors[team])