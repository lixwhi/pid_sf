# pid_sf
Estimates the Stability Fee using a PID controller

requires numpy ,Tkinter, and matplotlib

first run get_daily_usd_error.py to build the csv

then run mcd_pid_realdata.py to tune the gains and plot

sources of error:
-I was only able to get the ETHUSD price by the minute from Gemini. It would be better to get it from a basket of exchanges with a higher sample rate than once per minute. 15 seconds would be ideal. To work around this I've rounded down each DAI dex trade to the nearest minute, and calculated the error from there. 

-the first day is zero-ed out so the system can start from a steady state position. This could be changed but I didn't want to mess with it
