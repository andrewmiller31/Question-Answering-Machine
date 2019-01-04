# Question Answering Machine (QAM)
A program that mines information from Wikipedia pages to answer questions. NLP techniques used include query-
reformulation, n-gram mining, filtering, and tiling. More information and detailed comments available in the code.

To run:

python qa.py \<log file name\>

This log file tracks in detail how the answers are reached.

## Notable Correct Answers
Here is a collection of correct answers given by QAM that I thought did a good job showcases the program's strengths.

Q1) When was John F. Kennedy assassinated? 

QAM) John F Kennedy was assassinated November 22, 1963 
 
Q2) When was The Boston Massacre? 

QAM) The Boston Massacre was March 5, 1770 
 
Q3) When is Thanksgiving? 

QAM) Thanksgiving is the second Monday of October in Canada and on the fourth Thursday of November in the United States, 
     and around the same part of the year in other places. 
 
Q4) What is a pencil?

QAM) A pencil is an implement for writing or drawing constructed of a narrow, solid pigment core inside a protective casing which 
     prevents the core from being broken and/or from leaving marks on the users hand during use. 
 
Q5) Who was Abraham Lincoln? 

QAM) Abraham Lincoln was an American lawyer and politician who served as the 16th President of the United States from 1861 until 
     his assassination in April 1865. 
 
Q6) Who was Martin Luther King? 

QAM) Martin Luther King Jr. was an American Baptist minister and activist who became the most visible spokesperson and leader 
     in the civil rights movement from 1954 until his death in 1968. 
 
Q7) What is Zimbabwe? 

QAM) Zimbabwe is a landlocked country in southern Africa, lying between latitudes 15 and 23S, and longitudes 25 and 34E. 
 
Q8) Where is The Liberty Bell? 

QAM) The Liberty Bell is located in the Liberty Bell Center in Independence National Historical Park. 
 
Q9) Where is Kilimanjaro?

QAM) Kilimanjaro is in Tanzania. 
 
Q10) Who shot John Lennon? 

QAM) Mark David Chapman shot Lennon.

## Notable Blunders
Here is a collection of answers that I thought show where QAM fell short. Some of them can be very amusing. 
One thing to notice is that there are attempts withing the program to detect when a suitable answer can not be found, in such a case,
the response is "I'm sorry, I don't know the answer to that."

Q1) When was Ben Franklin born? 
QAM) Ben Franklin born was August 15, 1667 
 
Q2) Who was John Lennon? 
QAM) Lennon began to record as a solo artist before the band's break-up in April 1970; two of those songs were "Give Peace a Chance" 
and "Instant Karma!" Lennon subsequently produced albums that included John Lennon/Plastic Ono Band and Imagine, and songs such as 
"Working Class Hero", "Imagine" and "Happy Xmas (War Is Over)". 
 
Q3) Where is Mars? 
QAM) Mars is at the lowest elevations for short periods. 
 
Q4) What is a dog? 
QAM) I'm sorry, I don't know the answer to that. 
 
Q5) When is the next Avengers movie coming out? 
QAM) the next Avengers movie coming out is December 20 
 
Q6) Who won Super Bowl LII? 
QAM) I'm sorry, I don't know the answer to that. 
 
Q7) What is the Sun? 
QAM) the Sun is a near-perfect sphere with an oblateness estimated at about 9 millionths, which means that its polar diameter differs from its equatorial diameter by only 10 kilometres (6.2 mi). 
 
Q8) When is the next Super Bowl? 
QAM) the next Super Bowl is February 7, 2016 
 
Q9) Who was the director of Lord of the Rings? 
QAM) Lord of the Rings in its turn is considered to have had a great effect on modern fantasy; the impact of Tolkien's works is such that the use of the words "Tolkienian" and "Tolkienesque" have been recorded in the Oxford English Dictionary.The enduring popularity of The Lord of the Rings has led to numerous references in popular culture, the founding of many societies by fans of Tolkien's works, and the publication of many books about Tolkien and his works. 
 
Q10) Where is the Red Sea? 
QAM) the Red Sea is at its widest point, 355 km wide. 
