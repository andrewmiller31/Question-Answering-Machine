'''
Andrew Miller
12/7/2018
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Question Answering Machine (QAM)

The purpose of this program is to answer queries from the user by extracting 
data from Wikipedia, using the wikipedia library. The approach I used is based 
roughly on the strategies of the question-answering system AskMSR, namely query-
reformulation, n-gram mining, filtering, and tiling. Here is a brief walkthrough
of what typically happens when a question is asked, highlighting the key features.

user > Where is The Liberty Bell?

processing:
* Recognize the question is of the form 'Where is' 
* Trim search query to 'The Liberty Bell' 
* Search Wikipedia for 'The Liberty Bell' and load the result
* Split the document into a list of sentences
* Scan the document's sentences for several different forms that the answer might 
  be framed such as: X is located in Y ; X is in Y : X is at Y
* For each match found, save the entire sentence
* Trim the sentences to hold only relevant information using keywords
* For each sentence, split into every possible ngram and add to a list
* Sort the list by frequency and construct the answer based on the most frequent 
  answers that overlap.
* Print the answer

QAM > The Liberty Bell is located in the Liberty Bell Center in Independence 
National Historical Park.

If there are suitable answers found or the question type is not recognized, QAM 
appologizes and says the answer could not be found. 

FUTURE WORK
- Fine tune the question restructuring and filtering
- Deal with the problem of verb tense. For example, if the user asks "When did 
  Steve Jobs create Apple?", the program won't know to search for "Steve Jobs
  created Apple in ___" and would instead search something like "Steve jobs
  create Apple in ___" which likely wouldn't find any matches.  

TO RUN
python qa.py <log file name>

'''
import wikipedia as wp # wikipedia library
import re # regular expressions
import sys # used for taking command line args

f = None # global file used for writing logs
# Regular expressions to define months and days
months = '(january|jan\.|february|feb\.|march|mar\.|april|apr\.|may|june|jun\.|july|jul\.|august|aug\.|semptember|sept\.|october|oct\.|november|nov\.|december|dec\.)' 
days = '(monday|tuesday|wednesday|thursday|friday|saturday|sunday)'

# Regular expressions to define the different formats that dates can appear in 
re_date = []
re_date.append( r'(\d(\d)?\s'+months+r'(\,)?\s\d+)' )
re_date.append( r'('+months+r'\s\d(\d)?(\,)?\s\d+)' )
re_date.append( r'(\d(\d)?\s'+months+r')' )
re_date.append( r'('+months+r'\s\d(\d)?)' )
re_date.append( r'\s([io]n)\s.+('+days+'|'+months+').+' )
re_date.append( r'in\s\d+' )

# This function searches for a Wikipedia article based on the provided phrase q
# The result is a list of raw text of the pages containing either the summaries
# or the entire page, depending of the toggle of summary
def search(q,summary=False):
  # I originally pulled the first 5 results but I found that it introduced too much
  # noise so I decided to stick with just the first result
  s = wp.search(q,1) 
  write_log('Search results of: \'' + q + '\'')
  # Encode the unicode results to ascii so they can be written to the log
  for i in range(0,len(s)):
    s[i] = s[i].encode('ascii','ignore')
  write_log(','.join(s))
  # returns a list of loaded and formatted wikipedia content
  return load_pages(s,summary) 

# finds the sentences in each document that match the regular expression p
def find_phrase(p,docs):
  write_log('Searching documents for \'' + p + '\'...')
  # a list to hold all the matching sentences
  matches = []
  # for each document, iterate through the sentences
  for d in docs:
    for sent in d[1]:
      # search for re match
      s = re.search(p,sent,flags=re.I)
      # if there's a match append
      if s:
        write_log('Found match: ' + s.group(0))
        matches.append(s.group(0))
  return matches # return all matching sentences

# This function takes a list of regular expresssions and finds the matching
# sentences for each in each document
def find_phrases(phrases,docs):
  matches = [] # a list to track all matches
  # for each regular expression find the matches and add to the list
  for p in phrases:
    new_matches = find_phrase(p,docs)
    for nm in new_matches:
      matches.append(nm)
  return matches

# Loads a list of wikipedia pages and extracts either the content or the
# summary. The text is then processed to be a list of individual sentences
# It should be noted that this currently only uses a list of one since I 
# decided that working with multiple pages results in too much noise.
def load_pages(p,summary):
  pages = [] # a list to hold the page text
  for name in p:
    try:
      # check the summary toggle to see if the summary or full content is needed
      if summary == True:
        cur_page = wp.page(name).summary.encode('ascii','ignore')
      else:
        cur_page = wp.page(name).content.encode('ascii','ignore')
      # split into sentences
      sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s',cur_page)
      # add as a tuple with the name so we can see what document is being used later
      pages.append((name,sentences))
    except wp.DisambiguationError:
      write_log('Disambiguation error in search for \'' + name + '\'')
  return pages 

# This function finds matches for the regular expression dates listed above from
# a list of sentences.
# matches is a list of sentences that is assumed to contain possible answers for 
# the users question
def find_dates(matches):
  dates = []
  write_log('Searching matches for dates...')
  # for each match go through the list of expressions until a match is found or
  # the end of the list is reached
  for m in matches:
    d = re.search(re_date[0],m,re.I)
    for i in range(1,len(re_date)):
      if not d:
	d = re.search(re_date[i],m,re.I)
    # if a date was found, trim to just contain the date and append
    if d:
      date = re.sub(r'\b[io]n\s','',d.group(0),1,re.I)
      dates.append(date)
      write_log('Found date: ' + date)
  return dates

# This function seperates a list of possible answers into ngrams and tiles 
# them to construct the final answer.
def choose_best(phrases):
  write_log('Tiling the response...')
  # If there were no possible answers found, return None
  if phrases == []:
    return None
  # a list to hold the phrases seperated into single words
  sentences = [] 
  # a list that will hold the candidate ngrams
  choices = []
  # split the sentences into an array of words and append to list
  for p in phrases:
    sentences.append(p.split())
  # for each list of words, start from beginning and add one to the ngram,
  # appending the result each time until the end is reached
  for s in sentences:
    cur_phrase = []
    for i in range(0,len(s)):
      cur_phrase.append(s[i])
      choices.append(' '.join(cur_phrase))
  # sort the list of all ngrams from all sentences by count
  s_choices = sorted(choices,key=choices.count,reverse=True)
  # start with the most frequent word
  best = s_choices[0]
  i = 1
  # iterate through the list, starting from the highest count and tile if 
  # the phrase is contained in the next phrase
  while i < len(s_choices):
    if re.search(re.escape(best),s_choices[i]):
      best = s_choices[i]
    i += 1
  # sub out information in parenthesis because it's usually noise anyway
  best = re.sub(r'\(.+\)\s','',best) 
  return best

# This is the function used when the user asks a 'when' question
# The function prioritizes finding answers with dates in them, if that's 
# not found, then it looks for more vague answers. 
def ask_when(q):
  write_log('User asked a \'when\' question.')
  matches = [] # list of all re matches
  phrases = [] # list of re phrases used for searching  
  dates = [] # list of dates found
  start = '' # The start of the response
  # if asking 'when is' or 'when was'
  if q[1].lower() == 'is' or q[1].lower() == 'was':
    # extract information from the question to phrase the answer
    # ex) 'When is Thanksgiving?' would change to 'Thanksgiving is '
    start = ' '.join(q[2:]) + ' ' + q[1] + ' '
    # all words after is/was are used to search wikipedia
    pages = search(' '.join(q[2:]))
    i = 2
    # while there are words to trim from the answer, search until matches 
    # are found
    while i < len(q) and matches == []:  
      # append the reformated question 
      phrases.append(' '.join(q[i:]) + r'.+(is|was)(on)?\s.+')
      # search for matches for the above expression
      matches = find_phrases(phrases,pages)
      i += 1
    # search for dates found in the matches
    dates = find_dates(matches)
  # sometimes was questions have a different form so there is further searching
  # ex) 'When was WWII?' would fit above but belove is needed for 'When was Bill
  # Clinton born'
  if q[1].lower() == 'was':
    # rephrase response
    start2 = ' '.join(q[2:-1]) + ' was ' + q[-1] + ' '
    # get the wiki page
    pages = search(' '.join(q[2:-1]))
    i = 2
    matches2 = []
    phrases = []
    # search for variations of '___ was ___ in/on/from ___'
    while i < len(q) and matches2 == []:
      phrases.append(' '.join(q[i:-1]) + r'\s(was)?(\s)?' + q[-1] + r'(\s)?(in|on|from)?\s?.+')
      phrases.append(' '.join(q[i:]) + r'\swas\s.+')
      matches2 = find_phrases(phrases,pages)
      i += 1
    # find dates in the second list of matches
    dates2 = find_dates(matches2)
    # append the new dates to the original list
    for d in dates2:
      dates.append(d)
    # choose the best one 
    dt = choose_best(dates)
    # if it was chosen from one of the new dates, change the response form
    if dt in dates2:
      start = start2
    # if no suitable answer was found, clear all possible responses because it 
    # would likely be wrong
    if dates == []:
      matches = []
  # 'when did' questions go here
  elif q[1].lower() == 'did':
    # response form SUBJECT VERB ____
    # problem here is it's hard to change the verb to past tense or find matches
    start = ' '.join(q[2:-1]) + ' ' + q[-1] + ' '
    pages = search(' '.join(q[2:])) 
    i = 2
    # search restructured question for matches, trimming if necessary
    while i < len(q) and matches == []:
      phrases.append(' '.join(q[i:-1]) + r'\s(' + q[-1] + ').+')
      phrases.append(r'('+q[-1]+r').+')
      matches = find_phrases(phrases,pages)
      i += 1
    # search for dates in the matches
    dates = find_dates(matches)
    
  # choose the best answer from whatever we have at this point using tiling
  if dates != []:
    matches[0] = start + choose_best(dates)
  elif matches != []:
    matches[0] = choose_best(matches)
  
  # print answer for user
  print_answer(matches)  

# this function answers 'where' questions
def ask_where(q):
  write_log('User asked a \'where\' question.')
  matches = []
  phrases = []
  start = ''
  # where is/was questions 
  if q[1].lower() == 'is' or q[1].lower() == 'was':
    # start of response: ___ is/was in/located/at/near ___
    start = ' '.join(q[2:]) + ' ' + q[1] + ' '
    # search wikipedia using words after 'where is/was'
    # I found that using the sumamry words best here because otherwise there
    # are a lot of noise matches
    pages = search(' '.join(q[2:]),summary=True)
    i = 2
    # rephrase to re search for matches, trim if no matches found
    # '___ is/was in/located/at/near ___'
    while i < len(q) and matches == []:
      phrases.append( '(' + ' '.join(q[i:]) + r'|it)\s.+\s(is|was)\s.+\s(in|located|at|near)\s.+') 
      matches = find_phrases(phrases,pages)
      i += 1
    # trim the matches found to only contain the end of the match from above
    # add start to the front
    for m in range(0,len(matches)):
      write_log('Trimming answer ' + matches[m])
      matches[m] = start + re.search(r'\s(in|located|at|near)\s.+',matches[m]).group(0)
      write_log('New answer: ' + matches[m])
  # if matches found, choose best one
  if matches != []:
    matches[0] = choose_best(matches)
  print_answer(matches)    

# this functions answers 'what' questions
# it's simple but is able to cover most what is/was questions
def ask_what(q):
  write_log('User asked a \'what\' question.')
  p = 'NULL'
  matches = []
  phrases = []
  # what is/was
  if q[1].lower() == 'is' or q[1].lower() == 'was':
    # search wikipedia using text after 'what is/was'
    pages = search(' '.join(q[2:]))
    # construct regular expression to search for
    # ___ is/was ___
    p = '(' + ' '.join(q[2:]) + r' (is|was)\s' + ').+' 
    matches = find_phrase(p,pages)

  # if matches found, choose best
  if len(matches) > 1:
    matches[0] = choose_best(matches)
  print_answer(matches)

# this function answers who questions
def ask_who(q):
  write_log('User asked a \'who\' question.')
  matches = []
  phrases = []
  # who is/was
  if q[1].lower() == 'is' or q[1].lower() == 'was':
    # search for page
    pages = search(' '.join(q[2:]),summary=True)
    i = 2
    # search for matches and trim name until end
    while i < len(q):
      # search for ___ is/was ___
      phrases.append(' '.join(q[i:]) + '.+\s(is|was)\s.+') 
      match = find_phrases(phrases,pages)
      for m in match:
        matches.append(m)
      i += 1
  # if it's not an is/was question, assume we're looking for a name
  else:
    pages = search(' '.join(q[2:]))
    i = 2
    while i < len(q):
      # search for an answer with the form '___ ___ ___ VERB(or whatever second
      # word was) ___'
      phrases.append(r'\S+\s\S+\s(\S+)?\s'+ q[1] + r'\s' + ' '.join(q[i:]))
      match = find_phrases(phrases,pages)
      for m in match:
	matches.append(m)
      i += 1      
  # choose the best match
  if len(matches) > 1:    
    matches[0] = choose_best(matches)
  print_answer(matches)    

# this function prints the answer found
def print_answer(matches):
  # if there were no answers, then tell the user
  if matches == []:
    write_log('No answer found.')
    print 'I\'m sorry, I don\'t know the answer to that.'
  # otherwise, assume beginning of list is best answer
  else: 
    write_log('Answering question with:\n' + matches[0])
    print matches[0]  

# this function distinguishes what type of question it is and
# forwards the question to the proper function
def question(question):
  question = re.sub(r'[\.\?\!,]','',question)
  q = question.split()
  if q[0].lower() == 'when':
    ask_when(q)
  elif q[0].lower() == 'where':
    ask_where(q)
  elif q[0].lower() == 'what':
    ask_what(q)
  elif q[0].lower() == 'who':
    ask_who(q)
  elif q[0].lower() == 'exit' and len(q) == 1:
    write_log('Exiting program.')
  else:
    err = 'Error, question not found.'
    print err
    write_log(err)

# this function takes in input until the user says 'exit'
def answer_questions(f):
  q = ''
  while q.lower() != 'exit':
    q = raw_input('Ask a question or type \'exit\'\n')
    write_log(q)
    question(q)

# this function writes a message to the log
def write_log(m):
  global f
  f.write(m)
  f.write('\n')

def main():
  log = sys.argv[1] # load the log name
  global f
  f = open(log,'w+') # open log file to write
  answer_questions(f) # start answering questions
  f.close()

if __name__ == "__main__":
  main()
