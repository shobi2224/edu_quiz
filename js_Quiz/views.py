from django.shortcuts import render
from .models import *

# def Quizpage(request):
#     return render(request, 'Quizpage.html')

from django.shortcuts import render
from .models import Topic, Question

def quiz_view(request, topic_name):
    topic = Topic.objects.get(name=topic_name)
    questions = Question.objects.filter(topic=topic)

    if request.method == 'POST':
        score = 0
        for question in questions:
            selected_answer = request.POST.get(f"q{question.id}")
            if selected_answer == question.correct_answer:
                score += 1
        
        # Message based on the score
        if score == len(questions):
            message = "Excellent! You've nailed every question! 🎉"
        elif score >= len(questions) // 2:
            message = "Good job! But there's room for improvement 👏"
        else:
            message = "Don't worry, keep practicing, you'll do better next time 👍"

        # Render the results page with score and message
        selected_topic = request.session.get('selected_topic', None)
        return render(request, 'quiz/quiz_results.html', {'score': score, 'total': len(questions), 'message': message, 'selected_topic': selected_topic})

    return render(request, 'quiz/quiz.html', {'topic': topic, 'questions': questions})