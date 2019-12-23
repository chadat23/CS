https://www.eecs.mit.edu/curriculum2017
https://www.eecs.mit.edu/docs/ug/new_curriculum_63.pdf

https://stackoverflow.com/questions/58422817/jupyter-notebook-with-python-3-8-notimplementederror

"
For those that can't wait for an official fix, I was able to get it working by editing the file tornado/platform/asyncio.py, by adding:

import sys

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())"



https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/

https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-01sc-introduction-to-electrical-engineering-and-computer-science-i-spring-2011/unit-1-software-engineering/state-machines/
