import csv
import datetime
import glob
import matplotlib
matplotlib.use('Agg')    # has to be called before pyplot is imported
import matplotlib.pyplot as plt
from matplotlib.dates import HourLocator, DateFormatter, DayLocator, YearLocator
import os
# import pylab
from time import sleep

CSV_DIR       = "/home/pi/csvdata"
DATE_FORMAT   = "%X %x"         # ex "07:06:05 09/30/13"
DAY_FORMAT    = "%Y-%m-%d"      # ex "2013-09-30"
INITIAL_DELAY = 10
REDRAW_DELAY  = 10
print "hello"
DEBUG = True
if DEBUG:
    def debug_print(s):
        print(s)
else:
    def debug_print(s):
        pass

def wait(i):
    debug_print("Waiting for {} seconds".format(i))
    sleep(i)

def get_newest_file(dir, ext=None):
    debug_print("Finding newest file")
    if ext is None:
        # no ext given - match all file extensions
        filespec = "*"
    elif ext[:1] == ".":
        # ext starts with period - don't repeat it
        filespec = "*" + ext
    else:
        # no period - insert one
        filespec = "*." + ext

    # make full search path
    path = os.path.join(dir, filespec)
    # get all matching files
    file_names = glob.glob(path)

    if not file_names:
        # no matching files found
        debug_print("  nothing found")
        return None
    else:
        # find newest file
        newest = max(file_names, key = os.path.getmtime)
        debug_print("  found {}".format(newest))
        return newest

def get_humidity_data(csv_fname):
    hum = []
    dat = []
    parsetime = datetime.datetime.strptime
    debug_print("Reading data")
    good, skip = 0, 0
    with open(csv_fname, "r") as csv_file:
        for row in csv.reader(csv_file):
            try:
                h = int(row[1])
                d = parsetime(row[0], DATE_FORMAT)
                if 1 <= h <= 1000:
                    hum.append(h)
                    dat.append(d)
                    good += 1
                else:
                    skip += 1
            except ValueError:
                skip += 1
    debug_print("  found {} good rows, skipped {} bad rows".format(good, skip))
    return hum, dat

def make_graph(humidities, dates_):
    firstdate = dates_[0]
    lastdate = dates_[-1]
    graph_title = "{} - {}".format(firstdate.strftime(DAY_FORMAT), lastdate.strftime(DAY_FORMAT))
    debug_print("Making graph for {}".format(graph_title))

    # create new plot
    fig, ax = plt.subplots()
    fig.set_size_inches(40.5, 20.5)
    fig.subplots_adjust(bottom = 0.2)
    # configure axes
    ax.xaxis_date()
    ax.xaxis.set_major_locator(DayLocator())
    ax.xaxis.set_minor_locator(HourLocator())
    ax.xaxis.set_major_formatter(DateFormatter(DATE_FORMAT))
    ax.yaxis.set_major_locator(plt.FixedLocator([10, 20, 30, 110, 120, 130, 140, 150, 160 , 300, 350, 365, 380, 400, 430, 480]))
    ax.set_xlim(firstdate, lastdate)
    ax.set_ylim(10,500)
    ax.autoscale_view()
    plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')
    plt.xticks(rotation=15)
    # add data
    plt.plot(dates_, humidities, ".")
    plt.grid()
    plt.title(graph_title)
    return fig

def plot_humidity():
    newest = get_newest_file(CSV_DIR, "csv")
    if newest is None:
        debug_print("No data file found!")
    else:
        h, d = get_humidity_data(newest)
        fig = make_graph(h, d)
        fig.savefig(newest + '_2.png', dpi=100)
        fig.savefig("plot.png", dpi=100)
        # pyplot.savefig("test.pdf")
        debug_print("Done")
        exit()

def main():
    wait(INITIAL_DELAY)
    while True:
        plot_humidity()
        wait(REDRAW_DELAY)

if __name__=="__main__":
    main()
