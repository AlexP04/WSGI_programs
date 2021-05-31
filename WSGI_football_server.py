from wsgiref.simple_server import make_server
import cgi
import random

HTML_PAGE_Rating = """
<html>
<title>Рейтинг команд</title>
<body>
<h3>Рейтинг команд</h3>
<br>
<table style="width:100%">
<tr>
<th>№</th>
<th>Назва</th>
<th>Ігор</th>
<th>Виграшів</th>
<th>Нічиїх</th>
<th>Поразок</th>
<th>Голів забито</th>
<th>Голів пропущено</th>
<th>Кількість очок</th>
</tr>
{}
</table>
</body>
</html>
"""

HTML_PAGE_Results = """
<html>
<title></title>
<body>
<h3>Ігрові результати</h3>
<br>
<table style="width:100%">
<tr>
<th>Перша команда</th>
<th>Друга команда</th>
<th>_</th>
<th>_</th>
</tr>
{}
</table>
</body>
</html>
"""

HTML_PAGE_main = """<html>
<title>Головна</title>
<body>
<br>
<form method=POST action="rating">
<input type="submit" value="Рейтинг команд">
</form>
<form method=POST action="results">
<input type="submit" value="Результати матчів">
</form>
</body>
</html>
"""

class Command:
    name=''
    games=1
    win=0
    lose=0
    withdraws=0
    goal_in=0
    goal_out=0

    def GetScore(self):
        return self.win*3+self.withdraws*1
    def __init__(self,n):
        self.name=n
    def __lt__(self,other):
        if self.GetScore()!=other.GetScore():
            return self.GetScore()<other.GetScore()
        a=self.goal_in-self.goal_out
        b=other.goal_in-other.goal_out
        if a!=b:
            return a<b
        
        if self.goal_in!=other.goal_in:
            return self.goal_in<other.goal_in
        random.seed()
        a=random.random()
        b=random.random()
        return a<b


def CreateResults():
    result=''
    list_of_strings=[]
    list_file = open("list_of_matches.txt")
    for line in list_file: 
        divided_line = line.split()
        list_of_strings.append(divided_line)
    

    list_file.close()

    commands=[]

    for item in list_of_strings:
        is_first_present=False
        is_second_present=False
        is_first_winer=False
        is_withdraw=False

        if int(item[2])==int(item[3]):
            is_withdraw=True
        elif int(item[2])>int(item[3]):
            is_first_winer=True
        
        index=0
        while index<len(commands):
            if commands[index].name == item[0]:
                is_first_present=True
                break
            index+=1

        if is_first_present:
            if is_first_winer:
                commands[index].win+=1
            else: 
                if is_withdraw:
                    commands[index].withdraws+=1
                else:
                    commands[index].lose+=1
            commands[index].goal_in+=int(item[2])
            commands[index].goal_out+=int(item[3])
            commands[index].games+=1
        else:
            new_command = Command(item[0])
            if is_first_winer:
                new_command.win=1
            else: 
                if is_withdraw:
                    new_command.withdraws=1
                else:
                    new_command.lose=1
            new_command.goal_in=int(item[2])
            new_command.goal_out=int(item[3])
            commands.append(new_command)

        index=0  
        while index<len(commands):
            if commands[index].name == item[1]:
                is_second_present=True
                break
            index+=1
        if is_second_present:
            if is_first_winer:
                commands[index].lose+=1
            else: 
                if is_withdraw:
                    commands[index].withdraws+=1
                else:
                    commands[index].win+=1
            commands[index].goal_in+=int(item[3])
            commands[index].goal_out+=int(item[2])
            commands[index].games+=1
        else:
            new_command = Command(item[1])

            if is_first_winer:
                new_command.lose=1
            else: 
                if is_withdraw:
                    new_command.withdraws=1
                else:
                    new_command.win=1
            new_command.goal_in=int(item[3])
            new_command.goal_out=int(item[2])
            commands.append(new_command)
        
    commands.sort()
    commands.reverse()
    index=1
    for item in commands:
            result+='<tr><th>' +str(index) + '</th><th>' + item.name + '</th><th>' + str(item.games) + '</th><th>' + str(item.win) +'</th><th>' + str(item.withdraws) + '</th><th>' + str(item.lose) + '</th><th>' + str(item.goal_in) + '</th><th>' + str(item.goal_out) + '</th><th>' + str(item.GetScore()) + '</th></th>'
            index+=1
    return result


def CreateRatingList():
    result=''
    list_of_strings=[]
    list_file = open("list_of_matches.txt")
    for line in list_file: 
        divided_line = line.split()
        list_of_strings.append(divided_line)
    

    print(list_of_strings)
    list_file.close()


    for item in list_of_strings:
        result+='<tr><th>' + item[0] + '</th><th>' + item[1] + '</th><th>' + item[2] + '</th><th>' + item[3] +'</th></th>'
    print(result)
    return result
 
def CreateMatchList():
    result=''
    list_of_strings=[]
    list_file = open("list_of_matches.txt")
    for line in list_file: 
        divided_line = line.split()
        list_of_strings.append(divided_line)
    
    list_file.close()
    for item in list_of_strings:
        result+='<tr><th>' + item[0] + '</th><th>' + item[1] + '</th><th>' + item[2] + '</th><th>' + item[3] +'</th></th>'
    return result



def application(environ,start_response):
    if environ.get('PATH_INFO', '').lstrip('/') == "results":
        body = HTML_PAGE_Results.format(CreateMatchList())
        start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])
    elif environ.get('PATH_INFO', '').lstrip('/') == 'rating':
        body = HTML_PAGE_Rating.format(CreateResults())
        start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])
    elif environ.get('PATH_INFO', '').lstrip('/') == '':
        body = HTML_PAGE_main
        start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])
    else:
        body="OOOPS! Something is wrong!"
        start_response('404 NOT FOUND', [('Content-Type', 'text/plain')])
    return [bytes(body, encoding='utf-8')]
print('=== Local WSGI webserver ===')
my_server = make_server('localhost', 8000, application).serve_forever()