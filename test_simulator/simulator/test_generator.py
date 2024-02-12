from tests.models import Test, Question
from json import dumps


class TestGenerator:

    def __init__(self, testId, numberQuestions):
        self.testId = testId
        self.numberQuestions = numberQuestions

    def generateTest(self):
        test = Test.objects.get(id=self.testId)
        questions = Question.objects.filter(test=test).order_by('?')[:self.numberQuestions]
        data = self.convertToJson(questions, test)
        
        return data

    def convertToJson(self, questions, test):
        dict_data = {'test_id': test.id, 
                    'name': test.name,
                    'questions': []
                    }

        for question in questions:
            dict_question = {'id': question.id,
                            'question_text': question.question_text,
                            'options': []
                            }
            options = question.getOptions()
            for option in options:
                dict_option = {'id': option.id,
                            'option_text': option.option_text,
                            }
                dict_question['options'].append(dict_option)
            dict_data['questions'].append(dict_question)
    
        data = dumps(dict_data)
        return data