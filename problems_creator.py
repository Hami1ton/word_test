import random

from flask import session, g


class ProblemsCreator:
    def __init__(self, number_of_questions: int):
        self.number_of_questions = number_of_questions
        # DBヘアクセスし、[英単語, その意味]を要素とするリストを作成する。
        # TODO アプリ起動時にこのリストを保持しておいて、問題作成を毎回呼び出すようにすれば軽い処理になるのでは？
        cur = g.db.execute('select word, meaning from english_words_and_meanings order by id desc')
        self.words_and_meanings = [[row[0], row[1]] for row in cur.fetchall()]

    def create_question_list(self):
        # [英単語, その意味]を要素とするリストから問題を作成する。
        meaning_random_list = [word_and_meaning[1] for word_and_meaning in self.words_and_meanings]
        problem_number_list = random.sample([i for i in range(len(self.words_and_meanings))], self.number_of_questions)
        session["problem_words_and_meanings_list"] = [self.words_and_meanings[i] for i in problem_number_list]
        result_list = list()
        for word_and_meaning in session["problem_words_and_meanings_list"]:
            choice_list = list()
            word = word_and_meaning[0]
            meaning = word_and_meaning[1]
            choice_list.append(meaning)
            # 残り二つの選択肢を用意する
            while len(choice_list) < 3:
                meaning_choosed = random.choice(meaning_random_list)
                if not meaning_choosed in choice_list:
                    choice_list.append(meaning_choosed)

            result_list.append([word, choice_list])
        return result_list
