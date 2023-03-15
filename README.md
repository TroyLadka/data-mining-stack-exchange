# data-mining-stack-exchange

ASSIGNMENT PROMPT:

In this project, you shall collect data from select StackExchange Q&A sites. Your team will be able to select a site for the project.

Write a program that shall: 
a) Download 1,000 most recent (“newest”) questions. 
b) For each question on each index page, use BeautifulSoup to extract the following: 
     1. The title (str) and the ID (str) of the question. 
     2. The name (str), the ID (str), and the reputation score (int) of the original poster. 
     3. The time the question was posted (str). 
     4. The question score (int), the number of views (int), the number of answers (int), and whether an answer was accepted (bool). 
     5. The question tags (str). A question may have at most five tags. 
     6. Whether the question is closed (bool). 
c) For each question on its own page, use BeautifulSoup to extract the following: 
     1. Whether the question has been edited since posting (bool). 
     2. The number of comments (int). 
     3. The score of the answer (int); the name (str), the ID (str), and the reputation score (int) of the poster; the number of comments (int) for                 each answer, and whether the answer was accepted (bool). 
d) Using the standard CSV writer, save the collected data as two CSV files: 
     1. The first file XXX-questions.csv contains the questions, one question per row. The column names are: Question_Title, Question_ID, Author_Name, Author_ID, Author_Rep, Question_Post_Time, Question_Score, Number_Of_Views, Number_Of_Answers, Number_Of_Comments, Edited, Answer_Accepted, Tag_1, Tag_2, ..., Tag_5 (use empty strings to represent non-specified tags), Question_Closed. 2. The second file XXX-answers.csv contains the answers, one answer per row. The column names are: Question_ID, Answer_Score, Author_Name, Author_ID, Author_Rep, Number_Of_Comments, Answer_Accepted.

Please be considerate of other users: 
1. Run the entire script only when you are sure it 100% works. 
2. Test the script first on a single page. 
3. Introduce a 1-sec delay between any consecutive downloads. 
4. Be prepared that your files may be large.

Deliverable: The python script and two CSV files. Modules to use: csv, bs4, urllib/requests. Modules NOT to use (yet): pandas, numpy.
