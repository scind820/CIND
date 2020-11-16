# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pandas as pd
import time
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import dash_table
from fuzzywuzzy import fuzz 


app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server


df_fuzz = pd.DataFrame({'Title': [""], "Rating": [""]})






#load files
df = pd.read_csv("IMDb movies.csv")

#choose the columns needed
df = df[["imdb_title_id","title","original_title","year","date_published","genre","duration","country","language","director","production_company","actors","description","avg_vote"]]

#clean genre column  -  remove leading zeroes and fix spacing
df["genre"] = [str(x).strip() for x in df["genre"]] 
df["genre"] = [str(x).replace(" ","") for x in df["genre"]] # remove leading zeroes and fix spacing
df["genre"] = [str(x).replace(",",", ") for x in df["genre"]] #replaces with comma then space 



#fuzzy name matching
#create genere list
genre_list = df[["genre"]] 
genre_list

#sort and order list
df_genre_list = np.sort(genre_list["genre"].str.split(',', expand=True).fillna(''), axis=1) #replace null values with empty space?
df_genre_list = pd.DataFrame(df_genre_list).agg(','.join, 1).str.strip(',') #aggregate genre combinations
df_genre_list = pd.DataFrame(df_genre_list)
df_genre_list.rename(columns={0 : "genre"}, inplace=True)
df_genre_list["genre"] = [str(x).replace(" ","") for x in df_genre_list["genre"]] # remove leading zeroes and fix spacing
df_genre_list["genre"] = [str(x).replace(",",", ") for x in df_genre_list["genre"]] #replaces with comma then space
df_genre_list
df["genre_work"] = df_genre_list["genre"]
df_genre_list = df_genre_list.drop_duplicates() 
df_genre_list

#rename columns 
df = df[["original_title", "genre_work", "language", "description", "avg_vote", "duration","year","country","director","production_company"]]
df = df.rename(columns={"original_title": "Title","language": "Language", "description":"Description", "avg_vote":"Rating", "duration": "Duration", "year":"Year", "genre_work":"Genre"})
df["Rating"] = pd.to_numeric(df["Rating"], downcast="float").round(1) #set rating as a float with decimals 
df["Year"] = df["Year"].astype(str) #set year as a string
df["Duration"] = pd.to_numeric(df["Duration"], downcast="integer") #set duration as an integer






names = df["Title"].drop_duplicates() #exclude duplicate titles 

names = [{'label':name, 'value':name} for name in names]





































y = df_genre_list["genre"]

def fuzzyname_ratio(dflist,dfcompare):
    dataframecolumn = pd.DataFrame(dflist)
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







attributes = html.Div(
    [
        dbc.Row(
            [
            dbc.ListGroupItem([
                dbc.ListGroupItemHeading("Rating"),
                dbc.ListGroupItemText(id = "rating"),
            ]),
             dbc.ListGroupItem([
                dbc.ListGroupItemHeading("Genre"),
                dbc.ListGroupItemText(id = "Genre"),
            ]),
             dbc.ListGroupItem([
                dbc.ListGroupItemHeading("Duration"),
                dbc.ListGroupItemText(id = "Duration"),
            ]),
            ],
            align="center"
        )
    ]
)

description = html.Div(
    [
        dbc.Row(
            [
            dbc.ListGroupItem([
                dbc.ListGroupItemHeading("Description"),
                dbc.ListGroupItemText(id = "Description")
            ])
            ]
        )
    ]
)



def fuzz_table():
    layout = html.Div([
        dash_table.DataTable(
            id = "recc_table",
            columns = [{"name": i, "id": i} for i in df_fuzz],
            data = df_fuzz.to_dict('records'),
            style_as_list_view=True,
            style_cell={'padding': '5px'},
            style_header={
            'backgroundColor': 'white',
            'fontWeight': 'bold'
            },
            style_cell_conditional=[
                {
            'if': {'column_id': c},
            'textAlign': 'left'
            } for c in ['Title']
            ]
            )
    ])
    return layout





app.layout = dbc.Container(
    [
        
        html.H1("Movie Search Engine"),
        html.Hr(),

        dcc.Dropdown(
        id='demo-dropdown',
        options=names,
        value=''
    ),
        html.Hr(),
        html.H1(id = "title-string"),
        html.Hr(),
        attributes,
        html.Hr(),
        description,
        html.Hr(),
        html.H2("Movies Recommended For You!"),
        fuzz_table(),
        html.Div(id="tab-content", className="p-4"),
        
    ]
)


@app.callback(
            Output('rating', 'children'),
            [Input('demo-dropdown', 'value')]
        )
def output_text(text):
    rating = df.loc[df["Title"] == text, "Rating"].values[0]
    
    return str(rating)


@app.callback(
            Output('Duration', 'children'),
            [Input('demo-dropdown', 'value')]
        )
def output_text2(text2):
    duration = df.loc[df["Title"] == text2, "Duration"].values[0]
    return (str(duration))


@app.callback(
            Output('Genre', 'children'),
            [Input('demo-dropdown', 'value')]
        )
def output_text3(text3):
    genre = df.loc[df["Title"] == text3, "Genre"].values[0]
    return str(genre)


@app.callback(
            Output('Description', 'children'),
            [Input('demo-dropdown', 'value')]
        )
def output_text4(text4):
    description = df.loc[df["Title"] == text4, "Description"].values[0]
    return str(description)



@app.callback(
            Output('title-string', 'children'),
            [Input('demo-dropdown', 'value')]
        )
def output_text5(text5):
    
    return str(text5)



#table
@app.callback(
            Output('recc_table', 'data'),
            [Input('demo-dropdown', 'value')]
        )
def output_text6(text6):
    x = df.loc[df["Title"] == text6 ,"Genre"].values.tolist()
    y= df_genre_list["genre"]
    language = df.loc[df["Title"] == text6 ,"Language"].values.tolist()
    country = df.loc[df["Title"] == text6 ,"country"].values.tolist()
    director = df.loc[df["Title"] == text6 ,"director"].values.tolist()
    prodcomp = df.loc[df["Title"] == text6 ,"production_company"].values.tolist()
    
    
    
    
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
            
    dff = pd.merge(df,dff, left_on = "Genre", right_on = "compare", how = "left")
    dff = dff.loc[dff["Title"] != text6]   
    dff = dff.loc[dff["score"] != 0 | dff["score"].notnull()]
    dff = dff.sort_values(by='Year', ascending=False).sort_values(by='Rating', ascending=False)

    
    
    
    df1 = dff.loc[dff["Genre"].isin(x)]
    dfname = df1["Title"]
    df2 = dff.loc[~dff["Title"].isin(dfname)]
    
    
    dff = [df1,df2]
    dff = pd.concat(dff) 
    
    
    df1 = dff.loc[dff["country"].isin(country)]
    dfname = df1["Title"]
    df2 = dff.loc[~dff["Title"].isin(dfname)]
    
    dff = [df1,df2]
    dff = pd.concat(dff)
    
    
    df1 = dff.loc[dff["Language"].isin(language)]
    dfname = df1["Title"]
    df2 = dff.loc[~dff["Title"].isin(dfname)]
    
    dff = [df1,df2]
    dff = pd.concat(dff)
    
    df1 = dff.loc[dff["director"].isin(director)]
    dfname = df1["Title"]
    df2 = dff.loc[~dff["Title"].isin(dfname)]
    
    dff = [df1,df2]
    dff = pd.concat(dff)
    
    df1 = dff.loc[dff["production_company"].isin(prodcomp)]
    dfname = df1["Title"]
    df2 = dff.loc[~dff["Title"].isin(dfname)]
    
    dff = [df1,df2]
    dff = pd.concat(dff)
    
  

    
    
    df1 = dff.loc[dff["Genre"].isin(x) & dff["Language"].isin(language) & dff["country"].isin(country) & dff["director"].isin(director) & dff["production_company"].isin(prodcomp)].sort_values(by='Rating', ascending=False)
    dfname = df1["Title"]
    df2 = dff.loc[~dff["Title"].isin(dfname)]
    
    dff = [df1,df2]
    dff = pd.concat(dff)

    dff = dff[["Title", "Rating"]].drop_duplicates().head(10).sort_values(by='Rating', ascending=False)
    dff["Rating"] = dff["Rating"].round(1).astype(str)
    return dff.to_dict("records")




if __name__ == "__main__":
    app.run_server(host ='127.0.0.1', debug=False)