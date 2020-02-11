#this class will hold the service logic for content
from content.models import Lecture
import datetime as dt
from datetime import timedelta
from institute.models import Batches

#d={'lectures': 1, 'duration': 2, 'time': '10:00', 'phase_id': '1', 'subject_id': '1', 'batches': ['1'], 'start_date': '2020-01-01'}
#from content.service import *
#create_lectures(**d)
def create_lectures(*args,**kwargs):
	no_of_lectures = kwargs.get('lectures')
	duration = kwargs.get('duration')
	time = kwargs.get('time')
	phase_id = kwargs.get('phase_id')
	subject_id = kwargs.get('subject_id')
	start_date = kwargs.get('start_date')
	at_time = kwargs.get('time')
	start_date_time = get_date_time(start_date,at_time)
	batches = kwargs.get('batches')
	batches = get_batches(batches,phase_id)

	for batch in batches:
		for lecture_counter in range(no_of_lectures):
			create_lecture(batch,subject_id,start_date_time,duration,phase_id)
			start_date_time = get_next_eligible_date(start_date_time) 


def get_batches(batches,phase_id):
	if 'all' in batches:
		batches = Batches.objects.filter(phase_id=phase_id).values_list('id',flat=True)
	return batches

def get_next_eligible_date(date_time,delta=1):
	'''
	This will provide the next working day skipping sunday
	'''
	if date_time.weekday() == 5:
		delta += 1
	return date_time + timedelta(delta)

def get_date_time(date,time):
	mydate = dt.datetime.strptime(date, "%Y-%m-%d")
	mytime = dt.datetime.strptime(time,'%H:%M').time()
	return dt.datetime.combine(mydate, mytime)

def create_lecture(batch_id,subject_id,start_date_time,duration,phase_id):
	Lecture.objects.create(batch_id=batch_id,subject_id=subject_id,start_date_time=start_date_time,duration_hours=duration,phase_id=phase_id)