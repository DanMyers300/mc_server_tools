import os
from datetime import date
today = date.today()

os.chdir("/home/admin/minecraft")
os.system(f"git add . && git commit -m \"{today}\" && git push origin main")
