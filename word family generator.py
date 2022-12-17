#!/usr/bin/env python3.10
# coding: utf-8

import pandas as pd
import re
import json

from timeis import timeis, yellow, line, white, green, tic, toc
from delete_unused_files import del_unused_files


def setup_dpd_df():
	print(f"{timeis()} {green}setting up dpd dataframe", end=" ")

	dpd_df = pd.read_csv("../csvs/dpd-full.csv", sep="\t", dtype=str)
	dpd_df.fillna("", inplace=True)
	dpd_df_length = len(dpd_df)
	print(f"{white} {len(dpd_df)}")
	return dpd_df, dpd_df_length


def generate_set_of_word_families():
	print(f"{timeis()} {green}generating set of all word families", end = " ")
	word_families_set = set()

	for row in range(dpd_df_length):
		word_family = dpd_df.loc[row, "Word Family"]
		words = word_family.split(" ")
		for word in words:
			word_families_set.add(word)
	
	word_families_set.remove("")
	print(f"{white} {len(word_families_set)}")
	return word_families_set

def generate_word_family_html():
	print(f"{timeis()} {green}generating word family html")
	dpd_df.loc[dpd_df["Meaning IN CONTEXT"] == "", "Meaning IN CONTEXT"] = dpd_df["Buddhadatta"]
	dpd_df.loc[dpd_df["Literal Meaning"] != "", "Meaning IN CONTEXT"] += "; lit. " + dpd_df["Literal Meaning"]

	counter = 0
	word_families_set_length = len(word_families_set)

	for word_family in word_families_set:
		
		word_family_dict = {}
		html_string = ""

		# if counter % 25 == 0:
		print(f"{timeis()} {counter}/{word_families_set_length}\t{word_family}")

		test1 = dpd_df["Word Family"] != ""
		test2 = dpd_df["Word Family"].str.contains(f"\\b{word_family}\\b")
		filter = test1 & test2
		word_family_df = dpd_df.loc[filter, ["Pāli1", "POS", "Meaning IN CONTEXT"]]

		if word_family_df.shape[0] > 0:
			html_string = f"""<table class = "table1">"""
			length = word_family_df.shape[0]

			for row in range(length):
				pali = word_family_df.iloc[row, 0]
				pos = word_family_df.iloc[row, 1]
				meaning = word_family_df.iloc[row, 2]
				html_string += f"""<tr><th>{pali}</th><td>{pos}</td><td>{meaning}</td></tr>"""
			
			html_string += """</table>"""
		
		html_for_json = re.sub("table1", "word family", html_string)
		word_family_dict[word_family] = html_for_json

		with open(f"output/html/{word_family}.html", "w") as f:
			f.write(html_string)
	
		counter += 1

	word_family_json = json.dumps(word_family_dict, ensure_ascii=False, indent=4)
	with open("../dpd-app/data/word families.json", "w") as f:
		f.write(word_family_json)


def delete_unused_files():

	file_dir = "output/html/"
	file_ext = ".html"
	del_unused_files(word_families_set, file_dir, file_ext)


tic()
print(f"{timeis()} {yellow}word families generator")
print(f"{timeis()} {line}")
dpd_df, dpd_df_length = setup_dpd_df()
word_families_set = generate_set_of_word_families()
generate_word_family_html()
delete_unused_files()
toc()