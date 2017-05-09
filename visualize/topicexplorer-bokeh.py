#!/usr/bin/env python
import os, sys, glob, csv 
import matplotlib as mp
import numpy as np
from bokeh.plotting import figure, output_file, output_notebook, show, vplot,gridplot
from bokeh.palettes import brewer
from bokeh.charts import Area, TimeSeries, Line
from bokeh.models import ColumnDataSource, Slider, Callback, CustomJS, TapTool, OpenURL
from bokeh.palettes import brewer 
from bokeh.io import vform 

def load_image_filenames(image_glob='dataset-panama-0302-images/*.jp*g', image_dir='/home/genevieve/mit-whoi/hlda/'): 
    image_dir=os.path.abspath(image_dir)
    image_filenames=[]
    image_filenames=glob.glob(image_dir+'/'+image_glob)
    while len(image_filenames)==0: 
        print('Looking in '+image_dir)
        if image_dir == '' or image_dir =='/':
            print("Could not find "+image_glob)
            return []
            #sys.exit(0)        
        image_dir=os.path.dirname(image_dir)
        image_filenames=glob.glob(image_dir+'/'+image_glob)
    print('Found '+str(len(image_filenames))+' images in '+image_dir)
    image_filenames=list(map(os.path.relpath, image_filenames))
    image_filenames.sort()
    print image_filenames
    return image_filenames[0:1000] # Artifically truncate images 

def load_topic_data(topic_hist_filename='./topics.hist.csv'):
    topics=[]
    timestamps=[]
    topic_order=[]
    vocabsize=0

    data=[]
    numcols=0
    with open(topic_hist_filename, 'r') as csvfile:
        reader = csv.reader(csvfile) 
        for row in reader: 
            numcols = max(numcols, len(row))
            data.append(list(map(float,row)))
    for row in data:
        while len(row) < numcols:
            row.append(0)

    vocabsize=numcols-1

    #data.pop() #remove the last row because for some reason rost is not processing it
    data = data[0:1000] # Artifically truncate data, becuase we only did for the frist 1000 images
    data=np.array(data)
    print "Data shape:", data.shape
    timestamps=data[:,0]
    topics=data[:,1:]
    topic_weights=np.ones(vocabsize)
    for t in topics:
        topic_weights+=t
        t/=np.sum(t)

    #topic_weights=map(np.sum, np.transpose(data[:,1:]))
    W=np.sum(topic_weights)
    topic_weights/=W
    #print 'topic weights:', topic_weights, 'W=',W

    topic_H=np.zeros(len(topics))
    minus_log_weights=-np.log(topic_weights)
    #print 'topic entropy:', minus_log_weights
    for i in range(len(topics)):
        topic_H[i]=np.sum(topics[i] * minus_log_weights)

    #topic_order=np.argsort(map(np.sum, np.transpose(topics)))[::-1]
    topic_order=np.array(range(vocabsize))
    return (topics, topic_H, topic_weights, vocabsize)

def load_ppx_data(ppx_filename='./perplexity.csv'):
    data=[]
    with open(ppx_filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            data.append(list(map(float,row)))
    ppxdata=np.array(data)
    ppxdata=ppxdata[:,1]
    return ppxdata

output_file('index.html')

image_filenames= load_image_filenames('/home/genevieve/mit-whoi/hlda/dataset-panama-0302-images/*.jpg')

(std_topic_dist, std_topic_H, std_topic_weight, std_K) = load_topic_data('/home/genevieve/mit-whoi/data/panama/d20150403_2/topics/default/topics.hist.csv')
(ann_topic_dist, ann_topic_H, ann_topic_weight, ann_K) = load_topic_data('/home/genevieve/mit-whoi/rost-scripts/topics-0302/annotate/topics.hist.csv')
print 'loading hdp'
(hdp_topic_dist, hdp_topic_H, hdp_topic_weight, hdp_K) = load_topic_data('/home/genevieve/mit-whoi/hlda/dataout-panama-0302-images/run010-topics.hist.csv')

hdp_topic_order=np.argsort(hdp_topic_weight)[::-1]
std_topic_order=np.argsort(std_topic_weight)[::-1]
ann_topic_order=np.argsort(ann_topic_weight)[::-1]

hdp_topic_dist_ordered=(hdp_topic_dist.transpose())[hdp_topic_order]
std_topic_dist_ordered=(std_topic_dist.transpose())[std_topic_order]
ann_topic_dist_ordered=(ann_topic_dist.transpose())[ann_topic_order]

hdp_cummulative_topic_dist = np.cumsum(hdp_topic_dist_ordered, axis=0)
std_cummulative_topic_dist = np.cumsum(std_topic_dist_ordered, axis=0)
ann_cummulative_topic_dist = np.cumsum(ann_topic_dist_ordered, axis=0)

# Should all be the same length
timesteps=list(range(len(hdp_topic_dist)))
T=len(timesteps)

print('#timesteps: '+str(T))
print('urls '+str(len(image_filenames)))

source = ColumnDataSource(dict(
    t=[0], 
    cursor_x=[0,0], 
    cursor_y=[-0.05, 1.05],
    x=timesteps, 
    url=[image_filenames[0]], 
    image_urls=image_filenames
))

callback = CustomJS(args=dict(source=source), code="""
    var data = source.get('data');
    var t = time.get('value')
    data['t'][0]=t
    data['url'][0]= data['image_urls'][t]
    data['cursor_x']=[t,t]
    source.trigger('change');
""")

image_w=1360; image_h=1024
plot_w=1200; plot_h=200;

fig_img=figure(x_range=(0,image_w), y_range=(0,image_h), width=int(plot_w/2), height=int(plot_w*image_h/image_w/2+0.5))
fig_img.image_url(url='url', source=source, x=0, y=0, angle=0, w=image_w, h=image_h, anchor='bottom_left')

colormap=brewer["Spectral"][min(20,11)]

ann_fig_topicdist = figure(width=plot_w, height=plot_h, y_range=[-0.1,1.1], title = 'Annotated Terrains')
ann_fig_topicdist.title.text_font_size = '20pt'
ann_fig_topicdist.title.align = 'center'
for i in range(ann_K-1,-1,-1):
    ann_fig_topicdist.patch(x=np.hstack(([timesteps[0]],timesteps, [timesteps[-1]])), y=np.hstack(([0], ann_cummulative_topic_dist[i],[0])), color=colormap[i%min(ann_K,11)])
    print "Doing color:", colormap[i%min(ann_K,11)]
ann_fig_topicdist.line(x='cursor_x', y='cursor_y', source=source, color='black')
ann_fig_topicdist.circle(x='cursor_x', y='cursor_y', source=source, color='black', fill_color='white')
ann_fig_topicdist.yaxis.axis_label = 'Topic Distribution'
ann_fig_topicdist.yaxis.axis_label_text_font_size = '15pt'
ann_fig_topicdist.xaxis.axis_label = 'Time'
ann_fig_topicdist.xaxis.axis_label_text_font_size = '15pt'

hdp_fig_topicdist = figure(width=plot_w, height=plot_h, y_range=[-0.1,1.1], title = 'HLDA Model')
hdp_fig_topicdist.title.text_font_size = '20pt'
hdp_fig_topicdist.title.align = 'center'
for i in range(hdp_K-1,-1,-1):
    hdp_fig_topicdist.patch(x=np.hstack(([timesteps[0]],timesteps, [timesteps[-1]])), y=np.hstack(([0], hdp_cummulative_topic_dist[i],[0])), color=colormap[i%min(hdp_K,11)])
hdp_fig_topicdist.line(x='cursor_x', y='cursor_y', source=source, color='black')
hdp_fig_topicdist.circle(x='cursor_x', y='cursor_y', source=source, color='black', fill_color='white')
hdp_fig_topicdist.yaxis.axis_label = 'Topic Distribution'
hdp_fig_topicdist.yaxis.axis_label_text_font_size = '15pt'
hdp_fig_topicdist.xaxis.axis_label = 'Time'
hdp_fig_topicdist.xaxis.axis_label_text_font_size = '15pt'

std_fig_topicdist = figure(width=plot_w, height=plot_h, y_range=[-0.1,1.1], title = 'Standard HDP Model')
std_fig_topicdist.title.text_font_size = '20pt'
std_fig_topicdist.title.align = 'center'
for i in range(std_K-1,-1,-1):
    std_fig_topicdist.patch(x=np.hstack(([timesteps[0]],timesteps, [timesteps[-1]])), y=np.hstack(([0], std_cummulative_topic_dist[i],[0])), color=colormap[i%min(std_K,11)])
std_fig_topicdist.line(x='cursor_x', y='cursor_y', source=source, color='black')
std_fig_topicdist.circle(x='cursor_x', y='cursor_y', source=source, color='black', fill_color='white')
std_fig_topicdist.yaxis.axis_label = 'Topic Distribution'
std_fig_topicdist.yaxis.axis_label_text_font_size = '15pt'
std_fig_topicdist.xaxis.axis_label = 'Time'
std_fig_topicdist.xaxis.axis_label_text_font_size = '15pt'

time_slider = Slider(start=0, end=len(timesteps)-1, value=0, step=1, title="Time", callback=callback)

callback.args['time']=time_slider

#plots=gridplot([[fig_topicdist], [fig_H],[fig_ppx]])
plots = gridplot([[ann_fig_topicdist], [hdp_fig_topicdist],  [std_fig_topicdist]], border_space=1)
p=vform(fig_img, time_slider, plots)


print ('Writing index.html')
show(p)
