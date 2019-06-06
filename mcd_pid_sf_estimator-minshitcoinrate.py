import csv
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

Kp = -0.3
Ki = -0.3
Kd = -0.7
step_size = 1
init_pos = 1
init_funds_rate = 5
shitcoin_bias = 4
min_shitcoin_rate = 3

# input price array
filename = "flat.csv"
title = "Low Error, High D Gain"
day = np.loadtxt(open(filename, "rb"), delimiter=",", skiprows=1, usecols=0)
error = np.loadtxt(open(filename, "rb"), delimiter=",", skiprows=1, usecols=1)


P = error * Kp

# initialize arrays
I = np.empty(P.size)
D = np.empty(P.size)

# start from steady state conditions
init_pos = 0
rolling_sum = init_pos
for j in range(0, error.size):
	rolling_sum += error[j]
	I[j] = rolling_sum
I = I * Ki


prev_val = 0
for j in range (0, error.size):
	D[j] = (error[j] - prev_val) / step_size
	prev_val = error[j]
D = D * Kd

# add to starting fee
# plot the shit out of everything

PID = P + I + D + init_funds_rate
PID_shitcoin = PID * 4
for j in range(0, PID_shitcoin.size):
	if (PID_shitcoin[j] < min_shitcoin_rate):
		PID_shitcoin[j] = min_shitcoin_rate

fig = plt.figure()
st = fig.suptitle(title, fontsize=32)

ax1 = plt.subplot(611)
ax1.set_title("PID Controller for Stability Fee Estimation in MCD with initial Funds Rate = {0}%, Kp = {1}, Ki = {2}, Kd = {3}".format((init_funds_rate), Kp, Ki, Kd))
ax1.title.set_fontsize(18)
ax1.spines['top'].set_position('zero')
ax1.set_ylabel("Price Error (%)")
ax1.yaxis.label.set_fontsize(12)
plt.plot(day, error)
plt.setp(ax1.get_xticklabels(), visible=False)

ax2 = plt.subplot(612, sharex=ax1)
ax2.spines['top'].set_position('zero')
ax2.set_ylabel("P (%)")
ax2.yaxis.label.set_fontsize(12)
plt.plot(day, P)
plt.setp(ax2.get_xticklabels(), visible=False)

ax3 = plt.subplot(613, sharex=ax1)
ax3.spines['top'].set_position('zero')
ax3.set_ylabel("I (%)")
ax3.yaxis.label.set_fontsize(12)
plt.plot(day, I)
plt.setp(ax3.get_xticklabels(), visible=False)

ax4 = plt.subplot(614, sharex=ax1)
ax4.spines['top'].set_position('zero')
ax4.set_ylabel("D (%)")
ax4.yaxis.label.set_fontsize(12)
plt.plot(day, D)
plt.setp(ax4.get_xticklabels(), visible=False)

ax5 = plt.subplot(615, sharex=ax1)
ax5.spines['top'].set_position(('data', init_funds_rate))
ax5.set_title("volatility bias factor = 1")
ax5.title.set_fontsize(8)
ax5.set_ylabel("Funds Rate (%)")
ax5.yaxis.label.set_fontsize(12)
plt.plot(day, PID)
plt.setp(ax5.get_xticklabels(), visible=False)


ax6 = plt.subplot(616, sharex=ax1)
ax6.spines['top'].set_position(('data', init_funds_rate * shitcoin_bias))
ax6.set_title("volatility bias factor = {0}, min sf: {1}%".format(shitcoin_bias, min_shitcoin_rate))
ax6.title.set_fontsize(8)
ax6.set_ylabel("Shitcoin SF (%)")
ax6.yaxis.label.set_fontsize(12)
ax6.set_xlabel("Days")
ax6.xaxis.label.set_fontsize(20)
plt.plot(day, PID_shitcoin)
plt.setp(ax6.get_xticklabels())

# shift subplots down:
st.set_y(0.95)
fig.subplots_adjust(top=0.85)

plt.show()
































