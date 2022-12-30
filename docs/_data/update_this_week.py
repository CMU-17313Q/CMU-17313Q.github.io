from datetime import datetime, date, timedelta
import yaml

class LineBreakDumper(yaml.SafeDumper):
    # Reference: https://github.com/yaml/pyyaml/issues/127
    def write_line_break(self, data=None):
        super().write_line_break(data)

        if len(self.indents) == 1:
            super().write_line_break()
    
    def ignore_aliases(self, data):
        return True

with open('schedule.yaml', 'r') as file:
    schedule = yaml.safe_load(file)

now = datetime(2022, 9, 4, 0, 0, 0, 0) # datetime.now()

last_homework = None
next_homework = None
recitation = None
lectures = []

if schedule: 
    found_week_start = False
    for schedule_day in schedule:
        date = datetime.strptime(schedule_day['date'], "%a %b %d").replace(year=now.year)
        if not found_week_start and date > now:
            # We're at the current week!
            found_week_start = True
        elif found_week_start and date > now + timedelta(weeks=1):
            # We left the current week
            break
        
        if found_week_start:
            if schedule_day['homework']['name'] != '':
                next_homework = schedule_day['homework']
                next_homework['date'] = schedule_day['date']
            
            if schedule_day['lecture']['name'] != '':
                lectures.append(schedule_day['lecture'])
                lectures[-1]['date'] = schedule_day['date']

                if schedule_day['reading']['name'] != '':
                    lectures[-1]['reading'] = schedule_day['reading']

            if schedule_day['recitation']['name'] != '':
                recitation = schedule_day['recitation']
                recitation['date'] = schedule_day['date']

        else:
            if schedule_day['homework']['name'] != '':
                last_homework = schedule_day['homework']
                last_homework['date'] = schedule_day['date']

output = {
    "last_homework": last_homework,
    "next_homework": next_homework,
    "recitation": recitation,
    "lectures": lectures
}

with open(r'this_week.yaml', 'w') as file:    
    documents = yaml.dump(output, file, Dumper=LineBreakDumper, default_flow_style=False)
