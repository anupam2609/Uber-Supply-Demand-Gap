
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime as dt


uber_dat=pd.read_csv("C:\\Users\\Anupam\\Documents\\Upgrad Documents\\Uber_Assignment\\Uber Request Data.csv")


# Data Cleansing
#check for null values
uber_dat.isnull().sum(axis=0)

#check for NA values
uber_dat.isna().sum(axis=0)

#check for duplicates
uber_dat.duplicated().sum(axis=0)


#changing the format of dates and time uniformly
uber_dat['Request timestamp']=pd.to_datetime(uber_dat['Request timestamp'])
uber_dat['Drop timestamp']=pd.to_datetime(uber_dat['Drop timestamp'])

#extracting dates and time
uber_dat['rdate'] = uber_dat['Request timestamp'].dt.date
uber_dat['ddate'] = uber_dat['Drop timestamp'].dt.date
uber_dat['rtime'] = uber_dat['Request timestamp'].dt.time
uber_dat['dtime']= uber_dat['Drop timestamp'].dt.time
uber_dat['rhour']= uber_dat['Request timestamp'].dt.hour
uber_dat['rmin']= uber_dat['Request timestamp'].dt.minute
uber_dat['dhour']= uber_dat['Drop timestamp'].dt.hour
uber_dat['dmin']= uber_dat['Drop timestamp'].dt.minute


sts_grp=uber_dat.groupby('Status')
uber_dat['travel_time(min)']=(abs(uber_dat['dhour']-uber_dat['rhour'])*60 + abs(uber_dat['dmin']-uber_dat['rmin']))

def timeslot(x):
    if x>=4 and x<=8:
        return ('Early Morning')
    elif x>8 and x<=12:
        return ('Morning')
    elif x>12 and x<=16:
        return ('Noon')
    elif x>16 and x<=20:
        return ('Evening')
    elif x>20 and x<=24:
        return ('Midnight')
    else:
        return ('Late Night')

uber_dat['TimeSlot']=uber_dat['rhour'].apply(timeslot)

uber_dat.head(100)

#Plot0 depicting Airport/City Hour of Day of Completed Trips, cancelled trips and no cars available
plt.figure(num=None, figsize=(12, 8), dpi=80, facecolor='w', edgecolor='k')
plt.ylim([0,24])
plt.title('Status of Trips as per the Request Hour w.r.t Origin')
p0=sns.barplot(x='Status', y='rhour', data=uber_dat, hue='Pickup point')
plt.show()



#Plot1 depicting Airport/City Count for Status Completed Trips, cancelled trips and no cars available wrt to Origin
plt.figure(num=None, figsize=(12, 8), dpi=80, facecolor='w', edgecolor='k')
plt.title('Count of Status w.r.t Origins')
df1=(uber_dat.groupby(['Pickup point'])['Status'].value_counts(normalize=False).rename('Frequency').reset_index().sort_values('Status'))
p1=sns.barplot(x='Status', y='Frequency',hue='Pickup point', data=df1)
plt.show()



#Plot2 depicting Airport/City Count of no. Trips wrt to Time SLots
plt.figure(num=None, figsize=(12, 8), dpi=80, facecolor='w', edgecolor='k')
plt.title('Count of Trips w.r.t Time Slots between Origins')
df1=(uber_dat.groupby(['Pickup point'])['TimeSlot'].value_counts(normalize=False).rename('Count of Trips').reset_index().sort_values('TimeSlot'))
p2=sns.barplot(x='TimeSlot', y='Count of Trips',hue='Pickup point', data=df1)
plt.show()


#Plot3 depicting Count of no. Trips wrt to Time SLots and Status of the Trips
plt.figure(num=None, figsize=(12, 8), dpi=80, facecolor='w', edgecolor='k')
plt.title('Count of Trips w.r.t Time Slots and Status')
df1=(uber_dat.groupby(['Status'])['TimeSlot'].value_counts(normalize=False).rename('Count of Trips').reset_index().sort_values('TimeSlot'))
p3=sns.barplot(x='TimeSlot', y='Count of Trips',hue='Status', data=df1)
plt.show()


#Plot4 depicting the request Frequencies wrt Time slots
plt.figure(num=None, figsize=(12, 8), dpi=80, facecolor='w', edgecolor='k')
plt.title('Request Frequency w.r.t Time Slots and Pickup point')
df1=(uber_dat.groupby(['TimeSlot','Pickup point'])['rhour'].value_counts(normalize=False).rename('Request Frequency').reset_index().sort_values('TimeSlot'))
p4a=sns.barplot(x='TimeSlot', y='Request Frequency',hue='Pickup point', data=df1)
plt.show()


#Extracting the DataFrame for Tableau model design purpose
uber_dat.to_csv('Uber_DAT.csv')


#Plot4 depicting the request Frequencies wrt Time slots
plt.figure(num=None, figsize=(12, 8), dpi=80, facecolor='w', edgecolor='k')
plt.title('Request Frequency w.r.t Time Slots and Pickup point at an Overall Level')
df1=(uber_dat.groupby(['TimeSlot','Pickup point'])['rhour'].value_counts(normalize=False).rename('Request Frequency').reset_index().sort_values('TimeSlot'))
p4b=sns.barplot(x='Pickup point', y='Request Frequency',hue='TimeSlot', data=df1)
plt.show()


#Plot5 depicting the request Frequencies wrt Timeslot and their resepctive status only from Aiport to City
plt.figure(num=None, figsize=(12, 8), dpi=80, facecolor='w', edgecolor='k')
plt.title('Request Frequencies wrt Timeslot and their resepctive status only for Aiport-City')
D1=uber_dat[uber_dat['Pickup point']=='Airport']
Dg1=(D1.groupby(['TimeSlot','Status'])['rhour'].value_counts(normalize=False).rename('Request Frequency').reset_index().sort_values('TimeSlot'))
p6=sns.barplot(x='Status', y='Request Frequency',hue='TimeSlot', data=Dg1)
plt.show()


#Plot5 depicting the request Frequencies wrt Timeslot and their resepctive status only from City-Airport as orgin trips
plt.figure(num=None, figsize=(12, 8), dpi=80, facecolor='w', edgecolor='k')
plt.title('Request Frequencies wrt Timeslot and their resepctive status only for City-Airport')
D2=uber_dat[uber_dat['Pickup point']=='City']
Dg2=(D2.groupby(['TimeSlot','Status'])['rhour'].value_counts(normalize=False).rename('Request Frequency').reset_index().sort_values('TimeSlot'))
p7=sns.barplot(x='Status', y='Request Frequency',hue='TimeSlot', data=Dg2)
plt.show()


