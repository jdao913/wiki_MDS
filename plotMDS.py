import csv
import argparse
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter

def makePlot(x, y):
    global fig, ax, sc, annot

    fig, ax = plt.subplots()
    ax.xaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    ax.xaxis.set_major_locator(plt.MaxNLocator(20))
    ax.yaxis.set_major_locator(plt.MaxNLocator(20))
    sc = plt.scatter(x,y)

    annot = ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
                        bbox=dict(boxstyle="round", fc="w"),
                        arrowprops=dict(arrowstyle="->"))
    annot.set_visible(False)

    fig.canvas.mpl_connect("motion_notify_event", hover)
    plt.show()

def update_annot(ind):
    global artNames, sc, annot
    pos = sc.get_offsets()[ind["ind"][0]]
    annot.xy = pos
    text = "{}".format(" ".join([artNames[n] for n in ind["ind"]]))
    if len(text) > 20:
        words = text.split()
        count = 0
        text = ""
        didSplit = False
        while count < len(words):
            didSplit = True
            part = ""
            while len(part) < 15:
                if count >= len(words):
                    break
                part += words[count] + " "
                count += 1
            text += part + "\n"
        if didSplit:
            text = text[0:-1]       #Chop off last "\n"
    annot.set_text(text)      
    annot.get_bbox_patch().set_alpha(0.4)

def hover(event):
    global fid, ax, annot, sc
    vis = annot.get_visible()
    if event.inaxes == ax:
        cont, ind = sc.contains(event)
        if cont:
            update_annot(ind)
            annot.set_visible(True)
            fig.canvas.draw_idle()
        else:
            if vis:
                annot.set_visible(False)
                fig.canvas.draw_idle()

if __name__ == "__main__":
    global artNames
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', type=str, help='Input file')
    parser.add_argument('-o', '--output_file', type=str, default='out.png')
    args = parser.parse_args()
    filename = args.input_file
    outname = args.output_file

    file = open(filename, newline='')
    reader = csv.reader(file)
    artNames = next(reader)
    x = next(reader)
    y = next(reader)
    makePlot(x, y)