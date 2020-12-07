import lzma
import zipfile
import os
from collections import defaultdict

# the below values needs to be configured at accordingly

# file names  with data dump are stored in a separate file
file1 = open('filenames.txt', 'r')
# dir = "/home/ec2-user/"
dir = "/Users/vamshimuthineni/PycharmProjects/FCNProject/data/"


# extracting two types of shortened urls. you might want to add others if you want.
goo_gle_extension = "goo-gl."
bit_ly_extension = "bitly_6."
zipped_paths = [dir + 'goo-gl/', dir + "bitly_6/"]

file_names = file1.readlines()

for filename in file_names:

    filename = filename.rstrip()
    zip_filepath = dir + filename + ".zip"

    if not os.path.isfile(zip_filepath):
        continue

    with zipfile.ZipFile(zip_filepath, 'r') as zip_ref:
        zip_ref.extractall(dir)

    google_zip_path = dir + goo_gle_extension + filename + ".zip"
    bitly_6_zip_path = dir+ bit_ly_extension + filename + ".zip"

    # extracting google zip
    if os.path.isfile(google_zip_path):
        with zipfile.ZipFile(google_zip_path, 'r') as zip_ref:
            zip_ref.extractall(dir)

    # extracting bitly zip
    if os.path.isfile(bitly_6_zip_path):
        with zipfile.ZipFile(bitly_6_zip_path, 'r') as zip_ref:
            zip_ref.extractall(dir)

    # output for each file, all these files will be merged and passed to map reduce cluster
    result_file = open(dir + "result_" + filename + ".txt", "a")
    result_map = defaultdict(int)
    for path in zipped_paths:
        if not os.path.isdir(path):
            continue

        # extracted files might be too large.
        files = [i for i in os.listdir(path) if os.path.isfile(os.path.join(path, i)) and
                 '___' in i and '.xz' in i]

        for file in files:
            xz_lines = lzma.open(path+file).readlines()

            for xz_line in xz_lines:
                xz_line = xz_line.decode('utf-8')

                if "|" in xz_line:
                    main_split = xz_line.split("|")
                    if len(main_split)<2:
                        continue
                    url = main_split[1]
                    if "https://" in url:
                        splits = url.split("https://")[1].split("/")
                        domain = splits[0]
                        domain = domain.rstrip()
                        result_map[domain] += 1

                    elif "http://" in url:
                        splits = url.split("http://")[1].split("/")
                        domain = splits[0]
                        domain = domain.rstrip()
                        result_map[domain] += 1

    # storing the result in reverse
    result_map = dict(sorted(result_map.items(), key=lambda item: item[1], reverse=True))

    for domain in result_map:
        result_file.write(domain + "," + str(result_map[domain]))
        result_file.write("\n")