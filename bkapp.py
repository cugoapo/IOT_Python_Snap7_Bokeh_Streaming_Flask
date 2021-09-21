import warnings
from math import radians
from threading import Thread
from time import sleep

import snap7
from bokeh.embed import server_document
from bokeh.layouts import layout
from bokeh.models import ColumnDataSource, DatetimeTickFormatter
from bokeh.models import HoverTool
from bokeh.models.widgets import Panel, Tabs
from bokeh.plotting import figure
from bokeh.server.server import Server
from bokeh.themes import Theme
from flask import Flask, render_template
from snap7.types import *
from snap7.util import *
from tornado.ioloop import IOLoop
warnings.filterwarnings("ignore")

app = Flask(__name__,
            template_folder="web/templates")

def xaxis_formatter_(fig, xaxis_label, radians_):
    # date_pattern = ["%Y-%m-%d\n%H:%M:%S"]
    date_pattern = ["%H:%M:%S"]
    fig.xaxis.formatter = DatetimeTickFormatter(
        seconds=date_pattern,
        minsec=date_pattern,
        minutes=date_pattern,
        hourmin=date_pattern,
        hours=date_pattern
        # days=date_pattern,
        # months=date_pattern,
        # years=date_pattern
    )
    fig.xaxis.major_label_orientation = radians(radians_)
    fig.yaxis.axis_label = xaxis_label
    return fig

def create_source(source_name):
    """
    ColumnDataSource(dict(x=[], y=[]))
    param :source_name
    return: Source Object
    """
    source_name = ColumnDataSource(dict(x=[], y=[]))
    return source_name

def create_fig(fig_name, circle_color, line_color, act_line_source, set_line_source):
    tools = "pan,wheel_zoom,reset"
    tooltips = [
        ('Temperature', '$y')
    ]
    fig_name = figure(x_axis_type="datetime", tools=tools)
    fig_name.circle(x="x", y="y", color="firebrick", source=act_line_source)
    fig_name.line(x="x", y="y", source=act_line_source)
    fig_name.line(x="x", y="y", source=set_line_source, line_color="firebrick")
    fig_name.add_tools(HoverTool(tooltips=tooltips))
    return fig_name

def plc_connect(ip, rack, slot, tcpport, stop_tries, freq):
    plc_name = snap7.client.Client()
    tries = 1
    while tries < stop_tries and not plc_name.get_connected():
        try:
            # print('trying for connecting to PLC ...')
            sleep(freq)
            plc_name.connect(ip, rack, slot, tcpport)
            return True, plc_name

        except Exception as e:
            logger.error("warning in PLC connection >>{}".format(e))
            sleep(freq)

            if tries == (stop_tries - 1):
                print('error in plc connection')
                return False

        tries += 1
    return False

def bkapp(doc):

    # workstation_1
    source41 = create_source("source41")        # Sensor Actual Value
    source411 = create_source("source411")      # Sensor Set Value
    source42 = create_source("source42")
    source421 = create_source("source421")
    source44 = create_source("source44")
    source441 = create_source("source441")
    source45 = create_source("source45")
    source451 = create_source("source451")

    # workstation_2
    source51 = create_source("source51")
    source511 = create_source("source511")
    source52 = create_source("source52")
    source521 = create_source("source521")
    source53 = create_source("source53")
    source531 = create_source("source531")
    source54 = create_source("source54")
    source541 = create_source("source541")

    def update():
        # workstation_1
        _, plc = plc_connect("ip address", 0, 2, 102, 3, 2)
        if _ == True:

            source41.stream(dict(x=[datetime.now()],
                                y=[get_real(plc.read_area(areas["DB"], 405, 804, S7WLReal), 0)]), rollover=30)
            source42.stream(dict(x=[datetime.now()],
                                y=[get_real(plc.read_area(areas["DB"], 405, 828, S7WLReal), 0)]), rollover=30)
            source44.stream(dict(x=[datetime.now()],
                                y=[get_real(plc.read_area(areas["DB"], 405, 876, S7WLReal), 0)]), rollover=30)
            source45.stream(dict(x=[datetime.now()],
                                y=[get_real(plc.read_area(areas["DB"], 405, 900, S7WLReal), 0)]), rollover=30)
            source411.stream(dict(x=[datetime.now()],
                                 y=[get_real(plc.read_area(areas["DB"], 405, 10, S7WLReal), 0)]), rollover=30)
            source421.stream(dict(x=[datetime.now()],
                                 y=[get_real(plc.read_area(areas["DB"], 405, 90, S7WLReal), 0)]), rollover=30)
            source441.stream(dict(x=[datetime.now()],
                                 y=[get_real(plc.read_area(areas["DB"], 405, 250, S7WLReal), 0)]), rollover=30)
            source451.stream(dict(x=[datetime.now()],
                                 y=[get_real(plc.read_area(areas["DB"], 405, 330, S7WLReal), 0)]), rollover=30)

        # workstation_2
        _, plc2 = plc_connect("ip address", 0, 2, 102, 3, 2)
        if _ == True:

            source51.stream(dict(x=[datetime.now()],
                                 y=[get_real(plc2.read_area(areas["DB"], 319, 34, S7WLReal), 0)]), rollover=30)
            source511.stream(dict(x=[datetime.now()],
                                 y=[get_word(plc2.read_area(areas["DB"], 319, 30, S7WLWord), 0)]), rollover=30)
            source52.stream(dict(x=[datetime.now()],
                                 y=[get_real(plc2.read_area(areas["DB"], 319, 52, S7WLReal), 0)]), rollover=30)
            source521.stream(dict(x=[datetime.now()],
                                  y=[get_word(plc2.read_area(areas["DB"], 319, 48, S7WLWord), 0)]), rollover=30)
            source53.stream(dict(x=[datetime.now()],
                                 y=[get_real(plc2.read_area(areas["DB"], 319, 70, S7WLReal), 0)]), rollover=30)
            source531.stream(dict(x=[datetime.now()],
                                  y=[get_word(plc2.read_area(areas["DB"], 319, 66, S7WLWord), 0)]), rollover=30)
            source54.stream(dict(x=[datetime.now()],
                                 y=[get_real(plc2.read_area(areas["DB"], 319, 88, S7WLReal), 0)]), rollover=30)
            source541.stream(dict(x=[datetime.now()],
                                  y=[get_word(plc2.read_area(areas["DB"], 319, 84, S7WLWord), 0)]), rollover=30)

    doc.add_periodic_callback(update, 500)

    # workstation_1
    p41 = xaxis_formatter_(create_fig("a", "firebrick", "firebrick", source41, source411), "Temperature Sensor 1", 15)
    p42 = xaxis_formatter_(create_fig("a", "firebrick", "firebrick", source42, source421), "Temperature Sensor 2", 15)
    p44 = xaxis_formatter_(create_fig("a", "firebrick", "firebrick", source44, source441), "Temperature Sensor 4", 15)
    p45 = xaxis_formatter_(create_fig("a", "firebrick", "firebrick", source45, source451), "Temperature Sensor 5", 15)

    # workstation_2
    p51 = xaxis_formatter_(create_fig("a", "firebrick", "firebrick", source51, source511), "Temperature Sensor 1", 15)
    p52 = xaxis_formatter_(create_fig("a", "firebrick", "firebrick", source52, source521), "Temperature Sensor 2", 15)
    p53 = xaxis_formatter_(create_fig("a", "firebrick", "firebrick", source53, source531), "Temperature Sensor 3", 15)
    p54 = xaxis_formatter_(create_fig("a", "firebrick", "firebrick", source54, source541), "Temperature Sensor 4", 15)

    lay_out_1 = layout([[p41, p42], [p44, p45]])
    lay_out_2 = layout([[p51, p52], [p53, p54]])

    first_panel = Panel(child=lay_out_1, title="workstation_1")
    second_panel = Panel(child=lay_out_2, title="workstation_2")

    tabs = Tabs(tabs=[first_panel, second_panel])
    doc.add_root(tabs)
    doc.theme = Theme(filename="theme.yaml")

@app.route('/', methods=['GET'])
def bkapp_page():
    script = server_document('http://localhost:5006/bkapp')
    return render_template("embed.html", script=script, template="Flask")

def bk_worker():
    # Can't pass num_procs > 1 in this configuration. If you need to run multiple
    # processes, see e.g. flask_gunicorn_embed.py
    server = Server({'/bkapp': bkapp}, io_loop=IOLoop(), allow_websocket_origin=["127.0.0.1:8000"])
    server.start()
    server.io_loop.start()

Thread(target=bk_worker).start()

if __name__ == '__main__':
    print('Opening single process Flask app with embedded Bokeh application on http://localhost:8000/')
    print()
    print('Multiple connections may block the Bokeh app in this configuration!')
    print('See "flask_gunicorn_embed.py" for one way to run multi-process')
    app.run(port=8000)