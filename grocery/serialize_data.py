import os
import sys

rootdir = sys.argv[1]

output_file = open("output.txt","w")
header = "order_date|time_slot|item|quantity_uom|price\n"
output_file.write(header)
print("Reading from '{}'".format(rootdir))

for file_name in os.listdir(rootdir) :
    print("Processing {}".format(file_name))
    fobj = open(rootdir + file_name)
    counter = 0
    (order_date, order_slot) = file_name.split("_")
    csv_line = order_date +"2018" + "|" + order_slot
    for line in fobj :
        line = line.rstrip("\r\n")
        csv_line += "|" + line
        counter += 1
        if counter == 3 :
            output_file.write(csv_line + "\n")
            csv_line = order_date +"2018" + "|" + order_slot
            counter = 0
    fobj.close()
    
output_file.close()
