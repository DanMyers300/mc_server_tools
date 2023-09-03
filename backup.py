import os
from datetime import date

today = date.today()
os.system("screen -X -S minecraft quit")
os.system(f"cd /home/admin/minecraft && git add . && git commit -m \"{today}\" && git push origin prod && cd ~")
