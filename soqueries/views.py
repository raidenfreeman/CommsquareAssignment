from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
import requests
import time
import datetime
from datetime import date, timedelta

StackOverflowQuestionsAPIUrl = 'https://api.stackexchange.com/2.2/questions'


def data(req):
    two_days_ago_timestamp = int(time.mktime((date.today() - timedelta(2)).timetuple()))
    now_timestamp = int(time.mktime(datetime.datetime.now().timetuple()))

    params_dictionary = {'tagged': 'python',
                         'site': 'stackoverflow',
                         'order': 'desc',
                         'sort': 'activity',
                         'fromdate': two_days_ago_timestamp,
                         'todate': now_timestamp}
    query_response = requests.get(StackOverflowQuestionsAPIUrl, params=params_dictionary).json()
    questions = query_response['items']
    number_of_questions = len(questions)
    number_of_answered_questions = len([x for x in questions if x['is_answered']])
    number_of_answers = sum([x['answer_count'] for x in questions])
    number_of_views = sum([x['view_count'] for x in questions])
    average_number_of_answers = number_of_answers / number_of_questions
    average_number_of_views = number_of_views / number_of_questions

    data_to_display = [{'display_name': x['owner']['display_name'],
                        'title': x['title'],
                        # Send timestamp to the webpage, and convert it there based on the browser's locale
                        'creation_date': x['creation_date'],
                        'is_answered': x['is_answered'],
                        'view_count': x['view_count'],
                        'score': x['score'],
                        'link': x['link']} for x in questions]
    statistics = {'totalQuestions': number_of_questions,
                  'totalAnsweredQuestions': number_of_answered_questions,
                  'avgAnswers': average_number_of_answers,
                  'avgViews': average_number_of_views}
    response = {'questionsArray': data_to_display, 'stats': statistics}
    return JsonResponse(response)


def index(req):
    return render(req, 'soqueries/index.html', )
