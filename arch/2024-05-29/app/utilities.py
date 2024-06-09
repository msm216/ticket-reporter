import os
import datetime






def get_last_modified_time(directory):
    
    latest_time = None
    for root, dirs, files in os.walk(directory):
        for fname in files:
            filepath = os.path.join(root, fname)
            file_mtime = datetime.datetime.fromtimestamp(os.path.getmtime(filepath))
            if latest_time is None or file_mtime > latest_time:
                latest_time = file_mtime
    return latest_time

