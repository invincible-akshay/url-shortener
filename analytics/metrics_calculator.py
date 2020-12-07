import os
from collections import defaultdict

# these belows values need to be configured accordingly

# total number of urls visited
total_urls_read = 69562876
# dir = "/home/ec2-user/"
mapreduce_output_dir = "/Users/vamshimuthineni/PycharmProjects/FCNProject/data/urls_output/"
# storing the percentage of each domain visited
final_result_file = open("/Users/vamshimuthineni/PycharmProjects/FCNProject/data/final_result2.txt", "a")
# optional, storing less frequent domains separately.
small_domains = open("/Users/vamshimuthineni/PycharmProjects/FCNProject/data/small_domains.txt", "a")


percent_dict = defaultdict(float)
# reading all the output files from the cluster
files = [i for i in os.listdir(mapreduce_output_dir) if os.path.isfile(os.path.join(mapreduce_output_dir, i)) and
         'part-' in i]

for file_name in files:
    file1 = open(dir+file_name, 'r')
    lines = file1.readlines()
    for line in lines:
        line = line.rstrip()
        # the output from the map reduce was a tuple of url and count
        line = line.replace('(', '')
        line = line.replace(')', '')
        splits = line.split(",")
        if len(splits)<1:
            continue
        if int(splits[1])<100:
            small_domains.write(line)
            small_domains.write("\n")
            continue
        percent_dict[splits[0]] = int(splits[1])*100.0/total_urls_read


# storing the result in descending order
percent_dict = dict(sorted(percent_dict.items(), key=lambda item: item[1], reverse=True))

for domain in percent_dict:
    final_result_file.write(domain + "," + str(percent_dict[domain]))
    final_result_file.write("\n")
