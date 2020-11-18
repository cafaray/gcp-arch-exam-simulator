import mysql.connector
import re

def readfile(name, conexion):
    fhandler = open(name)
    count = 1
    for line in fhandler:
        line = line.replace("\n", "")
        words = line.split(",")
        sqlInsertTopic = "INSERT INTO topics (description, file) VALUES ('{0}', '{1}');".format(words[0], words[1])
        #print(sqlInsertTopic)
        try:            
            cursor = conexion.cursor()
            cursor.execute(sqlInsertTopic)
            conexion.commit()
            count = count +1        
        except mysql.connector.Error as err:
            print("### - something fail while managing data:", err)
    print('Topics inserted: ', count)
    print('---------------------------')

def loadQuestions(conexion):
    optionpattern = '^[A,B,C,D,E,F][.] '
    answerpattern = '[\d]{1,2}[.]\s[A-F].\w*'
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM topics;")
        rows = cursor.fetchall()
        for row in rows:
            filename = row[2]
            topic = row[0]
            print("working file:", filename)
            fhandler = open(filename)
            isAnswer = False
            isOption = False
            countq = 0
            counto = 0
            for line in fhandler:                
                if re.match('\w', line):                    
                    isOption = re.match(optionpattern, line)
                    isAnswer = re.match(answerpattern, line)
                    # print('isOption={}, isAnswer={}'.format(isOption, isAnswer))                    
                    if isOption:
                        insertOption(line, conexion)
                        counto = counto+1
                    elif isAnswer:
                        updateExplanation(line, conexion)
                        updateOption(line, conexion)
                    else:
                        insertQuestion(topic, line, conexion)                        
                        countq = countq+1                        
                else:
                    # print('blank space', line)
                    continue
            print("\tQuestions inserted {} with {} options".format(countq, counto))
    except mysql.connector.Error as err:
        print("### - something fail while managing data:", err)

def updateOption(line, conexion):
    line = line.replace('\n', '')
    optionLine = line.split(" ")
    option = optionLine[1][0]
    sql = "UPDATE options SET is_right = True WHERE qoption = '{}' and idquestion = (SELECT id FROM questions ORDER BY id desc limit 1);".format(option)
    try:            
        cursor = conexion.cursor()
        cursor.execute(sql)
        conexion.commit()
    except mysql.connector.Error as err:
        print("### - something fail while updating otion {}: {}".format(sql, err))

def updateExplanation(line, conexion):
    qid=-1
    try:            
        cursor = conexion.cursor()
        cursor.execute("SELECT id FROM questions ORDER BY id desc limit 1")
        rows = cursor.fetchall()
        for row in rows:
            qid = row[0]
            # print('qid:',qid)
    except mysql.connector.Error as err:
        print("### - something fail while updating question explanation: {}".format(err))
        return 
    line = line.replace('\n', '')
    sql = "UPDATE questions SET explanation = '{}' WHERE id = {};".format(line, qid)
    try:            
        cursor = conexion.cursor()
        cursor.execute(sql)
        conexion.commit()
    except mysql.connector.Error as err:
        print("### - something fail while updating question explanation {}: {}".format(sql, err))

def insertQuestion(topic, line, conexion):
    line = line.replace('\n', '')
    sql = "INSERT INTO questions (question, idtopic) VALUES ('{}', '{}');".format(line, topic)
    try:            
        cursor = conexion.cursor()
        cursor.execute(sql)
        conexion.commit()
        #cursor.execute("SELECT id FROM questions ORDER BY id desc;")
        #rows = cursor.fetchone()
        #for row in rows:
        #    qid = row
        #print('qid=', qid)
        #return qid
    except mysql.connector.Error as err:
        print("### - something fail while inserting question:", err)
        #return -1


def insertOption(line, conexion):
    line = line.replace('\n', '')
    option = line[0]
    description = line[3:]
    isRight = 0
    sql = "INSERT INTO options (idquestion, qoption, description, is_right) VALUES ((SELECT id FROM questions ORDER BY id desc limit 1),'{}','{}','{}');".format(option, description, isRight)
    try:            
        cursor = conexion.cursor()
        cursor.execute(sql)
        conexion.commit()
    except mysql.connector.Error as err:
        print("### - something fail while inserting option for question {}: {}".format(sql, err))

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
    print("Loading topics")
    readfile("manager_loader.txt", cnx)
    loadQuestions(cnx)
    print("closing connection ...")
    cnx.close()
except mysql.connector.Error as err:
    print("### - something fail while connecting to mysql:", err)

