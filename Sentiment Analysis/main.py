"""
CS1026a 2023
Assignment 03 - main.py
Ali Ajwani
251374819
aajwani2
November 17, 2023
"""

# This code asks users for the keyword and tweet filenames, and then returns a report of the files in a new .txt file which is also named by the user

# Import the sentiment_analysis functions needed to write the report
from sentiment_analysis import read_keywords, read_tweets, make_report, write_report

def main():
   try:
       # Prompt user for input file names
       keyword_filename = input("Input keyword filename (.tsv file): ")
       tweet_filename = input("Input tweet filename (.csv file): ")
       report_filename = input("Input filename to output report in (.txt file): ")

       # Make sure user enters proper file types
       if not keyword_filename.lower().endswith('.tsv'):
           raise Exception("Must have tsv file extension!")
       if not tweet_filename.lower().endswith('.csv'):
           raise Exception("Must have csv file extension!")
       if not report_filename.lower().endswith('.txt'):
           raise Exception("Must have txt file extension!")

       # Read the data from the files
       keyword_dict = read_keywords(keyword_filename)
       tweet_list = read_tweets(tweet_filename)


       # Make sure the files are not empty
       if not keyword_dict:
           raise Exception("Keyword dictionary is empty!")
       if not tweet_list:
           raise Exception("Tweet list is empty!")


       # Create and write the report
       report = make_report(tweet_list, keyword_dict)
       write_report(report, report_filename)

    # Address what the output should be for any file not found errors or other exceptions that were not already addressed
   except FileNotFoundError as e:
       raise Exception(f"Error: {e.filename} not found.")
   except Exception as e:
       raise Exception(f"Error: {e}")


if __name__ == "__main__":
   main()

