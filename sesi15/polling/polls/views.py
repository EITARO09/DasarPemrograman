from django.shortcuts import render, get_object_or_404, redirect
from .models import Poll, Choice, Vote

def vote(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)

    if request.method == "POST":
        choice_id = request.POST.get("choice")
        choice = get_object_or_404(Choice, id=choice_id, poll=poll)
        Vote.objects.create(choice=choice)
        return redirect('results', poll_id=poll.id)

    return render(request, 'polls/vote.html', {'poll': poll})


def results(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    results_count = {choice.text: choice.votes.count() for choice in poll.choices.all()}
    return render(request, 'polls/results.html', {'poll': poll, 'results': results_count})
