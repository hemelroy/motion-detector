from motiondetector import times_df
from bokeh.plotting import figure, show, output_file
from bokeh.models import HoverTool, ColumnDataSource

#Format datetime in dataframe
times_df["Start_str"] = times_df["Start"].dt.strftime("%Y-%m-%d %H-%M-%S")
times_df["End_str"] = times_df["End"].dt.strftime("%Y-%m-%d %H-%M-%S")

col_dt_src = ColumnDataSource(times_df)

#plot graph
plot = figure(x_axis_type = 'datetime', height = 100, width = 500, sizing_mode= "scale_both", title = "Object Detection History")
plot.yaxis.minor_tick_line_color = None
plot.ygrid[0].ticker.desired_num_ticks = 1
plot.title.text_font_size = "30pt"

hover = HoverTool(tooltips = [("Object Entrance Time", "@Start_str"), ("Object Exit Time", "@End_str")])
plot.add_tools(hover)

q = plot.quad(left = "Start", right = "End", bottom = 0, top = 1, color = "blue", source = col_dt_src)

output_file("MotionGraph.html")
show(plot)
