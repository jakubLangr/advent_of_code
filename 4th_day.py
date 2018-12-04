from collections import defaultdict, namedtuple
from datetime import datetime as dt, timedelta

import pandas as pd

test_file_name = 'day4_test_case.txt'
file_name = 'day4_input.txt'
event_log = namedtuple('EventLog', ['time','event'])

def corrected_date(event: tuple):
    date = dt.strptime(event[0][1:], '%Y-%m-%d %H:%M')
    if date.hour==23:
        new_date = date + timedelta(days=1)
        str_date = str(new_date.date())
        date = dt.strptime(str_date + ' 00:00', '%Y-%m-%d %H:%M')
    if date.minute!=00 and event[1].startswith('Guard'):
        date = dt.strptime(str(date.date()) + " 00:00", '%Y-%m-%d %H:%M')
    return date

def load_format(file_name: str):
    file_object = open(file_name, 'r')
    loaded = file_object.read()
    split_s = loaded.split('\n')
    current_events = [x.split('] ') for x in split_s ]
    formatted_events = [event_log(corrected_date(x), x[1])
                         for x in current_events ]
    return formatted_events

formatted_log = load_format(test_file_name)
# print(formatted_log)

def pad_awake_list(asleep_list):
    # import ipdb; ipdb.set_trace()
    flat_list = [item for sublist in asleep_list for item in sublist]
    if len(flat_list) < 60:
        diff = 60 - len(flat_list)
        return flat_list + [0] * diff
    elif len(flat_list)==60:
        return flat_list

def preprocessing(file_name: str):
    formatted_log = load_format(file_name)
    structured_dict = defaultdict(list)
    for e in formatted_log:
        if e.event.startswith('Guard'):
            guard_id = f"{e.event.split(' ')[1]}-{e.time.date()}"
        structured_dict[guard_id].append(e)

    struct_sum = namedtuple('StructuredSummary', ['tawake','tasleep'])
    sum_dict = defaultdict(list)
    dict_asleep_patterns = defaultdict(list)

    for k in structured_dict.keys():
        awake = True
        tasleep = 0
        tawake = 0
        events = structured_dict[k]
        # import ipdb; ipdb.set_trace()
        for e in events:
            if e.event.startswith('Guard'):
                prev_time = e.time
            delta = e.time - prev_time
            if e.event == 'falls asleep' and awake==True:
                awake = False
                dict_asleep_patterns[k].append([
                    0] * (int(delta.total_seconds() / 60)))
                tawake += delta.total_seconds() / 60
                prev_time = e.time
            if e.event == 'wakes up' and awake==False:
                awake = True
                dict_asleep_patterns[k].append([
                    1] * (int(delta.total_seconds() / 60) ))
                tasleep += delta.total_seconds() / 60
                prev_time = e.time
        
        guard_id = k.split('-')[0]
        structured_dict[k].append(struct_sum(tawake, tasleep))
        sum_dict[guard_id].append(struct_sum(tawake, tasleep))
    
    useful_list = [pad_awake_list(dict_asleep_patterns[x]) for x in dict_asleep_patterns.keys()]
    df = pd.DataFrame(useful_list)
    import ipdb; ipdb.set_trace()
    df.index = structured_dict.keys()
    return sum_dict, df

# test_final, test_df = preprocessing(test_file_name)
# final, df = preprocessing(test_file_name)


def most_asleep_guard(final: dict):
    asleep_dict = defaultdict(int)
    max_asleep = '?'
    for g in final.keys():
        total_asleep = 0
        for e in final[g]:
            total_asleep += e.tasleep
        
        if max_asleep=="?":
            max_asleep = g
        elif total_asleep>=max(asleep_dict.values()):
            max_asleep = g
        asleep_dict[g] = total_asleep

    return int(max_asleep[1:])


def day_four(file_name: str):
    final, df = preprocessing(file_name)
    most_asleep_guard_result = most_asleep_guard(final)
    # # PLACEHOLDER MISSING MOST LIKLEY MIN
    shifts_most_asleep_guard = df[df.index.str[1:].str.startswith(str(most_asleep_guard_result))]
    most_asleep_min = shifts_most_asleep_guard.sum().sort_values().index[59]
    return most_asleep_min * most_asleep_guard_result


# print(day_four(test_final, test_df))
print(day_four(file_name))

TARGET_ID = 10 
TARGET_MINUTE = 24 
print(day_four(final, df) == TARGET_ID*TARGET_MINUTE)