from flask import Flask, render_template_string, jsonify
import threading
import json

app = Flask(__name__)

dashboard_state = {
    "world": {},
    "config": {},
    "sensors": {},
    "controllers": {},
}

HTML = """
<!DOCTYPE html>
<html>

<head>

<title>Smart Truck Dashboard</title>

<style>

* {
    box-sizing: border-box;
}

body {
    margin: 0;
    padding: 20px;
    font-family: Arial, sans-serif;
    background: #111;
    color: #eee;
}

h1 {
    margin-bottom: 20px;
}

h2 {
    color: #6cf;
    margin-top: 0;
}

h3 {
    color: #9cf;
    margin-top: 0;
}

.top {
    display: flex;
    justify-content: space-between;
    gap: 2%;
    width: 100%;
}

.top .box {
    width: 32%;
}

.grid {
    margin-top: 20px;

    display: grid;
    grid-template-columns: 45% 45%;
    justify-content: space-between;
    row-gap: 20px;
}

.box {
    background: #181818;
    border: 1px solid #555;
    border-radius: 10px;
    padding: 15px;

    overflow: hidden;
}

.entry {
    display: flex;
    justify-content: space-between;

    border-bottom: 1px solid #333;

    padding: 5px 0;
}

.key {
    color: #aaa;
}

.value {

    text-align: right;

    max-width: 60%;

    overflow-wrap: anywhere;

    white-space: pre-wrap;
}

pre {
    white-space: pre-wrap;
    overflow-wrap: anywhere;
    margin: 5px 0;
}

.history {
    max-height: 220px;
    overflow-y: auto;
}

</style>

</head>

<body>

<h1>Smart Truck Dashboard</h1>

<div class="top">

    <div class="box">
        <h2>World State</h2>
        <div id="world"></div>
    </div>

    <div class="box">
        <h2>Real Sensor Values</h2>
        <div id="sensors"></div>
    </div>

    <div class="box">
        <h2>Configuration</h2>
        <div id="config"></div>
    </div>

</div>


<h2>Controllers</h2>

<div id="controllers" class="grid"></div>


<script>

function renderEntries(target, data)
{
    let html = "";

    for (const [key,value] of Object.entries(data))
    {
        let display = value;

        if (typeof value === "object" && value !== null)
        {
            display = JSON.stringify(value, null, 2);
        }

        html += `
        <div class="entry">

            <div class="key">${key}</div>

            <div class="value">${display}</div>

        </div>
        `;
    }

    document.getElementById(target).innerHTML = html;
}


function updateDashboard()
{
    fetch("/api/state")

    .then(r => r.json())

    .then(data => {

        renderEntries(
            "world",
            data.world
        );

        renderEntries(
            "config",
            data.config
        );

        renderEntries(
            "sensors",
            data.sensors
        );


        let html = "";

        for (const [name,controller] of Object.entries(data.controllers))
        {
            html += `
            <div class="box">

                <h3>${name}</h3>

                <b>Current Plan</b>

                <pre>${controller.plan}</pre>

                <b>History</b>

                <pre class="history">${controller.history.slice().reverse().join("\\n")}</pre>

            </div>
            `;
        }

        document.getElementById("controllers").innerHTML = html;

    });
}

setInterval(updateDashboard, 500);

updateDashboard();

</script>

</body>

</html>
"""


@app.route("/")
def index():
    return render_template_string(HTML)


@app.route("/api/state")
def api_state():
    return jsonify(dashboard_state)


def start():

    threading.Thread(
        target=lambda: app.run(
            host="0.0.0.0",
            port=8090,
            debug=False,
            use_reloader=False,
        ),
        daemon=True,
    ).start()


def update(
    world=None,
    config=None,
    sensors=None,
    controllers=None,
):
    if world is not None:
        dashboard_state["world"] = world

    if config is not None:
        dashboard_state["config"] = config

    if sensors is not None:
        dashboard_state["sensors"] = sensors

    if controllers is not None:
        dashboard_state["controllers"] = controllers
