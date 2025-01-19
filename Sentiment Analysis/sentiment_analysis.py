"""
Ali Ajwani
November 17, 2023
"""

# This code has many functions which are used to read, clean, process, analyze, and report on the tweets in the given dataset

# The read_keywords function reads keywords from a .tsv file and the scores that are associated with those keywords
# It then takes that information and inputs it into a dictionary which is what is returned
def read_keywords(keyword_file_name):
   keyword_dict = {}
   try:
       with open(keyword_file_name, 'r') as file:
           for line in file:
               keyword, score = line.strip().split('\t')
               keyword_dict[keyword] = int(score)
   except IOError:
       print(f"Could not open file {keyword_file_name}!")
   return keyword_dict

# The clean_tweet_text converts the tweet to lowercase and removes and text that is not a space or a letter
def clean_tweet_text(tweet_text):
    lowercase_text = tweet_text.lower()
    cleaned_text = ""
    for char in lowercase_text:
        if char.isalpha() or char.isspace():
            cleaned_text += char
    return cleaned_text

# The read_tweets function reads and processes tweets from a file and then adds each tweet to a dictionary
def read_tweets(tweet_file_name):
   tweet_list = []
   try:
       with open(tweet_file_name, 'r') as file:
           for line in file:
               fields = line.strip().split(',')
               tweet_dict = {
                   'date': fields[0],
                   'text': clean_tweet_text(fields[1]),
                   'user': fields[2],
                   'retweet': int(fields[3]),
                   'favorite': int(fields[4]),
                   'lang': fields[5],
                   'country': fields[6],
                   'state': fields[7],
                   'city': fields[8],
                   'lat': float(fields[9]) if fields[9] != 'NULL' else 'NULL',
                   'lon': float(fields[10]) if fields[10] != 'NULL' else 'NULL',
               }
               tweet_list.append(tweet_dict)
   except IOError:
       print(f"Could not open file {tweet_file_name}!")
   return tweet_list

# The calc_sentiment function calculates the sentiment score of a tweet based on the text in the tweet
def calc_sentiment(tweet_text, keyword_dict):
   words = tweet_text.split()
   sentiment_score = 0
   for word in words:
       word_score = keyword_dict.get(word, 0)
       sentiment_score += word_score
   return sentiment_score

# The classify function classifies the sentiment score as positive, negative or neutral
def classify(score):
   if score > 0:
       return 'positive'
   elif score < 0:
       return 'negative'
   else:
       return 'neutral'

# The make_report function generates the full report for the sentiment analysis
def make_report(tweet_list, keyword_dict):
    num_tweets = len(tweet_list)
    if num_tweets == 0:
        return {'avg_favorite': 'NAN', 'avg_retweet': 'NAN', 'avg_sentiment': 'NAN', 'num_favorite': 0,
                'num_negative': 0, 'num_neutral': 0, 'num_positive': 0, 'num_retweet': 0, 'num_tweets': 0,
                'top_five': ''}
    # Initiate counters
    total_sentiment = 0
    num_positive = 0
    num_negative = 0
    num_neutral = 0
    num_favorite = 0
    total_favorite_sentiment = 0
    num_retweet = 0
    total_retweet_sentiment = 0
    countries_sentiment = {}

    # Process each tweet
    for tweet in tweet_list:
        sentiment = calc_sentiment(tweet['text'], keyword_dict)
        total_sentiment += sentiment

        # Classify the sentiment of a tweet and add to the appropriate counters
        classification = classify(sentiment)
        if classification == 'positive':
            num_positive += 1
        elif classification == 'negative':
            num_negative += 1
        else:
            num_neutral += 1

        # Check for favourite and retweets and add to the appropriate counters
        if tweet['favorite'] > 0:
            num_favorite += 1
            total_favorite_sentiment += sentiment

        if tweet['retweet'] > 0:
            num_retweet += 1
            total_retweet_sentiment += sentiment

        # Process the sentiment for countries
        if tweet['country'] != 'NULL':
            country = tweet['country']
            if country not in countries_sentiment:
                countries_sentiment[country] = {'total_sentiment': 0, 'num_tweets': 0}
            countries_sentiment[country]['total_sentiment'] += sentiment
            countries_sentiment[country]['num_tweets'] += 1

    # Calculate averages for the sentiment, favourites and retweets
    avg_sentiment = round(total_sentiment / num_tweets, 2) if num_tweets > 0 else 'NAN'
    avg_favorite_sentiment = round(total_favorite_sentiment / num_favorite, 2) if num_favorite > 0 else 'NAN'
    avg_retweet_sentiment = round(total_retweet_sentiment / num_retweet, 2) if num_retweet > 0 else 'NAN'

    # Determine the top five countries
    sorted_countries = sorted(countries_sentiment, key=lambda country: (countries_sentiment[country]['total_sentiment'] / countries_sentiment[country]['num_tweets']), reverse=True)
    top_five_countries = ', '.join(sorted_countries[:5])

    # Compile report
    report = {
        'avg_sentiment': avg_sentiment,
        'num_tweets': num_tweets,
        'num_positive': num_positive,
        'num_negative': num_negative,
        'num_neutral': num_neutral,
        'num_favorite': num_favorite,
        'avg_favorite': avg_favorite_sentiment,
        'num_retweet': num_retweet,
        'avg_retweet': avg_retweet_sentiment,
        'top_five': top_five_countries
    }
    return report

# The write_report function writes out the report from the make_report section
def write_report(report, output_file):
    try:
        with open(output_file, 'w') as file:
            for key, value in report.items():
                file.write(f"{key}: {value}\n")
        print(f"Wrote report to {output_file}")
    except IOError:
        print(f"Could not open file {output_file}")
