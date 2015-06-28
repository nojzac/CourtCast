# Import libraries
import os
import re

# Initialize variables 
count = 0

dir_origin = "data/c010_original_oral_arguments_txt/"
dir_target = "data/c020_cleaned_txt/"

strs_to_replace = ["ALDERSON REPORTING COMPANY, INC.",
				   "1111 FOURTEENTH STREET, N.W.",
				   "SUITE 400",
				   "WASHINGTON, D.C. 20005",
				   "(202)289-2260",
				   "(800) FOR DEPO",
				   "800-FOR-DEPO",
				   "Alderson Reporting Company",  ###!!! Added this on 6/24/2015
				   "Official"
				   ]

# Cycle through text files of oral arguments to replace repetitve strings
for fn in os.listdir(dir_origin):
	count += 1
	if 'c_' + fn in os.listdir(dir_target):
		os.remove('c_' + fn)
	
	input_file = open(dir_origin + fn, "r").read()

	for s in strs_to_replace:
		input_file = input_file.replace(s, '')

	output_file = open(dir_target + 'c_' + fn, 'w')
	output_file.write(input_file)
	output_file.close()

	if count % 50 == 0:
		print 'Count: ', count