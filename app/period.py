from datetime import datetime
from datetime import timedelta

dict1 = [
		'07:14',
		'08:00',
		'08:50',
		'09:42',
		'10:32',
		'11:22',
		'12:12',
		'13:02',
		'13:52',
		'14:44',
		'15:34',
		'16:24'
	]
dict2 = [
		'07:56',
		'08:47',
		'09:39',
		'10:29',
		'11:19',
		'12:09',
		'12:59',
		'13:49',
		'14:41',
		'15:31',
		'16:21',
		'17:11'
	]

periodStart=[]
periodEnd=[]
timeBtwEnd=[]
timeBtwStart=[]
for t in range(0,len(dict1)):
   periodStart.append(datetime.strptime(dict1[t],'%H:%M'))
   periodEnd.append(datetime.strptime(dict2[t],'%H:%M'))
for t in range(0,len(dict1)):
	timeBtwEnd.append(datetime.strptime(dict1[t],'%H:%M')+timedelta(minutes=3))
	timeBtwStart.append(datetime.strptime(dict1[t],'%H:%M')-timedelta(minutes=6))

def convertTS(timestamp):
	time = timestamp.strftime('%H:%M')
	rt = datetime.strptime(time,'%H:%M')
	for x in range(0,len(periodStart)):
    	if(periodStart[x]<=rt and rt<=periodEnd[x]):
    		return x+1

def entryStatus(timestamp):
	time = timestamp.strftime('%H:%M')

	for x in range(0,len(periodStart)):
		if(rt>=timeBtwEnd[x] and rt<=periodEnd[x]):
			return "Late"
		if(rt<=timeBtwEnd[x] and rt>=timeBtwStart[x]):
			return "Present"
