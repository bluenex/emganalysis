__author__ = 'tulakan'

topdir = 'D:\Dropbox\Rehabilitation Project\EMG data\EMG Gyro 26-27 Aug'
extens = ['asc']  # the extensions to search for
found = {x: [] for x in extens} # lists of found files
# Walk the tree
for dirpath, dirnames, files in os.walk(topdir):
    # Loop through the file names for the current step
    for name in files:
        # Split the name by '.' & get the last element
        ext = name.lower().rsplit('.', 1)[-1]

        # Save the full name if ext matches
        if ext in extens:
            found[ext].append(os.path.join(dirpath, name))

fontPath = found[ext]
# print fontPath