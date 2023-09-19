import sqlite3


class DataBase:
    DB = sqlite3.connect('bot_helper.dp')
    CUR = DB.cursor()

    def create_tables(self):
        self.CUR.execute("CREATE TABLE IF NOT EXISTS categorys("
                         "id INTEGER PRIMARY KEY AUTOINCREMENT, category TEXT);"
                         )

        self.CUR.execute("""CREATE TABLE IF NOT EXISTS questions(
                         id INTEGER PRIMARY KEY AUTOINCREMENT,
                         user_id INTEGER, question TEXT,
                         category_id INTEGER,
                         FOREIGN KEY(category_id) REFERENCES categorys(id) ON DELETE CASCADE);"""
                         )

        self.CUR.execute("""CREATE TABLE IF NOT EXISTS answer_questions(
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            user_id INTEGER,
                            user_username TEXT,
                            user_id_questions INTEGER,
                            answer TEXT,
                            id_question INTEGER,
                            FOREIGN KEY (id_question) REFERENCES questions(id) ON DELETE CASCADE);"""
                         )
        self.DB.commit()

    def insert_category(self):
        categorys = ['Python', 'Java', 'c++']
        for i in categorys:
            self.CUR.execute("INSERT INTO categorys (category) VALUES (?)", (i,))
        self.DB.commit()

    async def check_category(self, text: str) -> bool:
        flag = (text,) in self.CUR.execute("SELECT category FROM categorys")
        self.DB.commit()
        return flag

    async def get_id_category(self, text: str) -> int:
        sqlite_select_query = "SELECT id FROM categorys WHERE category=?;"
        category_id = self.CUR.execute(sqlite_select_query, (text,)).fetchone()[0]
        return category_id

    async def save_questions(self, user_id: int, question: str, category_id: int) -> None:
        self.CUR.execute("INSERT INTO questions (user_id, question, category_id) VALUES (?, ?, ?)", (user_id, question, category_id))
        self.DB.commit()

    def get_all_categorys(self):
        all_categorys = self.CUR.execute("SELECT category FROM categorys").fetchall()
        self.DB.commit()
        return all_categorys

    def check_have_user_questions(self, id: int):
        flag = self.CUR.execute("SELECT user_id FROM questions WHERE user_id=?", (id,)).fetchall()
        self.DB.commit()
        if flag:
            return True
        return False

    async def get_questions_user(self, user_id: int):
        questions = self.CUR.execute("SELECT id, question FROM questions WHERE user_id=?", (user_id,)).fetchall()
        self.DB.commit()
        return questions

    async def get_questions_id_user(self, user_id: int):
        questions = self.CUR.execute("SELECT id FROM questions WHERE user_id=?", (user_id,)).fetchall()
        self.DB.commit()
        return [str(i[0]) for i in questions]

    def get_answer_for_questions(self, id_questions: str):
        answer = self.CUR.execute("SELECT id, user_username, answer FROM answer_questions WHERE id_question=?", (int(id_questions),)).fetchall()
        self.DB.commit()
        return answer

    async def delite_question(self, id_question: str) -> None:
        self.CUR.execute("DELETE FROM questions where id = ?", (id_question,))
        self.DB.commit()

    async def get_answer(self, id_answer: str):
        answer = self.CUR.execute("SELECT user_username, answer FROM answer_questions WHERE id=?", (int(id_answer),)).fetchall()
        self.DB.commit()
        return answer[0]

    async def get_questions_for_id_category(self, id_category, user_id):
        # questions = self.CUR.execute("SELECT id, question FROM questions WHERE category_id=? and user_id !=?", (int(id_category), int(user_id))).fetchall()
        questions = self.CUR.execute("SELECT id, question FROM questions WHERE category_id=?", (int(id_category),)).fetchall()

        self.DB.commit()
        return [i for i in questions]

    async def get_user_id_question(self, id_question):
        user_id_question = self.CUR.execute("SELECT user_id FROM questions WHERE id=?",(int(id_question),)).fetchone()
        self.DB.commit()
        return int(user_id_question[0])

    async def save_answer(self, user_id, username, user_id_questions, answer, id_question):
        if username is None:
            username = 'пользователь не определён'
        self.CUR.execute("INSERT INTO answer_questions (user_id, user_username, user_id_questions, answer, id_question) VALUES (?, ?, ?, ?, ?)", (user_id, username, user_id_questions, answer, id_question))
        self.DB.commit()


if __name__ == '__main__':
    a = DataBase()
    print(a.save_answer(5435345, 'inc', 543566543, 'gtr5gyh5tghergrte', 17))
    # a.create_tables()
    # a.insert_category()
