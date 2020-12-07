import urllib.request
import urllib

url = "https://archive.org/compress/urlteam_-placeholder-/formats=ZIP&file=/urlteam_-placeholder-.zip"
count = 0

# tried generating the file names initially but too slow and too less number of hits hence got the file names from
# the archive.org website by some javascript dom manipulation

# year = "2020"
# for month in range(1,12):
#     for day in range(1,31):
#         for hour in range(0,23):
#             for minute in range(0,59):
#                 for sec in range(0,59):
#                     if count == 100:
#                         exit(1)
#                     filename = year + "-" + "{0:0=2d}".format(month)\
#                                + "-" + "{0:0=2d}".format(day)\
#                                + "-" + "{0:0=2d}".format(hour)\
#                                + "-" + "{0:0=2d}".format(minute)\
#                                + "-" + "{0:0=2d}".format(sec)


# this can be configured accordingly
dir = "/Users/vamshimuthineni/PycharmProjects/FCNProject/"
# dir = "/home/ec2-user/"

# the gathered filenames are stored in the following file
file1 = open(dir+'filenames.txt', 'r')

lines = file1.readlines()
for line in lines:
    line = line.rstrip()
    url2 = url.replace("-placeholder-", line)

    try:
        filename, _ = urllib.request.urlretrieve(url2, dir+line+".zip")
    except urllib.error.HTTPError:
        pass
    print("done " + url2)