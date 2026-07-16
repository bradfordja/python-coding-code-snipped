# Counting Minutes

## Question: 
## Return the number of minutes between two times.

def counting_minutes(time_str):
    start, end = time_str.split("-")

    def to_minutes(t):
        period = t[-2:]
        hour, minute = map(int, t[:-2].split(":"))

        if period == "pm" and hour != 12:
            hour += 12
        if period == "am" and hour == 12:
            hour = 0

        return hour * 60 + minute

    start_min = to_minutes(start)
    end_min = to_minutes(end)

    if end_min < start_min:
        end_min += 24 * 60

    return end_min - start_min

print(counting_minutes("12:30pm-12:00am"))  # Output: 690
print(counting_minutes("12:30am-12:00pm"))  # Output: 690
print(counting_minutes("1:00pm-11:00am"))  # Output: 1320
print(counting_minutes("1:00am-11:00pm"))  # Output: 1320
print(counting_minutes("1:00am-1:00am"))  # Output: 0

## Interview note: Convert both times to minutes after midnight.
## Complexity: O(1)