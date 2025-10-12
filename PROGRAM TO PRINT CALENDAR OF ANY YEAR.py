#ACCORDING TO GREGORIAN CALENDAR

import calendar
year =int(input("Which Year Calendar You Want To See? : "))

if year>0000 and year<10000:
    print(calendar.calendar(year))
else:
    print("Year Entered Is Invalid")

