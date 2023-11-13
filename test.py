from datetime import datetime
import requests
import json

val = datetime.strptime("11/11/2023", "%d/%m/%Y").date()
today = datetime.today().date()
diff = today - val
print(diff.days)
# .strftime("%d/%m/%Y")

with open("") as file:
    file.truncate(0)
