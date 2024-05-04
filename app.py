from flask import Flask, render_template, request, jsonify
import requests, plotly.graph_objs as go
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/', methods = ['POST'])
def Home():
    return render_template('home.html')

@app.route('/Track', methods=['POST'])
def track():
    return render_template('track.html')

@app.route('/AI-Buddy', methods = ['POST'])
def aibuddy():
    return render_template('aibuddy.html')

@app.route('/Community', methods=['POST'])
def community():
    return render_template('community.html')

def charts(d, cate=' ', val=' '):
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
        yaxis=dict(title=val)
    )
    bar_chart_fig = go.Figure(data=[bar_chart_trace], layout=bar_chart_layout)
    # Create pie chart
    pie_chart_trace = go.Pie(labels=labels, values=values)
    pie_chart_layout = go.Layout(
        title=''
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
        xaxis=dict(title=cate, tickvals=labels),  # Set tick values to specified labels
        yaxis=dict(title=val)
    )
    bar_chart_fig = go.Figure(data=[bar_chart_trace], layout=bar_chart_layout)
    return bar_chart_fig.to_html(include_plotlyjs='cdn')

def get_colours(rank, maxRank):#3 fields of colours are : titleColour, maxTitleColour, firstLetter
    colours = {}
    if 'grandmaster' in rank:
        colours['titleColour'] = 'red'
        if 'legendary' in rank:
            colours['firstLetter'] = 'black'
    elif 'candidate' in rank:
        colours['titleColour'] = 'pink'
    elif 'master' in rank:
        colours['titleColour'] = 'yellow'
    elif rank == 'expert':
        colours['titleColour'] = 'violet'
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
        colours['maxTitleColour'] = 'yellow'
    elif maxRank == 'expert':
        colours['maxTitleColour'] = 'blue'
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
                if item['verdict'] == 'OK' and 'rating' in problem :
                    rating = problem['rating']
                    ratings[rating] = ratings.get(rating, 0) + 1
                    
                if 'tags' in problem and isinstance(problem['tags'], list):
                    for tag in problem['tags']:
                        tags[tag] = tags.get(tag, 0) + 1

        verdicts_bar, verdicts_pie =  charts(verdicts)
        languages_bar, languages_pie = charts(languages)
        ratings_bar = rating_chart(ratings,'problem ratings' ,'no. of problems solved ')
        tags_bar, tags_pie = charts(tags,'problem tags' ,'no. of problems solved ')

        colours = get_colours( info_data.get('result')[0].get('rank'), info_data.get('result')[0].get('maxRank') )

        return render_template('results.html', info_data=info_data, verdicts_pie=verdicts_pie, languages_pie=languages_pie, ratings_bar=ratings_bar, tags_bar=tags_bar, colours=colours)
    else:
        return 'user not found'

if __name__ == '__main__':
    app.run(debug=True)
