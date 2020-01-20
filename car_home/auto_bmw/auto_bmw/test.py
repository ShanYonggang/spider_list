import os
path = os.path.join(os.path.dirname(os.path.dirname(__file__)),'image')
if not os.path.exists(path):
    os.mkdir(path)
else:
    print("Path already exist......")