from bs4 import BeautifulSoup
import requests
import sys
import csv
import time

section_one_data = [['Question_Title', 'Question_ID', 'Author_Name', 'Author_ID', 'Author_Rep', 'Question_Post_Time', 'Question_Score', 'Number_Of_Views', 'Number_Of_Answers', 'Number_Of_Comments', 'Edited,', 'Answer_Accepted,', 'Tags', 'Question_Closed']]

titles = []
ids = []
user_names = []
user_ids = []
user_reps = []
post_times = []
votes = []
answers = []
views = []
answer_acceptions = []
tags = []
closed = []

page_counter = 1

while len(titles) <= 985:
    object = requests.get(f"https://softwareengineering.stackexchange.com/questions?tab=newest&page={page_counter}")

    if object.status_code != 200:
        sys.exit()

    html = object.text
    soup = BeautifulSoup(html, "lxml")
    divs = soup.findAll('div', class_='s-post-summary')

    for item in divs:
        # TITLE OF QUESTION
        try:
            title = item.findAll('a', class_='s-link')[0].text
        except (AttributeError, IndexError):
            title = "Invalid Title"
        titles.append(title)

        # ID OF QUESTION
        try:
            id = item.get('data-post-id')
        except (AttributeError, IndexError):
            id = "Invalid ID"
        ids.append(id)

        # NAME OF POSTER
        try:
            user_name_container = item.findAll('div', class_='s-user-card--link d-flex gs4')[0]
            user_name = user_name_container.contents[1].text
        except (AttributeError, IndexError):
            user_name = "Invalid Name"
        user_names.append(user_name)

        # ID OF POSTER
        try:
            user_id = item.findAll('a', class_='s-avatar')[0]['data-user-id']
        except (AttributeError, IndexError):
            user_id = "Invalid ID"
        user_ids.append(user_id)
    

        # REPUTAION OF POSTER
        try:
            user_rep_str = item.findAll('span', class_='todo-no-class-here')[0].text
            user_rep_list = user_rep_str.split()
            for i in range(len(user_rep_list)):
                if 'k' in user_rep_list[i]:
                    user_rep_list[i] = int(float(user_rep_list[i].replace('k', '')) * 1000)
                elif ',' in user_rep_list[i]:
                    user_rep_list[i] = int(float(user_rep_list[i].replace(',', '')))
                else:
                    user_rep_list[i] = int(user_rep_list[i])
            user_rep = user_rep_list[0]
        except (AttributeError, IndexError):
            user_rep = "Invalid Rep"
        user_reps.append(user_rep)

        # TIME OF POST
        try:
            post_time = item.findAll('span', class_='relativetime')[0]['title'][:-1]
        except (AttributeError, IndexError):
            post_time = "Invalid Time"
        post_times.append(post_time)
        

        # SCORE OF POST
        try:
            vote = int(item.findAll('span', class_='s-post-summary--stats-item-number')[0].text)
        except (AttributeError, IndexError):
            vote = "Invalid Score"
        votes.append(vote)
        
        # ANSWER COUNT
        try:
            answer = int(item.findAll('span', class_='s-post-summary--stats-item-number')[1].text)
        except (AttributeError, IndexError):
            answer = "Invalid Answer Count"
        answers.append(answer)

        # VIEW COUNT
        try:
            view_string = item.findAll('span', class_='s-post-summary--stats-item-number')[2].text
            view_list = []
            for v in view_string.split():
                if v.isdigit():
                    view_list.append(int(v))
                elif 'k' in v:
                    view_list.append(int(float(v.replace('k', '')) * 1000))
            view = sum(view_list)
        except (AttributeError, IndexError):
            view = "Invalid View Count"
        views.append(view)

        # IS ANSWER ACCEPTED
        try:
            answer_acception = len(item.findAll('div', title='one of the answers was accepted as the correct answer')) > 0
        except (AttributeError, IndexError):
            answer_acception = "Invalid Data"
        answer_acceptions.append(answer_acception)

        # TAGS OF QUESTION
        try:
            tag_divs = []
            tag = []
            tag_divs.append(item.findAll('div', class_='tags')[0])
            for item in tag_divs:
                tag.append(item.findAll('a', class_='post-tag'))
            for i in range(len(tag)):
                for j in range(len(tag[i])):
                    tag[i][j] = tag[i][j].text
        except (AttributeError, IndexError):
            tag = ['No tags']
        tags.append(tag)
            

        # IS QUESTION CLOSED
        try:
            if '[closed]' in title:
                is_closed = True
            else:
                is_closed = False
        except (AttributeError, IndexError):
            is_closed = "Invalid Data"
        closed.append(is_closed)            
        
    page_counter += 1
    time.sleep(1)
    
###################################################
        
question_links = []
page_counter = 1

while (len(question_links)<1000):
    object = requests.get(f"https://softwareengineering.stackexchange.com/questions?tab=newest&page={page_counter}")

    if object.status_code != 200:
        sys.exit()
    
    html = object.text
    soup = BeautifulSoup(html, "lxml")
    divs = soup.findAll('div', class_='s-post-summary')
    
    for item in divs:
        question_links.append(item.findAll('a', class_='s-link')[0]['href'])
    
    time.sleep(1)

section_two_data = [['Question_ID', 'Answer_Score', 'Author_Name', 'Author_ID', 'Author_Rep', 'Number_Of_Comments', 'Answer_Accepted']]
is_edited = []
answer_votes = []
answer_name = []
answer_name_ids = []
answer_rep = []
comments = []
answer_comments= []


for i in range(1000):
    question_obj = requests.get('https://softwareengineering.stackexchange.com' + question_links[i])
    question_html = question_obj.text
    question_soup = BeautifulSoup(question_html, 'lxml')
    question_div = question_soup.findAll('div', class_='post-signature')
    
    # IS EDITED
    try:
        edited_list = [item.findAll('a', title='show all edits to this post') for item in question_div]
        edited = len(edited_list[0])>0
    except (AttributeError, IndexError):
        edited = 'Invalid Data'
    is_edited.append(edited)
    
    # NUMBER OF COMMENTS
    try:
        num_comments = question_soup.findAll('span', itemprop='commentCount')[0].text
    except (AttributeError, IndexError):
        num_comments = '0';
    comments.append(num_comments)
    
    # ANSWER SCORE
    try:
        answer_vote = int(question_soup.findAll('div', class_='js-vote-count')[1]['data-value'])
    except (AttributeError, IndexError):
        answer_vote = 0
    answer_votes.append(answer_vote)
    
    # ANSWER USER NAME
    try:
        answer_user_name_div = question_soup.findAll('div', itemprop='author')[1]
        answer_user_name = answer_user_name_div.findAll('span', itemprop='name')[0].text
    except (AttributeError, IndexError):
        answer_user_name = 'Invalid Name'
    answer_name.append(answer_user_name)
    
    # ANSWER USER ID
    if (answer_user_name != 'Invalid Name'):
        try:
            answer_user_id = answer_user_name_div.findAll('a')[0]['href'].split('/')[-2]
        except (AttributeError, IndexError, NameError):
            answer_user_id = 'Invalid ID'
    else:
        answer_user_id = 'Invalid ID'
    answer_name_ids.append(answer_user_id)
        
    
    # ANSWER REP SCORE
    try:
        answer_rep_score = question_soup.findAll('span', class_='reputation-score')[1].text
    except (AttributeError, IndexError):
        answer_rep_score = '0'
    answer_rep.append(answer_rep_score)
        
    # ANSWER COMMENT COUNT
    answer_stats_div = question_soup.find('div', class_='answer')
    try:
        answer_comment_count = answer_stats_div.find('span', itemprop='commentCount').text
        if (answer_comment_count == ''):
            answer_comment_count = 0
        else: answer_comment_count = int(answer_comment_count)
    except (AttributeError, IndexError):
        answer_comment_count = 0
    answer_comments.append(answer_comment_count)
        
    time.sleep(1)
    
new_answer_rep = []
for rep in answer_rep:
    answer_rep_list = rep.split()
    for i in range(len(answer_rep_list)):
        if 'k' in answer_rep_list[i]:
            answer_rep_list[i] = int(float(answer_rep_list[i].replace('k', '')) * 1000)
        elif ',' in answer_rep_list[i]:
            answer_rep_list[i] = int(float(answer_rep_list[i].replace(',', '')))
        else:
            answer_rep_list[i] = int(answer_rep_list[i])
    answer_rep_list[i] = int(answer_rep_list[i])
    new_answer_rep.append(answer_rep_list[i])
    
new_comments = []
for comment in comments:
    if comment == '':
        new_comments.append(0)
    else:
        new_comments.append(int(comment))

for i in range(1000):
    new_list = []
    new_list.append(titles[i])
    new_list.append(ids[i])
    new_list.append(user_names[i])
    new_list.append(user_ids[i])
    new_list.append(user_reps[i])
    new_list.append(post_times[i])
    new_list.append(votes[i])
    new_list.append(views[i])
    new_list.append(answers[i])
    new_list.append(new_comments[i])
    new_list.append(str(is_edited[i]))
    new_list.append(str(answer_acceptions[i]))
    new_list.append(tags[i][0])
    new_list.append(str(closed[i]))
    section_one_data.append(new_list)

        
for i in range(1000):
    new_list = []
    new_list.append(ids[i])
    new_list.append(answer_votes[i])
    new_list.append(answer_name[i])
    new_list.append(answer_name_ids[i])
    new_list.append(new_answer_rep[i])
    new_list.append(answer_comments[i])
    new_list.append(str(answer_acceptions[i]))
    section_two_data.append(new_list)
    
with open('softwareengineering-questions.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    for row in section_one_data:
        writer.writerow(row)
        
with open('softwareengineering-answers.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    for row in section_two_data:
        writer.writerow(row)
