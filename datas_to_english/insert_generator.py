#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import os
from typing import MutableSequence, Any


# In[2]:


print(*list(filter(lambda x: x.endswith('.xlsx'),os.listdir())),sep="\n")


# ## Make an textfile for generating inserts

# In[3]:


# Default file name for inserts to be saved
INSERTS_FILE_NAME = "inserts.txt"
QUERIES = []


# In[4]:


# If file exist with inserts -> delete file and make file again
# If not exist -> Make file
if os.path.exists(INSERTS_FILE_NAME):
    os.remove(INSERTS_FILE_NAME)

# Make file and close file object
file = open(INSERTS_FILE_NAME,'w')
file.close()


# In[5]:


def make_str_value(value) -> str:
    return f"'{str(value)}'"
    
def insert_formatter(table_name,datas:MutableSequence,fields = None) -> str:
    query = ["INSERT", "INTO"]
    
    # If type of data is string -> require to add ''
    filtering_data_structures = list(map(lambda x: make_str_value(x),datas))
    
    # add table name to query
    query.append(table_name)
    
    # If field list is empty  -> pass else -> make field query
    query.append(f"({','.join(fields)})") if fields else True
    
    #. add VALUES to query
    query.append("VALUES")
    query.append(f"({','.join(filtering_data_structures)})")
    return ' '.join(query) + "\n"

def write_queries(message = None):
    with open(INSERTS_FILE_NAME,'a') as file:
        if message:
            file.write(f"--{message}\n")
        query = "\n".join(QUERIES)
        file.writelines(QUERIES)
        QUERIES.clear()


# ## Process : Player Information

# In[6]:


pi = pd.read_excel('kleague_player_information_renew.xlsx',index_col=0)
pi_table_name = 'player_info'


# In[7]:


for i in pi.index:
    datas = [
        pi['id'][i],
        pi['raname'][i],
        pi['teamid'][i],
        pi['league_type'][i],
        pi['포지션'][i],
        pi['배번'][i],
        pi['키'][i],
        pi['몸무게'][i],
        pi['생년월일'][i],
        pi['player_image'][i]
    ]
    QUERIES.append(insert_formatter(pi_table_name,datas))

# Save Queries to text file
write_queries("Player Information")


# ## Process : Player league history

# In[8]:


plh = pd.read_excel('kleague_player_league_history_renew.xlsx',index_col=0)
plh_table_name = 'player_prev_league'


# In[9]:


for i in plh.index:
    datas = [
        plh['id'][i],
        plh['리그'][i],
        plh['teamid'][i],
        plh['출장'][i],
        plh['득점'][i],
        plh['도움'][i],
        plh['골킥'][i],
        plh['코너킥'][i],
        plh['오프사이드'][i],
        plh['슈팅'][i],
        plh['파울'][i],
        plh['실점'][i],
        plh['경고'][i],
        plh['퇴장'][i]
    ]
    QUERIES.append(insert_formatter(plh_table_name,datas))

write_queries("Player previous league")


# ## Process : Previous league -> Some ambigious part related to primary key exist, but lack of datas, we decided to set leaguename as primary key

# In[10]:


pl = pd.read_excel("previous_league_history_renew.xlsx",index_col=0)
pl_table_name = 'previous_league'


# In[11]:


for i in pl.index:
    datas = [
        pl['리그'][i],
        pl['연도'][i]
    ]
    QUERIES.append(insert_formatter(pl_table_name,datas))
    
write_queries("Previous league history")


# ## Process : Team Homeground

# In[12]:


th = pd.read_excel("stadium_information.xlsx",index_col=0)
th_table_name = 'team_homeground'


# In[13]:


for i in th.index:
    datas = [
        th['teamid'][i],
        th['경기장'][i]
    ]
    QUERIES.append(insert_formatter(th_table_name,datas))
    
write_queries("Team homeground")


# ## Process : Team Info

# In[14]:


ti = pd.read_excel("team_information.xlsx",index_col=0)
ti_table_name = 'team_info'


# In[15]:


for i in ti.index:
    datas = [
        ti['teamid'][i],
        ti['클럽'][i],
        ti['리그'][i],
        ti['경기'][i],
        ti['승점'][i],
        ti['승'][i],
        ti['무'][i],
        ti['패'][i],
        ti['득점'][i],
        ti['실점'][i],
        ti['최근 홈 5경기'][i],
        ti['image'][i]
    ]
    QUERIES.append(insert_formatter(ti_table_name,datas))

write_queries("Team information")


# In[ ]:




