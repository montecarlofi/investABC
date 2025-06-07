# (c) Mikal Rian 2025
# 
import streamlit as st
import numpy as np
import altair as alt
st.set_page_config(layout="wide")

# Data conversion from numpy array to list of dicts.
def np_XY_table_to_chart_data(table, namelist, namelist_label = 'Type', x_offset=1):
	len_Y = table.shape[0]
	len_X = table.shape[1]

	D = []

	for i in range(len_Y):
		for j in range(len_X):
			d = { 
				namelist_label: namelist[i], 
				'x': j + x_offset,
				'y': table[i][j]
			}
			D.append(d)

	return D

# Charting list of dicts.
def chart(data, namelist, category_name, x_range, y_min=0, y_max=100, tickcount=12, colours=None, title=''):
	#domain =  [0.5, 0.6, 0.7, 0.8, 0.9]
	#range_ = ['#9cc8e2', '#9cc8e2', 'red', '#5ba3cf', '#125ca4']
	#category_name="Type:N"
	#import streamlit as st
	#st.write(tickcount)

	# create default range of colours if None

	c = (
		alt.Chart(alt.Data(values=data))
		.mark_line()
		.encode(
		    #x="x:O",
		    x = alt.X("x:O", axis=alt.Axis(tickCount=tickcount)),# scale=alt.Scale(domain=np.arange(0, 120, 12), type="ordinal"), axis=alt.Axis(tickCount=tickcount)), 
		    #x=alt.X("x:O", scale=alt.Scale(domain=list(x_range)), axis=alt.Axis(values=list(x_range))),
		    y = alt.Y('y:Q', scale=alt.Scale(domain=(y_min, y_max))),
		    color = alt.Color(f'{category_name}:N', scale=alt.Scale(domain=namelist, range=colours))  # scheme="dark2" or viridis, magma, dark2, inferno
		).properties(title=title)	
	   	).configure_axis(
	   		grid=False
	   	).configure_view(
	   		stroke=None 	# Borders
	)
	return c

# Convert yearly to monthly rate.
def get_r(yr):
	r = np.e**(np.log((1+yr))/12)
	return r

def geometric_series(n, start_value=0, repeating_amount=0, periodic_rate=1):
	r = periodic_rate
	if n == 0:
		return []
	y = [0 for i in range(n)]
	if start_value == 0:
		start_value = repeating_amount
	y[0] = start_value * periodic_rate #+ repeating_amount * periodic_rate
	if r == 1:  # Makes .../(1-r) zero division.
		for i in range(1, n):
			y[i] = start_value * periodic_rate + repeating_amount * i
	else:
		#for i in range(0, n):
		#	m = i + 2
		#	a = repeating_amount * (1-r**m) / (1-r)
		#	a -= repeating_amount
		#	y[i] = a
		for i in range(1, n):
			#y[i] = (y[i-1] + repeating_amount) * periodic_rate
			y[i] = y[i-1] * periodic_rate + repeating_amount
	return y

# Geometric series: we invest at 00:01 the first day, and read the result at 23:59 the last day.
def geo_series(start, periodic_amount, periodic_rate, n):
	r = periodic_rate
	if n == 0:
		return []
	y = [0 for i in range(n)]

	#if start == 0:
	#	start = periodic_amount
	y[0] = (start + periodic_amount) * periodic_rate

	for i in range(1, n):
		P = y[i-1] + periodic_amount
		y[i] = P * periodic_rate

	return y

def geo(r, n):
	return (1-r**n)/(1-r)


# SCRIPT
N = 480 * 2

A, B, C, G = st.columns([2, 2, 2, 9])

with A:
	st.write('A')
	capital_A = st.number_input('Starting capital', min_value=0, value=1000, key='capital_A')
	switch = True if capital_A == 0 else False
	reinvest_A = st.number_input('Reinvest, monthly', value=0., key='reinvest_A', disabled=switch)
	rate_A = get_r(st.slider('Growth in \\%', min_value=-5, max_value=10, value=4, step=1, key='rate_A', disabled=switch)/100)
	invest_A2 = st.number_input('A2 invest, monthly', min_value=0., value=0., key='invest_A2', disabled=switch)
	switch_ = True if (switch == True or invest_A2 == 0) else False
	rate_A2 = get_r(st.slider('A2 growth in \\%', min_value=-5, max_value=10, value=0, step=1, key='rate_A2', disabled=switch_)/100)
	invest_A3 = st.number_input('A3 invest, monthly', min_value=0., value=0., key='invest_A3', disabled=switch)
	switch_ = True if (switch == True or invest_A3 == 0) else False
	rate_A3 = get_r(st.slider('A3 growth in \\%', min_value=-5, max_value=10, value=0, step=1, key='rate_A3', disabled=switch_)/100)

with B:
	st.write('B')
	capital_B = st.number_input('Starting capital', min_value=0, value=1000, key='capital_B')
	switch = True if capital_B == 0 else False
	reinvest_B = st.number_input('Reinvest, monthly', value=0., key='reinvest_B')
	rate_B = get_r(st.slider('Growth in \\%', min_value=-5, max_value=10, value=4, step=1, key='rate_B', disabled=switch)/100)
	invest_B2 = st.number_input('B2 invest, monthly', min_value=0., value=0., key='invest_B2', disabled=switch)
	switch_ = True if (switch == True or invest_B2 == 0) else False
	rate_B2 = get_r(st.slider('B2 growth in \\%', min_value=-5, max_value=10, value=0, step=1, key='rate_B2', disabled=switch_)/100)
	invest_B3 = st.number_input('B3 invest, monthly', min_value=0., value=0., key='invest_B3', disabled=switch)
	switch_ = True if (switch == True or invest_B3 == 0) else False
	rate_B3 = get_r(st.slider('B3 growth in \\%', min_value=-5, max_value=10, value=0, step=1, key='rate_B3', disabled=switch_)/100)
	is_checked = st.checkbox("Combine with C")

with C:
	st.write('C')
	capital_C = st.number_input('Starting capital', min_value=0, value=0, key='capital_C')
	switch = True if capital_C == 0 else False
	reinvest_C = st.number_input('Reinvest, monthly', value=0., key='reinvest_C', disabled=switch)
	rate_C = get_r(st.slider('Growth in \\%', min_value=-5, max_value=10, value=4, step=1, key='rate_C', disabled=switch)/100)
	invest_C2 = st.number_input('C2 invest, monthly', min_value=0., value=0., key='invest_C2', disabled=switch)
	switch_ = True if (switch == True or invest_C2 == 0) else False
	rate_C2 = get_r(st.slider('C2 growth in \\%', min_value=-5, max_value=10, value=0, step=1, key='rate_C2', disabled=switch_)/100)
	invest_C3 = st.number_input('C3 invest, monthly', min_value=0., value=0., key='invest_C3', disabled=switch)
	switch_ = True if (switch == True or invest_C3 == 0) else False
	rate_C3 = get_r(st.slider('C3 growth in \\%', min_value=-5, max_value=10, value=0, step=1, key='rate_C3', disabled=switch_)/100)

with C:
	display_N = st.selectbox('Display months', [i for i in range(120, N+1, 120)], index=1)  # + 12
	display_N = display_N if display_N <= N else N


CA1 = geo_series(start=capital_A, periodic_amount=reinvest_A, periodic_rate=rate_A, n=N)
CA2 = geo_series(start=0, periodic_amount=invest_A2, periodic_rate=rate_A2, n=N)
CA3 = geo_series(start=0, periodic_amount=invest_A3, periodic_rate=rate_A3, n=N)

CB1 = geo_series(start=capital_B, periodic_amount=reinvest_B, periodic_rate=rate_B, n=N)
CB2 = geo_series(start=0, periodic_amount=invest_B2, periodic_rate=rate_B2, n=N)
CB3 = geo_series(start=0, periodic_amount=invest_B3, periodic_rate=rate_B3, n=N)

CC1 = geo_series(start=capital_C, periodic_amount=reinvest_C, periodic_rate=rate_C, n=N)
CC2 = geo_series(start=0, periodic_amount=invest_C2, periodic_rate=rate_C2, n=N)
CC3 = geo_series(start=0, periodic_amount=invest_C3, periodic_rate=rate_C3, n=N)

CA = [a + b + c for a, b, c in zip(CA1, CA2, CA3)]
CB = [a + b + c for a, b, c in zip(CB1, CB2, CB3)]
CC = [a + b + c for a, b, c in zip(CC1, CC2, CC3)]


if is_checked == True:
	CB = [a + b for a, b in zip(CB, CC)]
	capital_C = 0


if capital_A == 0:
	CA = [0 for i in range(N)]
if capital_B == 0:
	CB = [0 for i in range(N)]
if capital_C == 0:
	CC = [0 for i in range(N)]


with G:
	table = np.array([CA[:display_N], CB[:display_N], CC[:display_N]])
	y_max = np.max(table)
	y_min = np.min(table)
	#a_end, b_end, c_end = int(np.max(table[0,:])) if capital_A != 0 else '', int(np.max(table[1,:])) if capital_B != 0 else '', int(np.max(table[2,:])) if capital_C != 0 else ''
	a_end, b_end, c_end = int(table[0,-1]) if capital_A != 0 else '', int(table[1,-1]) if capital_B != 0 else '', int(table[2,-1]) if capital_C != 0 else ''

	if capital_A == 0:
		CA = [None for i in range(N)]
	if capital_B == 0:
		CB = [None for i in range(N)]
	if capital_C == 0:
		CC = [None for i in range(N)]
	table = np.array([CA[:display_N], CB[:display_N], CC[:display_N]])

	namelist = ['A', 'B', 'C']
	category_name = 'Investment type'
	colours = ['blue', 'red', 'lightgreen', '#125ca4'] # ['#9cc8e2', '#9cc8e2', 'red', '#5ba3cf', '#125ca4']
	chart_data = np_XY_table_to_chart_data(table, namelist, namelist_label=category_name, x_offset=1)
	y_min = y_min if y_min < 0 else y_min*.9
	x_range = range(table.shape[1])
	c = chart(chart_data, namelist, category_name, x_range, y_min=y_min, y_max=y_max*1.1, tickcount=3, colours=colours, title='')



#	data = pd.DataFrame({
#	    'x': range(0, display_N),
#	    'a: Real (+extra pay, invest) *': capital_R,
#	    'c: Real (+invest) **': capital_I,
#	})
#	data.set_index('x', inplace=True)
	st.subheader("&nbsp; &nbsp; &nbsp; Invest in A, B, or C?")
	# Display graphs
	st.altair_chart(c, use_container_width=True) # theme="streamlit" throws error

	space = '&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; '
	st.write(space, 'A:', a_end)
	st.write(space, 'B:', b_end)
	st.write(space, 'C:', c_end)
