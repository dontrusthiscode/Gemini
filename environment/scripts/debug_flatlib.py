
from flatlib.datetime import Datetime
d = Datetime('2007/04/24', '04:15', '+03:00')
print(f"Type: {type(d)}")
print(f"Date Type: {type(d.date)}")
print(f"Date Dir: {dir(d.date)}")
print(f"Date Str: {d.date}")
try:
    print(f"Year: {d.date.year}")
except Exception as e:
    print(f"Error accessing year: {e}")

print(f"ToList: {d.date.toList()}")
print(f"Date toString: {d.date.toString()}")
print(f"Time toString: {d.time.toString()}")

