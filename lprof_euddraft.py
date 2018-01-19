import os
import subprocess
import datetime
import time


curTime = datetime.datetime.now().strftime("%B %d, %Y - I:%M%p")

print("Running script")
st = time.time()
os.system("kernprof -l ed_profile.py")
execTime = time.time() - st
print("Execute time = %fs" % execTime)

profile_result = subprocess.check_output(
    "python -m line_profiler ed_profile.py.lprof",
    shell=True
).decode('utf-8').replace("\r\n", "\n")
print(profile_result)

with open('lprof_log.txt', 'a') as lprof_fp:
    lprof_fp.write("[%s]: Total execution time %.4fs\n%s\n\n\n" %
                   (curTime, execTime, profile_result))
