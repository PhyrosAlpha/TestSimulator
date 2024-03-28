from django.test import TestCase
from simulator.test_corrector import AnswerSheetFactory, SystemAnswerSheet, QuestionAnswered, TestCorrector

#Testando test_corrector
class TestTestCorrector(TestCase):

    def setUp(self):
        print('carregando')

        user_answer_sheet = AnswerSheetFactory\
                                .get_user_answer_sheet(user_answer_sheet_dict, None)

        system_answer_sheet = createSystemSheetToTest()
        self.corrected_answer_sheet = TestCorrector(user_answer_sheet, system_answer_sheet).init_correction()


    def test_corrector(self):
        pass

    def test_correct_questions(self):
        pass

    def test_correct_user_question_without_options(self):
        questions = self.corrected_answer_sheet.get_questions()
        question_1 = questions[0]
        question_2 = questions[1]

        self.assertEqual(False, question_1.get_is_correct(), "Se a questão 1 está vazia")
        self.assertEqual(False, question_2.get_is_correct(), "Se a questão 2 está vazia")

    def test_correct_question(self):
        questions = self.corrected_answer_sheet.get_questions()
        question_3 = questions[2]
        question_4 = questions[3]

        self.assertEqual(True, question_3.get_is_correct(), "Se a questão 3 está correta")
        self.assertEqual(True, question_4.get_is_correct(), "Se a questão 4 está correta")
"""
    def test_correct_more_user(self):
        pass

    def test_correct_less_user(self):
        pass
"""

def createSystemSheetToTest():
    questions = []

    questions.append(QuestionAnswered(1, create_correct_options(11,12)))
    questions.append(QuestionAnswered(2, create_correct_options(21,22)))
    questions.append(QuestionAnswered(3, create_correct_options(31,32)))
    questions.append(QuestionAnswered(4, create_correct_options(41)))
    questions.append(QuestionAnswered(5, create_correct_options(11,12)))
    questions.append(QuestionAnswered(6, create_correct_options(11,12)))
    questions.append(QuestionAnswered(7, create_correct_options(11,12)))
    questions.append(QuestionAnswered(8, create_correct_options(11,12)))
    questions.append(QuestionAnswered(9, create_correct_options(11,12)))
    questions.append(QuestionAnswered(10, create_correct_options(11,12)))
    return SystemAnswerSheet(1, questions)

def create_correct_options(*arg):
    options = []
    for id in arg:
        #print(id)
        options.append({'option_id':id, 'is_correct': True}.copy())

    print('GERAÇÃOOOOOOOOOOOOOOOOOO')
    print(options)
    return options

user_answer_sheet_dict = {
    "test_id": 1,
    "questions": [
        {
            "question_id": 1,
            "answers": [

            ]
        },
        {
            "question_id": 2,
            "answers": [

            ]
        },
        {
            "question_id": 3,
            "answers": [
                {
                    "option_id": 31,
                },
                {
                    "option_id": 32,
                }
            ]
        },
        {
            "question_id": 4,
            "answers": [
                {
                    "option_id": 41
                }
            ]
        },
        {
            "question_id": 5,
            "answers": [
                {
                    "option_id": 531,
                }
            ]
        },
        {
            "question_id": 6,
            "answers": [
                {
                    "option_id": 513,
                }
            ]
        },
        {
            "question_id": 7,
            "answers": [
                {
                    "option_id": 662,
                },
                {
                    "option_id": 664,
                },
                {
                    "option_id": 663,
                }
            ]
        },
        {
            "question_id": 8,
            "answers": [
                {
                    "option_id": 300,
                }
            ]
        },
        {
            "question_id": 9,
            "answers": [
                {
                    "option_id": 263,
                },
                {
                    "option_id": 262,
                }
            ]
        },
        {
            "question_id": 10,
            "answers": [
                {
                    "option_id": 760,
                }
            ]
        }
    ],
}


