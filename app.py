from flask import Flask, render_template, request, jsonify
import requests, statistics, plotly.graph_objs as go
from datetime import datetime
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/', methods = ['POST'])
def Home():
    return render_template('index.html')

@app.route('/Track', methods=['POST'])
def track():
    return render_template('track.html')

@app.route('/AI-Buddy', methods = ['POST'])
def aibuddy():
    return render_template('aibuddy.html')

@app.route('/Community', methods=['POST'])
def community():
    return render_template('community.html')

def charts(d, cate=' ', val=' ', ti = ' '):
    labels = list(d.keys())
    values = list(d.values())
    # Create bar chart
    bar_chart_trace = go.Bar(
        x=labels,
        y=values,
        marker=dict(color='rgb(100, 0, 0)')
    )
    bar_chart_layout = go.Layout(
        xaxis=dict(title=cate),
        yaxis=dict(title=val),
        title = ti
    )
    bar_chart_fig = go.Figure(data=[bar_chart_trace], layout=bar_chart_layout)
    # Create pie chart
    pie_chart_trace = go.Pie(labels=labels, values=values)
    pie_chart_layout = go.Layout(
        title=ti
    )
    pie_chart_fig = go.Figure(data=[pie_chart_trace], layout=pie_chart_layout)
    return bar_chart_fig.to_html(include_plotlyjs='cdn'), pie_chart_fig.to_html(include_plotlyjs='cdn')

def rating_chart(d, cate=' ', val=' '):
    labels = list(range(800, 3600, 100))
    values = [d[label] if label in d else 0 for label in labels]
    custom_colors = ['rgb(169, 169, 169)','rgb(169, 169, 169)','rgb(169, 169, 169)','rgb(169, 169, 169)', 'rgb(0, 128, 0)','rgb(0, 128, 0)', 'rgb(0, 255, 255)','rgb(0, 255, 255)', 'rgb(139, 0, 1139)','rgb(139, 0, 1139)','rgb(139, 0, 1139)', 'rgb(255, 140, 255)', 'rgb(255, 140, 255)', 'rgb(255, 200, 100)', 'rgb(255, 200, 100)', 'rgb(255, 165, 0)', 'rgb(255, 100, 100)', 'rgb(255, 100, 100)', 'rgb(255, 0, 0)', 'rgb(255, 0, 0)', 'rgb(255, 0, 0)', 'rgb(255, 0, 0)','rgb(139, 0, 0)','rgb(139, 0, 0)','rgb(139, 0, 0)','rgb(139, 0, 0)','rgb(139, 0, 0)','rgb(139, 0, 0)' ]
    bar_chart_trace = go.Bar(
        x=labels,
        y=values,
        marker=dict(color=custom_colors)
    )
    bar_chart_layout = go.Layout(
        xaxis=dict(title=cate, tickvals=labels),
        yaxis=dict(title=val)
    )
    bar_chart_fig = go.Figure(data=[bar_chart_trace], layout=bar_chart_layout)
    return bar_chart_fig.to_html(include_plotlyjs='cdn')

def verdict_chart(d):
    labels = list(d.keys())
    values = list(d.values())
    colors_map = {'OK': 'green', 'TIME_LIMIT_EXCEEDED': 'blue', 'MEMORY_LIMIT_EXCEEDED': 'yellow',
                  'WRONG_ANSWER': 'red', 'RUNTIME_ERROR': 'orange', 'COMPILATION_ERROR': 'purple', 
                  'SKIPPED': 'pink', 'CHALLENGED': 'black', 'PARTIAL':'cyan',
                  'IDLENESS_LIMIT_EXCEEDED':'violet', 'PRESENTATION_ERROR':'white'}
    colors = [colors_map[label] for label in labels]

    pie_chart_trace = go.Pie(
        labels=labels,
        values=values,
        marker=dict(colors=colors)
    )
    pie_chart_layout = go.Layout(
        title = ''
    )
    pie_chart_fig = go.Figure(data=[pie_chart_trace], layout=pie_chart_layout)
    return  pie_chart_fig.to_html(include_plotlyjs='cdn')

def rating_timeline(xplot,yplot,Xaxis,Yaxis):
    maxRatingIndex = 2
    rating=[1200,1400,1600,1900,2100,2300,2400,2600,3000]
    for r in yplot:
        if(maxRatingIndex > 8):
            maxRatingIndex = 12
            break
        if r > rating[maxRatingIndex-2]:
            maxRatingIndex += 1 
            
    fig_trace= go.Scatter(
        x=xplot,
        y=yplot,
        marker=dict(color='rgb(0,0,0)')
    )
    fig_layout = go.Layout(
        xaxis=dict(title=Xaxis),
        yaxis=dict(title=Yaxis,tickvals=rating),
    )
    fig = go.Figure(data=[fig_trace], layout=fig_layout)
    fig.add_hrect(
        y0=0,y1=1199,
        fillcolor="Silver", opacity=0.5,
        layer="below", line_width=0
    )
    fig.add_hrect(
        y0=1200,y1=1399,
        fillcolor="#77ff77", opacity=0.5,
        layer="below", line_width=0
    )
    if maxRatingIndex >= 3:
        fig.add_hrect(
            y0=1400,y1=1599,
            fillcolor="#77ddbb", opacity=0.5,
            layer="below", line_width=0
        )
    if maxRatingIndex >= 4:
        fig.add_hrect(
            y0=1600,y1=1899,
            fillcolor="#aaaaff", opacity=0.5,
            layer="below", line_width=0
        )
    if maxRatingIndex >= 5:
        fig.add_hrect(
            y0=1900,y1=2099,
            fillcolor="#ff88ff", opacity=0.5,
            layer="below", line_width=0
        )
    if maxRatingIndex >= 6:
        fig.add_hrect(
            y0=2100,y1=2299,
            fillcolor="#ffcc88", opacity=0.5,
            layer="below", line_width=0
        )
    if maxRatingIndex >= 7:
        fig.add_hrect(
            y0=2300,y1=2399,
            fillcolor="#ffbb55", opacity=0.5,
            layer="below", line_width=0
        )
    if maxRatingIndex >= 8:
        fig.add_hrect(
            y0=2400,y1=2599,
            fillcolor="#ffbb55", opacity=0.5,
            layer="below", line_width=0
        )
    if maxRatingIndex >= 9:
        fig.add_hrect(
            y0=2600,y1=2999,
            fillcolor="#ff3333", opacity=0.5,
            layer="below", line_width=0
        )
    if maxRatingIndex >= 10:
        fig.add_hrect(
            y0=3000,y1=5000,
            fillcolor="#aa0000", opacity=0.5,
            layer="below", line_width=0
        )
    return  fig.to_html(include_plotlyjs='cdn')

def get_colours(rank, maxRank):#3 fields of colours are : titleColour, maxTitleColour, firstLetter
    colours = {}
    if 'grandmaster' in rank:
        colours['titleColour'] = 'red'
        if 'legendary' in rank:
            colours['firstLetter'] = 'black'
    elif 'candidate' in rank:
        colours['titleColour'] = 'pink'
    elif 'master' in rank:
        if 'international' in rank : 
            colours['titleColour'] = 'rgb(255, 165, 0)'
        else:
            colours['titleColour'] = 'rgb(255, 200, 100)'
    elif rank == 'expert':
        colours['titleColour'] = 'rgb(139, 0, 1139)'
    elif rank == 'specialist':
        colours['titleColour'] = 'cyan'
    elif rank == 'pupil':
        colours['titleColour'] = 'green'
    elif rank == 'newbie':
        colours['titleColour'] = 'gray'
    
    if 'grandmaster' in maxRank:
        colours['maxTitleColour'] = 'red'
    elif 'candidate' in maxRank:
        colours['maxTitleColour'] = 'pink'
    elif 'master' in maxRank:
        if 'international' in maxRank : 
            colours['maxTitleColour'] = 'rgb(255, 165, 0)'
        else:
            colours['maxTitleColour'] = 'rgb(255, 200, 100)'
    elif maxRank == 'expert':
        colours['maxTitleColour'] = 'rgb(139, 0, 1139)'
    elif maxRank == 'specialist':
        colours['maxTitleColour'] = 'cyan'
    elif maxRank == 'pupil':
        colours['maxTitleColour'] = 'green'
    elif maxRank == 'newbie':
        colours['maxTitleColour'] = 'gray'

    if 'firstLetter' not in colours:
        colours['firstLetter'] = colours['titleColour']
    
    return colours

@app.route('/Track/Results', methods=['POST'])
def submit():
    handle = request.form['handle']
    url = f'https://codeforces.com/api/user.info?handles={handle}&checkHistoricHandles=false'
    response = requests.get(url)
    info_data = response.json()

    url = f'https://codeforces.com/api/user.status?handle={handle}'
    response = requests.get(url)
    status_data = response.json()

    url = f' https://codeforces.com/api/user.rating?handle={handle}'
    response = requests.get(url)
    rating_data = response.json()

    if info_data.get('status') == 'OK':
        #print(info_data)
        verdicts = {}
        languages = {}
        tags = {}
        ratings = {800: 0}
        
        for item in status_data['result']:
            if 'verdict' in item:
                verdict = item['verdict']
                verdicts[verdict] = verdicts.get(verdict, 0) + 1
            
            if 'programmingLanguage' in item:
                language = item['programmingLanguage']
                languages[language] = languages.get(language, 0) + 1
            
            if 'problem' in item and isinstance(item['problem'], dict):
                problem = item['problem']
                if item.get('verdict') == 'OK' and 'rating' in problem :
                    rating = problem['rating']
                    ratings[rating] = ratings.get(rating, 0) + 1

                if 'tags' in problem and isinstance(problem['tags'], list):
                    for tag in problem['tags']:
                        tags[tag] = tags.get(tag, 0) + 1
        
        tags = dict(sorted(tags.items(), key=lambda item: item[1], reverse=True))

        #time taken to solve a particular level in a contest
        
        time_taken = {800:[], 900:[], 1000:[], 1100:[], 1200:[], 1300:[], 1400:[], 1500:[], 1600:[], 1700:[], 1800:[], 1900:[], 2000:[], 2100:[], 2200:[], 2300:[], 2400:[],2500:[], 2600:[], 2700:[], 2800:[], 2900:[], 3000:[], 3100:[], 3200:[], 3300:[], 3400:[], 3500:[]}
        
        time_taken_index = {'A':[]}

        for item in status_data['result']:
            if item['author']['participantType'] == 'CONTESTANT' and item['verdict'] == 'OK':
                prob = item['problem']
                minutes = (item['relativeTimeSeconds'] ) // 60
                if prob.get('rating') is not None:
                    time_taken[prob['rating']].append(minutes)

                if prob.get('index') not in time_taken_index:
                    time_taken_index[prob['index']] = []
                time_taken_index[prob['index']].append((item['relativeTimeSeconds'] ) // 60)

        time_per_rating  = {}
        time_per_index = {}

        for rating in time_taken:
            if time_taken[rating]:
                time_per_rating[rating] = statistics.median(time_taken[rating])
            else:
                time_per_rating[rating] = 0  # Handle empty lists
      
        for index in time_taken_index:
            if time_taken_index[index]:
                time_per_index[index] = statistics.median(time_taken_index[index])
            else:
                time_per_index[index] = 0  # Handle empty lists
        time_per_index = dict(sorted(time_per_index.items(), key=lambda item: item[0]))

        rating_list=[]
        date_list=[]
        if rating_data['status']!='OK':
            return rating_data['comment']
        for items in rating_data['result']:
            rating_list.append(items['newRating'])
            date_list.append(datetime.utcfromtimestamp(items['ratingUpdateTimeSeconds']).strftime('%Y-%m-%d %H:%M:%S'))
        # print(rating_list)
        # print(date_list)
        scatter_plot = rating_timeline(date_list,rating_list,'','')
        
        verdicts_pie =  verdict_chart(verdicts)
        languages_bar, languages_pie = charts(languages)
        ratings_bar = rating_chart(ratings,'problem ratings' ,'no. of problems solved ')
        tags_bar, tags_pie = charts(tags,'problem tags' ,'no. of problems solved ')
        time_bar, time_pie= charts(time_per_rating, 'problem ratings', 'time taken to solve in a contest (in minutes)', 'Median time taken per rating')
        time_index_bar, time_index_pie= charts(time_per_index, 'problem indexes', 'time taken to solve in a contest (in minutes)', 'Median time taken per index')
        colours = get_colours( info_data.get('result')[0].get('rank'), info_data.get('result')[0].get('maxRank') )
        
        return render_template('results.html', info_data=info_data, verdicts_pie=verdicts_pie, languages_pie=languages_pie, ratings_bar=ratings_bar, tags_bar=tags_bar, time_bar = time_bar, time_index_bar=time_index_bar, scatter_plot=scatter_plot, colours=colours)
    else:
        return info_data.get('comment')

if __name__ == '__main__':
    app.run(debug=True)
