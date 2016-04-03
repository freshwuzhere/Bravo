# coding: utf-8
import io
import ui



import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates

from datetime import datetime
from collections import deque

def plot_strip(dqx , dqy , var_name):

	def plot_to_scrollable_image_view(plt):
		b = io.BytesIO()
		plt.savefig(b)
		img = ui.Image.from_data(b.getvalue())
		cview = ui.ImageView(background_color='white')
		cview.image =img
		return cview


#	plt.plot([math.sin(x/10.0) for x in xrange(95)])
#	plt.xlim(0, 94.2)
	xval = np.array(list(dqx))
#	print(str(xval))

	yval = np.array(list(dqy))
#	print(str(yval))
	
	if len(xval) == len(yval):
		fig,ax = plt.subplots(1,1)
		ax.plot(xval,yval)
		ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
	#	plt.gcf().autofmt_xdate()
		fig.autofmt_xdate()
		ax.grid(True)
		plt.title(var_name)
		plt.ylabel(var_name)
		plt.xlabel('Time')
	
		iview = plot_to_scrollable_image_view(fig)
		iview.frame = (250,250,700,700)
		#view.add_subview(iview)
		iview.present(style='sheet')
	
	