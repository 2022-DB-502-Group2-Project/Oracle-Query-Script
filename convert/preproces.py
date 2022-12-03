#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


import os,uuid


# In[3]:


reprocess_datas_directory = f"{os.getcwd()}/../datas_to_english"

if not os.path.isdir(reprocess_datas_directory):
    os.mkdir(reprocess_datas_directory)


# In[4]:


print(*list(filter(lambda x: x.endswith('.xlsx'),os.listdir())),sep="\n")


# ## Install dependencies
# 
# ```bash
# !conda install openpyxl -y
# !conda install pandas -y
# ```

# ## kleague_player_information

# In[5]:


df = pd.read_excel('kleague_player_information.xlsx',index_col=0)


# ### Preprocess country

# In[6]:


country = set(df['국적'])
country


# In[7]:


country_mapping = {
    '브라질' : 'Brazil',
    '한국' : 'Korea',
    '호주' : 'Australia'
}
df['국적'] = pd.Series(list(map(lambda x: country_mapping[x],df['국적'])))


# ### Preprocess team

# In[8]:


team = set(df['소속구단'])
team_map_str = { i : "" for i in team}
team_map_str


# In[9]:


# Team name mapping
team_mapping = {
     '울산': 'Ulsan',
     '전남': 'Jeonnam',
     '안산': 'Ansan',
     '서울': 'Seoul',
     '경남': 'Kyeongnam',
     '전북': 'Jeonbook',
     '대전': 'Daejeon',
     '인천': 'Incheon',
     '수원': 'Suwon',
     '충남아산': 'Choongnam_Asan',
     '광주': 'Gwangju',
     '서울E': 'Seoul_E',
     '김천': 'Kimcheon',
     '부산': 'Busan',
     '제주': 'Jeju',
     '대구': 'Daegu',
     '포항': 'Pohang',
     '안양': 'Anyang',
     '부천': 'Bucheon',
     '성남': 'Seongnam',
     '강원': 'Kangwon',
     '수원FC': 'Suwon_FC',
     '김포': 'Gimpo'
}

# Team id mapping
team_id_mapping = { i : uuid.uuid4() for i in team_mapping.values() }

df['소속구단'] = pd.Series(list(map(lambda x: team_mapping[x],df['소속구단'])))


# In[10]:


import faker

faker = faker.Faker()


# ### Preprocess player's name and ID randomly again

# In[11]:


player = df['이름']
random_name_set = list()

for _ in range(len(player)):
    n = faker.name()
    while True:
        if n not in random_name_set:
            random_name_set.append(n)
            break
        n = faker.name()
            
player_bucket = dict()
for i,j in enumerate(player):
    name = j.split('_')[0]
    if name in player_bucket.keys():
        name = f"{name}{len(list(filter(lambda x: x.startswith(name),player_bucket.keys()))) + 1}"
    player_bucket[name] = {
        'ran_name' : random_name_set[i],
        'id' : j.split('_')[1]
    }


# In[12]:


player_bucket


# In[13]:


col_raname = pd.Series(list(map(lambda x: x['ran_name'],player_bucket.values())),name="raname")


# In[14]:


col_id = pd.Series(list(map(lambda x: x['id'],player_bucket.values())),name="id")


# In[15]:


df_team_id = pd.Series(list(map(lambda x: team_id_mapping[x],df['소속구단'])),name="teamid")


# In[16]:


df = pd.concat([df,col_raname,col_id,df_team_id],axis=1)


# In[17]:


df


# In[18]:


df.to_excel(f'{reprocess_datas_directory}/kleague_player_information_renew.xlsx')


# ## kleague_player_league_history

# In[19]:


kplh = pd.read_excel('kleague_player_league_history.xlsx',index_col=0)


# In[20]:


kplh


# In[21]:


league = set(kplh['소속'])
# 현재 리그에 존재하는 팀들에 대한 히스토리만 필터링 
# -> K-league 홈페이지처럼 모든 데이터를 다 가지고 있는 상태가 아니므로 현재 있는 데이터에 대해서만 처리할 수 있도록 데이터를 가공한다.
n_kplh = kplh.copy().loc[kplh['소속'].isin(team_mapping.keys())]
# index reset for numbering
n_kplh.reset_index(drop=True, inplace=True)


# In[22]:


# 소속 전처리
n_kplh['소속'] = pd.Series(list(map(lambda x:team_mapping[x],n_kplh['소속'])),name='소속')
# 이름 전처리
n_kplh['이름'] = pd.Series(list(map(lambda x:x.split('_')[0],n_kplh['이름'])),name='이름')
# 현재 플레이어 명단에만 존재하는 


# In[23]:


n_kplh = n_kplh.loc[n_kplh['이름'].isin(player_bucket.keys())]


# In[24]:


raname = pd.Series([ player_bucket[i]['ran_name'] for i in n_kplh['이름']],name="raname")
_id = pd.Series([player_bucket[i]['id'] for i in n_kplh['이름']],name="id")
kplh_teamid_col = pd.Series(list(map(lambda x: team_id_mapping[x],n_kplh['소속'])),name="teamid")
n_kplh = pd.concat([n_kplh,raname,_id,kplh_teamid_col],axis=1)


# In[25]:


{ i : "" for i in set(n_kplh['리그'])}


# In[26]:


league_mapping = {
 '2009 K-리그': '2009 K-league',
 '현대오일뱅크 K리그 클래식 2016': 'Hyundai K-league Classic 2016',
 '하나원큐 K리그1 2022': 'Hanaone Q K-league1 2022',
 '하나원큐 K리그2 2019': 'Hanaone Q K-league2 2019',
 'KEB하나은행 K리그 챌린지 2017': 'KEB Hana K-league Challenge 2017',
 'KEB하나은행 K리그1 2018': 'KEB Hana K-league1 2018',
 '현대오일뱅크 K리그 2011': 'Hyundai K-league 2011',
 '하나원큐 K리그2 2021': 'Hanaone Q K-league2 2021',
 '현대오일뱅크 K리그 클래식 2014': 'Hyundai K-leageue Classic 2014',
 '하나원큐 K리그1 2020': 'Hanaone Q K-league1 2020',
 '현대오일뱅크 K리그 2012': 'Hyundai K-league 2012',
 '현대오일뱅크 K리그 챌린지 2016': 'Hyundai K-leageue Challenge 2016',
 '2001 포스코 K-리그': 'K-league POSCO 2001',
 '삼성 하우젠 K-리그 2006': 'Samsung K-league 2006',
 '삼성 하우젠 K-리그 2007': 'Samsung K-league 2007',
 '삼성 하우젠 K-리그 2005': 'Samsung K-league 2005',
 '현대오일뱅크 K리그 챌린지 2015': 'Hyundai K-leageue Challenge 2015',
 '현대오일뱅크 K리그 클래식': 'Hyundai K-leageue Classic',
 '현대오일뱅크 K리그 챌린지 2014': 'Hyundai K-leageue Challenge 2014',
 '2002 삼성 파브 K-리그': 'Samsung K-league 2002',
 '97 라피도컵 프로축구대회': '97 Rapidocup',
 '삼성 하우젠 K-리그 2008': 'Samsung K-league 2008',
 '쏘나타 K리그 2010 ': 'Sonata K-league 2010',
 '하나원큐 K리그1 2021': 'Hanaone Q K-league1 2021',
 '삼성 하우젠 K-리그 2004': 'Samsung K-league 2004',
 '2000 삼성디지털 K-리그': '2000 Samsung K-league',
 '96 라피도컵 프로축구대회': '96 Rapidocup',
 '98 현대컵 K-리그': '98 Hyundaicup K-league',
 '삼성 하우젠 K-리그 2003': 'Samsung K-league 2003',
 '하나원큐 K리그2 2022': 'Hanaone Q K-league2 2022',
 '하나원큐 K리그1 2019': 'Hanaone Q K-league1 2019',
 '현대오일뱅크 K리그 챌린지': 'Hyundai K-leageue Challenge',
 '하나원큐 K리그2 2020': 'Hanaone Q K-league2 2020',
 '현대오일뱅크 K리그 클래식 2015': 'Hyundai K-leageue Classic 2015',
 '99 바이코리아컵 K-리그': '99 By-Koreacup',
 'KEB하나은행 K리그2 2018': 'KEB Hana K-league2 2018',
 'KEB하나은행 K리그 클래식 2017': 'KEB Hana K-league Classic 2017'}

n_kplh['리그'] = pd.Series(list(map(lambda x: league_mapping[x],n_kplh['리그'])),name="리그")


# In[27]:


n_kplh.to_excel(f'{reprocess_datas_directory}/kleague_player_league_history_renew.xlsx')


# In[28]:


n_kplh


# ## Previous league history

# In[29]:


plh = pd.read_excel('previous_league_history.xlsx',index_col=0)


# In[30]:


# Filter league that exists in player's previous league
n_plh = plh.copy().loc[plh['리그'].isin(league_mapping.keys())]
n_plh.reset_index(drop=True, inplace=True)


# In[31]:


n_plh['리그'] = pd.Series(list(map(lambda x: league_mapping[x],n_plh['리그'])))


# In[32]:


n_plh.to_excel(f'{reprocess_datas_directory}/previous_league_history_renew.xlsx')


# ## Stadium Information

# In[33]:


sti = pd.read_excel('stadium_information.xlsx',index_col=0)


# In[34]:


sti['클럽'] = pd.Series(list(map(lambda x: team_mapping[x],sti['클럽'])))
sti_club_id = pd.Series(list(map(lambda x: team_id_mapping[x],sti['클럽'])),name="teamid")
sti = pd.concat([sti,sti_club_id],axis=1)


# In[35]:


{ i : "" for i in sti['경기장']}


# In[36]:


previous_league_mapping = {
 '울산문수축구경기장*': 'Ulsan Stadium',
 '전주월드컵경기장*': 'Jeonju worldcup Stadium',
 '포항스틸야드*': 'Pohang steal yard',
 '인천축구전용경기장*': 'Incheon Stadium',
 '제주월드컵경기장*': 'Jeju worldcup Stadium',
 '강릉종합경기장': 'Gangleung Stadium',
 '수원월드컵경기장*': 'Suwon worldcup Stadium',
 'DGB대구은행파크*': 'DGB Daegu Park',
 '서울월드컵경기장*': 'Seoul worldcup Stadium',
 '수원종합운동장': 'Suwon Stadium',
 '김천종합운동장': 'Kimcheon Stadium',
 '탄천종합운동장': 'Tancheon Stadium',
 '광주축구전용구장': 'Gwangju Stadium',
 '대전월드컵경기장*': 'Dajeon worldcup Stadium',
 '안양종합운동장': 'Anyang Stadium',
 '창원축구센터*': 'Changwon Stadium',
 '부천종합운동장': 'Bucheon Stadium',
 'Stadium Unknown': 'Choongnam Stadium',
 '목동운동장': 'Mokdong Stadium',
 '김포솔터축구장*': 'Gimpo Stadium',
 '와~스타디움': 'Wa~ Stadium',
 '구덕운동장': 'Goodeok Stadium',
 '광양축구전용구장*': 'Gwangyang Stadium'
}
sti['경기장'] = pd.Series(list(map(lambda x: previous_league_mapping[x],sti['경기장'])))


# In[37]:


sti.to_excel(f'{reprocess_datas_directory}/stadium_information.xlsx')


# ## Team information

# In[38]:


tei = pd.read_excel('team_information.xlsx',index_col=0)


# In[39]:


# Filter club
tei['클럽'] = pd.Series(list(map(lambda x: team_mapping[x],tei['클럽'])))
tei_club_id = pd.Series(list(map(lambda x: team_id_mapping[x],tei['클럽'])),name="teamid")
tei = pd.concat([tei,tei_club_id],axis=1)


# In[40]:


w_or_l = {
    '승' : 'W',
    '패' : 'L',
    '무' : 'D'
}

tei['최근 홈 5경기'] = pd.Series(list(map(lambda x: ' '.join(list(map(lambda y: w_or_l[y],x.split(' ')))), tei['최근 홈 5경기'])))


# In[41]:


tei.to_excel(f'{reprocess_datas_directory}/team_information.xlsx')

