from flask import Flask, Markup, render_template, request, flash
import os
import json

app = Flask(__name__) #__name__ = "__main__" if this is the file that was run.  Otherwise, it is the name of the file (ex. webapp)

@app.route("/")
def render_main():
    return render_template('home.html')

@app.route("/largestDams")
def render_largest_dams():
    with open('hydropower.json') as dams_data:
        dams = json.load(dams_data)
    longestData = get_longest_dam(dams)
    tallestData = get_tallest_dam(dams)
    return render_template('largest-dams.html', longest = longestData[0], length = longestData[1], tallest = tallestData[0], height = tallestData[1])

@app.route("/dataByDam")
def render_data_by_dam():
    with open('hydropower.json') as dams_data:
        dams = json.load(dams_data)
    if 'dam' in request.args:
        d = get_dam_data(dams, request.args['dam'])
        return render_template('data-by-dam.html', options = get_dam_options(dams), name = d["Identity"]["Name"], year = d["Identity"]["Project"]["Year"], state = d["Location"]["State"], length = d["Dimensions"]["Crest Length"], height = d["Dimensions"]["Structural Height"])
    return render_template('data-by-dam.html', options = get_dam_options(dams))

@app.route("/damsPerState")
def render_dams_per_state():
    with open('hydropower.json') as dams_data:
        dams = json.load(dams_data)
    if 'state' in request.args:
        return render_template('dams-per-state.html', options = get_state_options(dams), numDams = get_dams_per_state(dams, request.args['state']), state = request.args['state'])
    return render_template('dams-per-state.html', options = get_state_options(dams))

def get_dam_options(dams):
    names = []
    options = ""
    for d in dams:
        if d["Identity"]["Name"] not in dams:
            names.append(d["Identity"]["Name"])
            options += Markup("<option value=\"" + d["Identity"]["Name"] + "\">" + d["Identity"]["Name"] + "</option>")
    return options

def get_state_options(dams):
    states = []
    options = ""
    for d in dams:
        if d["Location"]["State"] not in states:
            states.append(d["Location"]["State"])
            options += Markup("<option value=\"" + d["Location"]["State"] + "\">" + d["Location"]["State"] + "</option>")
    return options

def get_dam_data(dams, selected_dam):
    for d in dams:
        if d["Identity"]["Name"] == selected_dam:
            return d

def get_dams_per_state(dams, selected_state):
    numDams = 0
    for d in dams:
        if d["Location"]["State"] == selected_state:
            numDams += 1
    return numDams

def get_longest_dam(dams):
    length = 0
    longestDam = ""
    for d in dams:
        if d["Dimensions"]["Crest Length"] > length:
            length = d["Dimensions"]["Crest Length"]
            longestDam = d["Identity"]["Name"]
    return [longestDam, length]

def get_tallest_dam(dams):
    height = 0
    tallestDam = ""
    for d in dams:
        if d["Dimensions"]["Structural Height"] > height:
            height = d["Dimensions"]["Structural Height"]
            tallestDam = d["Identity"]["Name"]
    return [tallestDam, height]

if __name__ =="__main__":
    app.run(debug=False, port=54321)
