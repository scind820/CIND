#!/usr/bin/env python
# coding: utf-8

# In[1]:


#import libraries

import pandas as pd
import numpy as np
import os

#load files
df_movies = pd.read_csv("IMDb movies.csv")

#choose the columns needed
df_movies = df_movies[["imdb_title_id","title","original_title","year","date_published","genre","duration","country","language","director","production_company","actors","description","avg_vote"]]


# In[76]:


cnt = df_movies.count
print(cnt)


# In[4]:


df_graoh_genre =  df_movies[["genre", "avg_vote"]]

df_graoh_genre

df_graoh_genre = pd.DataFrame(df_graoh_genre.genre.str.split(',').tolist(), index=df_graoh_genre.avg_vote).stack()
df_graoh_genre = df_graoh_genre.reset_index()[[0, 'avg_vote']] # var1 variable is currently labeled 0
df_graoh_genre.columns = ["genre", 'avg_vote'] 
df_graoh_genre['genre'] = df_graoh_genre['genre'].str.strip()

# outlier_genres = ["Documentary","News","Adult", "Reality-TV"]

# df_graoh_genre= df_graoh_genre.loc[~df_graoh_genre["genre"].isin(outlier_genres)]


pysqldf = lambda q: sqldf(q, globals())

df_graoh_genre_avg = pysqldf("SELECT genre, avg(avg_vote) FROM df_graoh_genre group by genre;").sort_values(by = 'avg(avg_vote)', ascending = False) 


# In[5]:



from pandasql import sqldf
pysqldf = lambda q: sqldf(q, globals())

df_graoh_genre_count = pysqldf("SELECT genre, count(genre) FROM df_graoh_genre group by genre;").sort_values(by = 'count(genre)', ascending = False) 

 
df_graoh_genre_avg


# In[ ]:


plt.bar("genre", "avg(avg_vote)", data = df_graoh_genre_avg, color = "blue")
plt.xlabel("Genre")
plt.xticks(rotation = 90)
plt.ylabel("Average Number of Movies")
plt.title("Graph 3: Average Number of Movies per Genre(pre-outlier omission)")

plt.show()

fig = px.bar(df_graoh_genre_avg, x='genre', y='avg(avg_vote)',
             labels={'genre':'Genre', 'avg(avg_vote)': "Average Number of Movies"}, height=400)
fig.update_layout(title_text='Graph 3: Average Number of Movies per Genre(pre-outlier omission)')
fig.show()
plt.show()


# In[114]:


import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


plt.bar("genre", "count(genre)", data = df_graoh_genre_count, color = "blue")
plt.xlabel("Genre")
plt.xticks(rotation = 90)
plt.ylabel("Number of Movies")
plt.title(" Graph 1: Number of Movies per Genre(pre-outlier omission)")

plt.show()



fig = px.bar(df_graoh_genre_count, x='genre', y='count(genre)',
             labels={'genre':'Genre', 'avg(duration)': "Number of Movies"}, height=400)
fig.update_layout(title_text='Graph 1: Number of Movies per Genre(pre-outlier omission)')
fig.show()
plt.show()


# In[ ]:


df_graph_year_duration = df_movies[["genre","duration"]]

df_graph_year_duration = pd.DataFrame(df_graph_year_duration.genre.str.split(',').tolist(), index=df_graph_year_duration.duration).stack()
df_graph_year_duration = df_graph_year_duration.reset_index()[[0, "duration"]] # var1 variable is currently labeled 0
df_graph_year_duration.columns = ["genre","duration"] 
df_graph_year_duration['genre'] = df_graph_year_duration['genre'].str.strip()



outlier_genres = ["Documentary","News","Adult", "Reality-TV"]

df_graoh_genre= df_graoh_genre.loc[~df_graoh_genre["genre"].isin(outlier_genres)]

df_graph_year_duration = df_graph_year_duration.loc[~df_graph_year_duration["genre"].isin(outlier_genres)]

#graph duration average 
df_graph_year_duration = pysqldf("SELECT genre, avg(duration) FROM df_graph_year_duration group by genre;").sort_values(by = 'avg(duration)', ascending = False)
df_graph_year_duration

fig = px.bar(df_graph_year_duration, x='genre', y='avg(duration)',
             labels={'genre':'Movie Genre', 'avg(duration)': "Average Duration (Minute)"}, height=400)
fig.update_layout(title_text='Graph 5: Average Duration (Minutes) per Genre')
fig.show()
plt.show()


# In[116]:


df_graph_year_duration = df_movies[["genre","year"]]

df_graph_year_duration = pd.DataFrame(df_graph_year_duration.genre.str.split(',').tolist(), index=df_graph_year_duration.year).stack()
df_graph_year_duration = df_graph_year_duration.reset_index()[[0, "year"]] # var1 variable is currently labeled 0
df_graph_year_duration.columns = ["genre","year"] 
df_graph_year_duration['genre'] = df_graph_year_duration['genre'].str.strip()



outlier_genres = ["Documentary","News","Adult", "Reality-TV"]

df_graoh_genre= df_graoh_genre.loc[~df_graoh_genre["genre"].isin(outlier_genres)]

df_graph_year_duration = df_graph_year_duration.loc[~df_graph_year_duration["genre"].isin(outlier_genres)]

#graph duration average 
df_graph_year_duration = pysqldf("SELECT year, count(year) FROM df_graph_year_duration group by year;").sort_values(by = 'year', ascending = True)
df_graph_year_duration

fig = px.line(df_graph_year_duration, x="year", y="count(year)",labels={'year':'Release Year', 'count(year)': "Number of Movies"}, title='Graph 6: Number of Movies Released Per Year')
fig.show()


# In[8]:


#clean genre column  -  remove leading zeroes and fix spacing
df_movies["genre"] = [str(x).strip() for x in df_movies["genre"]]
df_movies["genre"] = [str(x).replace(" ","") for x in df_movies["genre"]]
df_movies["genre"] = [str(x).replace(",",", ") for x in df_movies["genre"]]

#create working genre column for fuzzy matching
df_movies["genre_work"] = [str(x).strip() for x in df_movies["genre"]]
df_movies["genre_work"] = [str(x).replace(" ","") for x in df_movies["genre_work"]]

df_movies


# In[17]:


#fuzzy name matching
#create genere list
genre_list = df_movies[["genre"]]
genre_list

#sort and order list
df_genre_list = np.sort(genre_list["genre"].str.split(',', expand=True).fillna(''), axis=1)
df_genre_list = pd.DataFrame(df_genre_list).agg(','.join, 1).str.strip(',')
df_genre_list = pd.DataFrame(df_genre_list)
df_genre_list.rename(columns={0 : "genre"}, inplace=True)
df_genre_list["genre"] = [str(x).replace(" ","") for x in df_genre_list["genre"]]
df_genre_list["genre"] = [str(x).replace(",",", ") for x in df_genre_list["genre"]]
df_genre_list
df_movies["genre_work"] = df_genre_list["genre"]
df_genre_list = df_genre_list.drop_duplicates()
df_genre_list


# In[ ]:


drama, news, 


# In[ ]:


from fuzzywuzzy import fuzz 

x = ["History, Drama"]
y = df_genre_list["genre"]

def fuzzyname_ratio(dflist,dfcompare):
    idataframecolumn = pd.DataFrame(dflist)
    dataframecolumn.columns = ['Match']

    compare = pd.DataFrame(dfcompare)
    compare.columns = ['compare']

    dataframecolumn['Key'] = 1
    compare['Key'] = 1
    combined_dataframe = dataframecolumn.merge(compare,on="Key",how="left")
    combined_dataframe = combined_dataframe[~(combined_dataframe.Match==combined_dataframe.compare)]

    def partial_match(x,y):
        return(fuzz.ratio(x,y))
    partial_match_vector = np.vectorize(partial_match)

    combined_dataframe['score']=partial_match_vector(combined_dataframe['Match'],combined_dataframe['compare'])
    combined_dataframe = combined_dataframe[combined_dataframe.score>=80]

    return combined_dataframe


def fuzzyname_token_set(dflist,dfcompare):
    dataframecolumn = pd.DataFrame(dflist)
    dataframecolumn.columns = ['Match']

    compare = pd.DataFrame(dfcompare)
    compare.columns = ['compare']

    dataframecolumn['Key'] = 1
    compare['Key'] = 1
    combined_dataframe = dataframecolumn.merge(compare,on="Key",how="left")
    combined_dataframe = combined_dataframe[~(combined_dataframe.Match==combined_dataframe.compare)]

    def partial_match(x,y):
        return(fuzz.token_set_ratio(x,y))
    partial_match_vector = np.vectorize(partial_match)

    combined_dataframe['score']=partial_match_vector(combined_dataframe['Match'],combined_dataframe['compare'])
    combined_dataframe = combined_dataframe[combined_dataframe.score>=80]

    return combined_dataframe


def fuzzyname_partial(dflist,dfcompare):
    dataframecolumn = pd.DataFrame(dflist)
    dataframecolumn.columns = ['Match']

    compare = pd.DataFrame(dfcompare)
    compare.columns = ['compare']

    dataframecolumn['Key'] = 1
    compare['Key'] = 1
    combined_dataframe = dataframecolumn.merge(compare,on="Key",how="left")
    combined_dataframe = combined_dataframe[~(combined_dataframe.Match==combined_dataframe.compare)]

    def partial_match(x,y):
        return(fuzz.partial_ratio(x,y))
    partial_match_vector = np.vectorize(partial_match)

    combined_dataframe['score']=partial_match_vector(combined_dataframe['Match'],combined_dataframe['compare'])
    combined_dataframe = combined_dataframe[combined_dataframe.score>=80]

    return combined_dataframe

fuzzyname_partial(x,y)


# In[ ]:


df_test = df_movies.merge(combined_dataframe, how = "left", left_on = "genre_work", right_on = "Match")
df_test.loc[df_test["Key"]==1]


# In[63]:


df_movies.loc[df_movies["title"] == "1987","genre"].values.tolist()


# In[74]:


x = ["Comedy"]
y = df_genre_list["genre"]
language = ["English"]
lang = "English"
if len(fuzzyname_ratio(x,y).index) != 0:
    dff = pd.DataFrame(fuzzyname_ratio(x,y))
    print (dff)
elif len(fuzzyname_ratio(x,y).index) == 0:
    if len(fuzzyname_token_set(x,y).index) != 0:
        dff = pd.DataFrame(fuzzyname_token_set(x,y))
        print (dff)
    elif len(fuzzyname_token_set(x,y).index) == 0:
        dff = pd.DataFrame(fuzzyname_partial(x,y))
        print (dff)
dff
dff = pd.merge(df_movies,dff, left_on = "genre_work", right_on = "compare", how = "left")
dff = dff.sort_values(by='avg_vote', ascending=False).sort_values(by='score', ascending=False)


df1 = dff.loc[dff["language"].isin(language)]
dfname = df1["title"]
df2 = dff.loc[~dff["title"].isin(dfname)]
    
dff = [df1,df2]
dff = pd.concat(dff)


# dff = dff[["title", "avg_vote"]].head()
dff.head()


# In[66]:


dff


# In[ ]:


names = df_movies["title"].drop_duplicates()

names = [{'label':name, 'value':name} for name in names]


# In[ ]:


df_movies.loc[df_movies["title"] != df_movies["original_title"]].head(100)


# In[ ]:





# In[ ]:




