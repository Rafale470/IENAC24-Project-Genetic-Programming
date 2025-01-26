import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(os.path.join(os.path.dirname(__file__), 'not_recursive_genetic'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'recursive_genetic'))

from not_recursive_genetic import main as not_rec_main
from recursive_genetic import main as rec_main
import tracemalloc
import matplotlib.pyplot as plt
import time

x = list(range(100))

yt_not_rec, ym_not_rec = [], []
for j in range(100):
    y1 = []
    y2 = []
    for i in range(10):
        print(f"Boucle {i}")
        tracemalloc.start()
        start_time = time.time()
        start = tracemalloc.get_traced_memory()[1]
        not_rec_main.main(f"simulation_configs/config_simulation_{j}.txt")
        end = tracemalloc.get_traced_memory()[1]
        end_time = time.time()
        tracemalloc.stop()
        y1.append(end-start)
        y2.append(end_time-start_time)
    ym_not_rec.append(sum(y1)/len(y1))
    yt_not_rec.append(sum(y2)/len(y2))

yt_rec, ym_rec = [], []
for j in range(100):
    y1 = []
    y2 = []
    for i in range(10):
        print(f"Boucle {i}")
        tracemalloc.start()
        start_time = time.time()
        start = tracemalloc.get_traced_memory()[1]
        rec_main.main(f"simulation_configs/config_simulation_{j}.txt")
        end = tracemalloc.get_traced_memory()[1]
        end_time = time.time()
        tracemalloc.stop()
        y1.append(end-start)
        y2.append(end_time-start_time)
    ym_rec.append(sum(y1)/len(y1))
    yt_rec.append(sum(y2)/len(y2))

print(yt_not_rec, ym_not_rec)
print(yt_rec, ym_rec)


plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)  
plt.plot(x, yt_not_rec, label='not_rec', color='b')
plt.plot(x, yt_rec, label='rec', color='r')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Temps necessaire')
plt.legend()


plt.subplot(1, 2, 2)  
plt.plot(x, ym_not_rec, label='not_rec', color='g')
plt.plot(x, ym_rec, label='rec', color='m')
plt.xlabel('y')
plt.ylabel('z')
plt.title('Espace mémoire necessaire')
plt.legend()


plt.tight_layout()
plt.show()
