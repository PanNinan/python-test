import os
import sys
import time

print(os.path.dirname(os.path.dirname(__file__)))
print(__file__)

# os.makedirs('t1/t2')
# os.removedirs('t1/t2')


for item in os.environ:
    print('-' * 120)
    print(item + ': ' + os.environ[item])

print(os.stat(__file__))

# sys.exit(250)

for i in range(100):
    sys.stdout.write('#')
    sys.stdout.flush()
    time.sleep(0.1)
