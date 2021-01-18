from pandas_datareader import data
import datetime
from bokeh.plotting import figure, show, output_file
from bokeh.embed import components
from bokeh.resources import CDN

#Enter start and end times to be viewed
start=datetime.datetime(2020,1,1)
end=datetime.datetime(2021,1,1)

#Enter stock ticker under "Name"
df=data.DataReader(name="^GSPC", data_source="yahoo", start=start, end=end)

#Create a Status column in df with a function that checks if Close is higher than Open
def inc_dec(c,o):
    if c > o:
        value="Increase"
    elif o > c:
        value="Decrease"
    else:
        value="Equal"
    return value
    
df["Status"]=[inc_dec(c,o) for c,o in zip(df["Close"],df["Open"])]
df["Middle"]=(df.Open+df.Close)/2
df["Height"]=abs(df.Open-df.Close)

p=figure(x_axis_type="datetime", width=1000, height=300, sizing_mode="scale_width")
p.title.text="Candlestick Chart"
p.grid.grid_line_alpha=0.3

#Passing the following values: )x-value highest point, )y-value highest point, )x-value lowest point, )y-value lowest point
p.segment(df.index, df.High, df.index, df.Low, color="black")
#Calculating the number of milliseconds in 12 hours to set the rectangle width
rectWidth=12*60*60*1000
#Passing the following values: )the x coordinate as df index, )the central point of the rectangle for the y coordinate, )width of the rect in 12hours in milliseconds, )height of rectangle in difference between Open and Close values
p.rect(df.index[df.Status == "Increase"],df.Middle[df.Status == "Increase"],
       rectWidth,df.Height[df.Status=="Increase"],fill_color="#CCFFFF", line_color="black")
p.rect(df.index[df.Status == "Decrease"],df.Middle[df.Status == "Decrease"],
       rectWidth,df.Height[df.Status == "Decrease"],fill_color="#FF3333", line_color="black")

output_file("CS.html")
show(p)