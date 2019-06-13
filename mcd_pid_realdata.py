import csv
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

Kp = -0.3
Ki = -0.3
Kd = -0.3
step_size = 1
init_pos = 1
init_funds_rate = 17.5
shitcoin_bias = 4

# input price array
filename = "20190513-20190612_DAIUSD_daily_error.csv"
title = "PID estimate for 20190513-20190612"
day = np.loadtxt(open(filename, "rb"), delimiter=",", skiprows=1, usecols=0)
day0 = np.arange(0, day.size)
mean_error = np.loadtxt(open(filename, "rb"), delimiter=",", skiprows=1, usecols=1)
mean_error = mean_error * 100
std_error = np.loadtxt(open(filename, "rb"), delimiter=",", skiprows=1, usecols=2)
std_error = std_error * 100

P_mean = mean_error * Kp
P_error = abs(Kp * std_error)

I_mean = np.empty(P_mean.size)
D_mean = np.empty(P_mean.size)

# start from steady state conditions
init_pos = 0
rolling_sum_mean = init_pos
for j in range(0, mean_error.size):
	rolling_sum_mean += mean_error[j]
	I_mean[j] = rolling_sum_mean
I_mean = I_mean * Ki
I_error = abs(Ki * std_error)

prev_val_mean = 0
for j in range (0, mean_error.size):
	D_mean[j] = (mean_error[j] - prev_val_mean) / step_size
	prev_val_mean = mean_error[j]
D_mean = D_mean * Kd
D_error = abs(Kd * std_error)



PID_mean = P_mean + I_mean + D_mean + init_funds_rate
PID_error = P_error + I_error + D_error

fig = plt.figure()
st = fig.suptitle(title, fontsize=32)

ax1 = plt.subplot(511)
ax1.set_title("PID Controller for Stability Fee Estimation in MCD with initial Funds Rate = {0}%, Kp = {1}, Ki = {2}, Kd = {3}".format((init_funds_rate), Kp, Ki, Kd))
ax1.title.set_fontsize(18)
ax1.spines['top'].set_position('zero')
ax1.set_ylabel("Price Error (%)")
ax1.yaxis.label.set_fontsize(12)
ax1.errorbar(day0, mean_error, yerr=std_error, fmt='o')
plt.plot(mean_error)
plt.setp(ax1.get_xticklabels(), visible=False)

ax2 = plt.subplot(512, sharex=ax1)
ax2.spines['top'].set_position('zero')
ax2.set_ylabel("P (%)")
ax2.yaxis.label.set_fontsize(12)
ax2.errorbar(day0, P_mean, yerr=P_error, fmt='o')
plt.plot(P_mean)
plt.setp(ax2.get_xticklabels(), visible=False)

ax3 = plt.subplot(513, sharex=ax1)
ax3.spines['top'].set_position('zero')
ax3.set_ylabel("I (%)")
ax3.yaxis.label.set_fontsize(12)
ax3.errorbar(day0, I_mean, yerr=I_error, fmt='o')
plt.plot(I_mean)
plt.setp(ax3.get_xticklabels(), visible=False)

ax4 = plt.subplot(514, sharex=ax1)
ax4.spines['top'].set_position('zero')
ax4.set_ylabel("D (%)")
ax4.yaxis.label.set_fontsize(12)
ax4.errorbar(day0, D_mean, yerr=D_error, fmt='o')
plt.plot(D_mean)
plt.setp(ax4.get_xticklabels(), visible=False)

ax5 = plt.subplot(515, sharex=ax1)
ax5.spines['top'].set_position(('data', init_funds_rate))
ax5.title.set_fontsize(8)
ax5.set_ylabel("Funds Rate (%)")
ax5.yaxis.label.set_fontsize(12)
ax5.errorbar(day0, PID_mean, yerr=PID_error, fmt='o')
plt.plot(PID_mean)
plt.setp(ax5.get_xticklabels(), visible=False)

# shift subplots down:
st.set_y(0.95)
fig.subplots_adjust(top=0.85)

plt.show()
































