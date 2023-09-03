import os
from datetime import date
today = date.today()

os.system(f"cd ~/minecraft && git add . && git commit -m \"{today}\" && git push origin prod && cd ~")
