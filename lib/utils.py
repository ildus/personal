#-*-coding:utf-8-*-

def make_upload_path(instance, filename):
    import datetime
    import os
    
    now = datetime.datetime.now()
    path, ext = os.path.splitext(filename)
    fn = "f%s%s%s%s%s%s"%(now.year, now.month, now.day, now.hour, now.minute, now.second)
    return "uploads/%s%s"%(fn, ext)