import mysql.connector
import random

def startSimulation(conexion):
    # insert simulation id, start
    sql = "INSERT INTO simulations (startAt) VALUES (current_timestamp);"
    try:
        cursor = conexion.cursor()
        cursor.execute(sql)
        conexion.commit()
    except mysql.connector.Error as err:
        print("### - can not start simulator:", err)
        return

    # do while simulation question is less or equals to 50
    max_questions = 50
    for q in range(max_questions):
        # find question excluding current questions
        sql = """ SELECT id, question, (SELECT id FROM simulations ORDER BY id desc LIMIT 1) as simulation 
                    FROM questions WHERE id not in 
                        (SELECT idquestion FROM simulation WHERE idsimulation = (SELECT id FROM simulations ORDER BY id desc LIMIT 1))
                    ORDER BY used LIMIT 25;"""
        try:
            cursor = conexion.cursor()
            cursor.execute(sql)
            rows = cursor.fetchall()
            selectedRow = random.randint(0,len(rows)-1)
            row = rows[selectedRow]
            # insert into simulation
            idSimulation = row[2]
            idQuestion = row[0]
            # insert question in simulation
            # print('insertSimulationQuestion({}, {}, conexion)'.format(idSimulation, idQuestion)) 
            insertSimulationQuestion(idSimulation, idQuestion, conexion)
            print('\n{}. {}'.format(q+1, row[1]))
            sqlOptions="SELECT qoption, description, is_right FROM options WHERE idquestion = {};".format(idQuestion)
            cursor.execute(sqlOptions)
            options = cursor.fetchall()
            for option in options:
                print('{}. {}'.format(option[0], option[1]))
                if option[2]==1:
                    rightAnswer = option[0]
            answer = input("\nSelect one option:   ")
            emoticon = ':('
            if answer==rightAnswer: emoticon = ':)'
            print('Right answer: {} {}'.format(rightAnswer, emoticon))
            # Update answer
            updateQuestionAnswer(idSimulation, idQuestion, answer, rightAnswer, conexion)
        except mysql.connector.Error as err:
            print("### - something fail while managing data:", err)

    # set results
    setResults(idSimulation, max_questions, conexion)

def insertSimulationQuestion(idSimulation, idQuestion, conexion):
    sql = "INSERT INTO simulation (idsimulation, idquestion) VALUES ('{}','{}');".format(idSimulation, idQuestion)
    try:
        cursor = conexion.cursor()
        cursor.execute(sql)
        cursor.execute('UPDATE questions SET used = used+1 WHERE id = {};'.format(idQuestion))
        conexion.commit()
    except mysql.connector.Error as err:
        print('### - Can not create the question in the simulation.', err)

def updateQuestionAnswer(idSimulation, idQuestion, answer, rightAnswer, conexion):
    evaluation = 0    
    if answer==rightAnswer: evaluation = 1
    sql = "UPDATE simulation SET selected1 = '{}', evaluation = {} WHERE idsimulation = {} and idquestion = {}".format(answer, evaluation, idSimulation, idQuestion)
    try:
        cursor = conexion.cursor()
        cursor.execute(sql)
        conexion.commit()
    except mysql.connector.Error as err:
        print('### - Can not update answer', err)

def setResults(idSimulation, count, conexion):
    sql = "SELECT TIMESTAMPDIFF(MINUTE, startAt, endAt) as myTime, result FROM simulations WHERE id={}".format(idSimulation)
    try:
        cursor = conexion.cursor()
        sqlUpdate = "UPDATE simulations SET result = (SELECT sum(evaluation) FROM simulation WHERE idsimulation = {}), endAt = current_timestamp WHERE id = {};".format(idSimulation, idSimulation)
        cursor.execute(sqlUpdate)
        conexion.commit()
        cursor.execute(sql)
        rows = cursor.fetchall()
        time = rows[0][0]
        result = rows[0][1]
        text = "| Result simulation: {} of {} were correct in {} minutes. Yor score is: {}".format(result, count, time, (result/count)*100)
        textspaces = [' ']*(78-len(text))
        print('- ---------------------------------------------------------------------------- -')
        print(text, ''.join(textspaces), '|')
        print('- ---------------------------------------------------------------------------- -')
        cursor.execute(sql)
    except mysql.connector.Error as err:
        print('### - Failed to set final result:', err)

config = {
  'user': 'syssimulator',
  'password': 'genseg89+',
  'host': '127.0.0.1',
  'database': 'gcparchexam',
  'raise_on_warnings': True
}

try: 
    cnx = mysql.connector.connect(**config)
    print("connection done!")
    startSimulation(cnx)
    print("closing connection ...")
    cnx.close()
except mysql.connector.Error as err:
    print("### - something fail while connecting to mysql:", err)