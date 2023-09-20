from json import load, dump
from ..models import Test, Question, Option

class LoadQuestions:
    test_id = None

    def __init__(self, test_id):
        self.test_id = test_id
    
    def load_questions(self):
        print('Loading questions for test_id: ')
        tests = Test.objects.filter(id=self.test_id)
        
        questions_list = self.read_json()
        for question_dict in questions_list:
            print('Carregando - ' + question_dict['question'])
            question = Question(test=tests[0], question_text=question_dict['question'])
            question.save()
            for option_dict in question_dict['options']:
                print('Carregando - ' + option_dict['text'])
                option = Option(question=question, option_text=option_dict['text'], is_correct=option_dict['correct'])
                option.save()

    def read_json(self):
        with open('tests/processes/questions.json') as json_file:
            file = load(json_file)
            return file