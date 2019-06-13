import csv
import numpy as np
from datetime import datetime
from datetime import timezone

#  for filtering errant dex trades
MIN_PRICE = 70
MAX_PRICE = 500
MAX_DAIUSD_ERROR = 0.15

dex_filename = "ethdai-trades-May-June2019.csv"
# need to sort these oldest trades first
ethusd_filename = "gemini_ETHUSD_2019_1min.csv"
output_filename = "20190513-20190612_DAIUSD_daily_error.csv"
clean_filename = "cleaned_trades.csv"

def filter_bad(fn):
	with open(fn, 'r') as inp, open(clean_filename, 'w') as out:
		writer = csv.writer(out)
		for row in csv.reader(inp):
			if ((float(row[4]) < MAX_PRICE) and (float(row[4]) > MIN_PRICE)):
				writer.writerow(row)

	inp.close()
	out.close()


# filter input prices
filter_bad(dex_filename)

# input
dex_timestamp = np.loadtxt(open(clean_filename, "rb"), delimiter=",", skiprows=0, usecols=0)
dex_timestamp = dex_timestamp.astype(int)
price_dex_trade_occured = np.loadtxt(open(clean_filename, "rb"), delimiter=",", skiprows=0, usecols=4)
ethusd_timestamp = np.loadtxt(open(ethusd_filename, "rb"), delimiter=",", skiprows=1, usecols=0)
# reduce ethusd timestamp to match dex trade timestamps
ethusd_timestamp = ethusd_timestamp / 1000
ethusd_timestamp = ethusd_timestamp.astype(int)

ethusd_high = np.loadtxt(open(ethusd_filename, "rb"), delimiter=",", skiprows=1, usecols=4)
ethusd_low = np.loadtxt(open(ethusd_filename, "rb"), delimiter=",", skiprows=1, usecols=5)
# use the midpoint of the high and low for that minute on gemini
ethusd_mid = (ethusd_high + ethusd_low) / 2

# Since I don't have ethusd data for every second, I must assume the ethusd price leads the
# daiusd dex price. This is often the case because it takes a few blocks to confirm transactions 
# after they are submitted. However, there is still information lost because the quality of the 
# ethusd data. If I had ethusd pricing data down to the second, I would use it. For now,
# I'm just going to round the dex prices down to the nearest minute. This will cause added
# error to the daiusd error signal.
# init arrays
adjusted_dex_timestamp = np.empty(dex_timestamp.size)
timestamp_day = np.empty(dex_timestamp.size)
timestamp_month = np.empty(dex_timestamp.size)
ethusd_at_blocktime = np.empty(dex_timestamp.size)
# daiusd_error = np.empty(dex_timestamp.size)
# round down blocktimes trades occured to nearest minute
for i in range(0, dex_timestamp.size):
	dayt = datetime.fromtimestamp(dex_timestamp[i])
	ts = datetime(year=dayt.year, month=dayt.month, day=dayt.day, hour=dayt.hour, minute=dayt.minute)
	ts.replace(tzinfo=timezone.utc)
	timestamp_day[i] = ts.day
	timestamp_month[i] = ts.month
	adjusted_dex_timestamp[i] = ts.timestamp()
adjusted_dex_timestamp = adjusted_dex_timestamp.astype(int)
timestamp_day = timestamp_day.astype(int)
timestamp_month = timestamp_month.astype(int)


for i in range(0, adjusted_dex_timestamp.size):
	indx = np.where(ethusd_timestamp == adjusted_dex_timestamp[i])
	if(indx[0].size != 0):
		ethusd_at_blocktime[i] = ethusd_mid[indx[0][0]]


# if error signal is negative, then DAI is weak
# if error signal is positive, then DAI is strong
daiusd_error = (ethusd_at_blocktime / price_dex_trade_occured) - 1
daiusd_error_abs = np.absolute(daiusd_error)
indxmax = np.where(daiusd_error_abs > MAX_DAIUSD_ERROR)
if (indxmax[0].size != 0):
	daiusd_error = np.delete(daiusd_error, indxmax[0])
	timestamp_day = np.delete(timestamp_day, indxmax[0])

list_of_days = []
list_of_error = []
daily_mean_error = []
daily_std = []
prev_day = timestamp_day[0]
for i in range(0, daiusd_error.size):
	# calculate stuff once per day
	if (timestamp_day[i] != prev_day):
		derror = np.array(list_of_error)
		dmean = np.mean(derror)
		dstd = np.std(derror)
		daily_mean_error.append(dmean)
		daily_std.append(dstd)
		list_of_days.append(prev_day)
		prev_day = timestamp_day[i]
		list_of_error = []

	list_of_error.append(daiusd_error[i])
# do the final day
derror = np.array(list_of_error)
dmean = np.mean(derror)
dstd = np.std(derror)
daily_mean_error.append(dmean)
daily_std.append(dstd)
list_of_days.append(timestamp_day[timestamp_day.size - 1])

with open(output_filename, 'w+') as csvF:
	writer = csv.writer(csvF)
	head = ['day', 'mean', 'std']
	writer.writerow(head)
	# write row of 0s for steady state start
	writer.writerow([timestamp_day[0] - 1,0,0])
	for i in range(0, len(list_of_days)):
		row = [int(list_of_days[i]), round(daily_mean_error[i], 8), round(daily_std[i], 8)]
		writer.writerow(row)
csvF.close()
































