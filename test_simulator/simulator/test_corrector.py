from tests.models import Question, Test
from json import dumps

class TestCorrector:
    def __init__(self, user_answer_sheet, system_answer_sheet):
        self.user_answer_sheet = user_answer_sheet
        self.system_answer_sheet = system_answer_sheet
        self.corrected_questions = []
    
    def init_correction(self):
        print("CORRIGINDO ESSA BAGAÇA")
        user_questions = self.user_answer_sheet.get_questions()

        for user_question in user_questions:
            self.__correct_current_question(user_question)
        
        correct_answer_sheet = AnswerSheetFactory.\
            get_corrected_answer_sheet(self.user_answer_sheet.get_test_id(), self.corrected_questions)

        return correct_answer_sheet

    def __correct_current_question(self, user_question):
        system_question = self.system_answer_sheet.get_question(user_question.question_id)
        self.__compare_both_questions(user_question, system_question)


    def __compare_both_questions(self, user_question, system_question):
        user_answers = user_question.get_answers()
        system_answers = system_question.get_answers()
        corrected_answers = []

        for answer_user in user_answers:
            for i, system_answer in enumerate(system_answers):
                if answer_user['option_id'] == system_answer['option_id']:
                    answer_user['is_correct'] = True
                    system_answers.pop(i)


class AnswerSheetFactory():
    def get_user_answer_sheet(dict, user):
        questions = []
        for question_json in dict['questions']:
            question_answered = QuestionAnswered(question_json['question_id'], question_json['answers'])
            questions.append(question_answered)

        user_answer_sheet = UserAnswerSheet(dict['test_id'], questions, user)
        return user_answer_sheet

    def get_system_answer_sheet(test_id, questions_list):
        questions = []
        result = Question.objects.filter(id__in = questions_list)
        
        for question in result:
            correct_answers = []
            for option in question.get_correct_options():
                correct_answers.append({'option_id':option.id, 'is_correct': option.is_correct})
            system_answer_sheet.add_question(question.id, correct_answers)

            system_question = QuestionAnswered(question.id, correct_answers)
            questions.append(system_question)

        system_answer_sheet = SystemAnswerSheet(test_id, questions)
        return system_answer_sheet

    def get_corrected_answer_sheet(test_id, questions):
        corrected_answer_sheet = CorrectedAnswerSheet(test_id, questions)
        return corrected_answer_sheet


class AnswerSheet:
    def __init__(self, test_id, questions):
        self.test_id = test_id
        self.questions = questions

    def get_questions_list(self):
        list = []
        for question in self.questions:
            list.append(question.get_question_id())
        return list
    
    def get_questions(self):
        return self.questions

    def get_question(self, question_id):
        for question in self.questions:
            if(question.question_id == question_id):
                return question
        return None

    def get_test_id(self):
        return self.test_id


class UserAnswerSheet(AnswerSheet):
    def __init__(self, test_id, questions):
        #self.user = user
        AnswerSheet.__init__(self, test_id, questions)


class SystemAnswerSheet(AnswerSheet):
    def __init__(self, test_id, questions):
        AnswerSheet.__init__(self, test_id, questions)


class CorrectedAnswerSheet(AnswerSheet):
    def __init__(self, test_id, questions, user):
        self.user = user
        self.corrects = 0
        self.incorrects = 0
        AnswerSheet.__init__(self, test_id, questions)

    def __set_corrected_to_true(self):
        self.corrected = True
        for question in self.questions:
            if(question.is_correct):
                self.corrects += 1
        
        self.incorrects = len(self.questions) - self.corrects

    def get_corrects(self):
        return self.corrects

    def get_incorrects(self):
        return self.incorrects

    def __init__(self, question_id, answers):
        self.question_id = question_id
        self.answers = answers
        self.is_correct = False

    def get_question_id(self):
        return self.question_id

    def set_is_correct_to_true(self):
        self.is_correct = True

    def get_is_correct(self):
        return self.is_correct

    def get_answers(self):
        return self.answers

    def __str__(self) -> str:
        return "Id - {} | {} | Answers - {}".format(self.question_id, self.is_correct, self.answers)


class QuestionAnswered:
    def __init__(self, question_id, answers):
        self.question_id = question_id
        self.answers = answers
        self.is_correct = False

    def get_question_id(self):
        return self.question_id

    def set_is_correct_to_true(self):
        self.is_correct = True

    def get_is_correct(self):
        return self.is_correct

    def get_answers(self):
        return self.answers

    def __str__(self) -> str:
        return "Id - {} | {} | Answers - {}".format(self.question_id, self.is_correct, self.answers)

class AnswerSheetUser:
    def __str__(self) -> str:
        return "{} | {} | {}".format(self.user, self.test_id, self.corrected)

    def __init__(self, json, user):
        self.test_id = json['test_id']
        self.user = user
        self.corrected = False
        self.questions = []
        self.corrects = 0
        self.incorrects = 0

        print("Dentro - ", len(self.questions))
        for question_json in json['questions']:
            question_answered = QuestionAnswered(question_json['question_id'], question_json['answers'])
            self.questions.append(question_answered)

    def get_questions_list(self):
        list = []
        for question in self.questions:
            list.append(question.get_question_id())
        return list
    
    def get_questions(self):
        return self.questions

    def set_corrected_to_true(self):
        self.corrected = True
        for question in self.questions:
            if(question.is_correct):
                self.corrects += 1
        
        self.incorrects = len(self.questions) - self.corrects

    def get_corrected(self):
        return self.corrected

    def get_corrects(self):
        return self.corrects

    def get_incorrects(self):
        return self.incorrects

    def serialize_to_json(self):
        obj_dict = {}
        obj_dict['test_id'] = self.test_id
        obj_dict['corrected'] = self.corrected
        obj_dict['corrects'] = self.corrects
        obj_dict['incorrects'] = self.incorrects
        obj_dict['questions'] = []

        for question in self.questions:
            obj_dict['questions'].append({
                'question_id':question.get_question_id(),
                'is_correct': question.get_is_correct(),
                'answers': question.get_answers()
            })
        return dumps(obj_dict)


class AnswerSheetTest:

    def __init__(self):
        test_id = None
        self.questions = {}

    def add_question(self, question_id, answers):
        self.questions[question_id] = answers

    def get_question(self, question_id):
        #Talvez colocar uma exceção se for None?
        target_question = self.questions[question_id]
        return target_question

    def get_questions(self):
        return self.questions


class GeneratorAnswerSheetTest:

    def __init__(self, questions_list, ) -> None:
        self.questions_list = []
        self.questions_list = questions_list

    def generate(self):
        result = Question.objects.filter(id__in = self.questions_list)
        new_answer_sheet = AnswerSheetTest()
        for question in result:
            correct_answers = []
            for option in question.get_correct_options():
                correct_answers.append({'option_id':option.id, 'is_correct': option.is_correct})
            new_answer_sheet.add_question(question.id, correct_answers)

        return new_answer_sheet

"""
    def __compare_both_questions(self, user_question, test_question):
        left = True
        for answer_user in user_question.get_answers():
            left = True

            for i, answer_test in enumerate(test_question):
                left = False
                if answer_user['option_id'] == answer_test['option_id']:
                    answer_user['is_correct'] = True
                    test_question.pop(i)

            if(left):
                answer_user['is_correct'] = False


        
        if len(test_question) == 0 and left == False:
            user_question.set_is_correct_to_true()

        user_question.answers += test_question

        print(test_question)
"""