from django.db.models import Q
from django.shortcuts import render, redirect
from questionnaire.models import Question, Answer, Questionnaire, Block, UserAnswer
from questionnaire.services.answer_abstract_factory import AnswerAbstractFactory


def start_questions(request, questionnaire_id):
    first_block = Block.objects.filter(questionnaire=questionnaire_id, is_first_block=True).first()
    return redirect('questionnaire:survey_question', block_id=first_block.uuid)


def survey_question(request, block_id):
    current_block = Block.objects.get(uuid=block_id)

    if current_block.type == Block.Type.SIMPLE:
        if request.method == 'POST':
            factory = AnswerAbstractFactory(current_block=current_block, data=request.POST, user=request.user,
                                            block_type=current_block.type)
            factory.process()
            next_block = factory.get_next_block()
            if next_block:
                return redirect('questionnaire:survey_question', block_id=next_block.uuid)
            else:
                return redirect('questionnaire:final_page', block_id=current_block.uuid)
        else:
            user_answers = UserAnswer.objects.filter(question__block=current_block)
            user_answers_dict = {answer.question.uuid: answer.user_answer for answer in user_answers}
            return render(request, 'questionnaire/question_multiple_answers.html',
                          {'unit': current_block, 'user_answers': user_answers_dict})
    else:
        if request.method == 'POST':
            selected_answers = request.POST.getlist('answer')
            factory = AnswerAbstractFactory(data=selected_answers, user=request.user, current_block=current_block,
                                            block_type=current_block.type)
            factory.process()
            next_block = factory.get_next_block()
            if next_block:
                return redirect('questionnaire:survey_question', block_id=next_block.uuid)
            else:
                return redirect('questionnaire:final_page', block_id=current_block.uuid)
        else:
            user_answers = UserAnswer.objects.filter(answer__current_block=current_block)
            user_answers_dict = {answer.answer.uuid: answer.user_answer for answer in user_answers}
            return render(request, 'questionnaire/question_single_answer.html',
                          {'unit': current_block, 'user_answers': user_answers_dict})


def list_questions(request):
    questionnaires = Questionnaire.objects.all()
    return render(request, 'questionnaire/questionnaire_list.html', {'questionnaires': questionnaires})


def final_page(request, block_id):
    current_block = Block.objects.filter(uuid=block_id).first()
    user_answers = UserAnswer.objects.filter(
        Q(question__block__questionnaire=current_block.questionnaire) | Q(
            answer__current_block__questionnaire=current_block.questionnaire))
    return render(request, 'questionnaire/final_page.html', {'user_answers': user_answers})
