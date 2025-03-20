def hello():
    return "Hello!"


def greet(name):
    return f"Hello, {name}!"

def calc(a, b, operation = 'multiply'):
    try:
        match operation:
            case 'multiply':
                return a * b
            case 'divide':
                return a / b
            case 'int_divide':
                return a // b
            case 'add':
                return a + b
            case 'subtract':
                return a - b
            case 'power':
                return a ** b
            case 'modulo':
                return a % b
            case _:
              return "No operation match, please use: multiply, divide, int_divide, add, subtract, power, or modulo."
    except ZeroDivisionError:
        return "You can't divide by 0!"
    except TypeError:
        return "You can't multiply those values!"
    
print(calc(5,7, 'powerrrr'))    
    
def data_type_conversion(value, data_type):
    try:
        match data_type:
            case 'float':
                return float(value)
            case 'str':
                return str(value)
            case 'int':
                return int(value)
    except ValueError:
        return f"You can't convert {value} into a {data_type}."
    
def grade(*args):
    try:
        avg = sum(args) / len(args)
        if avg >= 90 :
            return "A"
        elif 80 <= avg <= 89:
            return "B"
        elif 70 <= avg <= 79:
            return "C"
        elif 60 <= avg <= 69:
            return "D"
        else:
            return "F"
    except TypeError:
        return "Invalid data was provided."

def repeat(string, count):
    new_string = ""
    for _ in range(count):
        new_string += string
    return new_string
        
#print(repeat('up,', 4))
        
        
def student_scores(param, **kwargs):
    if param == 'best':
        best_score = 0
        student = ''
        for key, value in kwargs.items():
            if value > best_score:
                best_score = value
                student = key
        return student
    elif param == 'mean':
        total = sum(kwargs.values())
        return total / len(kwargs)

print(student_scores("mean", Tom=75, Dick=89, Angela=91))
print(student_scores("best", Tom=75, Dick=89, Angela=91, Frank=50))


def titleize(a):
    words = []
    little_words = ("a", "on", "an", "the", "of", "and", "is", "in")
    titleString = ''
    for word in a.split():
        words.append(word)
    for word in words:
      if (word not in little_words) or ((word == words[0]) or (word == words[-1])):
        word = word.capitalize()
      titleString = titleString + ' ' + word
    return titleString.strip()
    

def hangman(secret, guess):
  hidenString= ""
  for _ in secret:
    if _ in guess:
      hidenString += _
    else:
      hidenString += '_'


  return hidenString

#print(hangman("difficulty","ic"))

  for word in words:
   pigLatin = word
 
   if 'qu' in pigLatin:
     pigLatin = pigLatin.replace('qu','',1)
     #print(pigLatin)
     pigLatin += 'qu'
     #print(pigLatin)
 
 
   if pigLatin[0] in volves:
     pigLatinStr += pigLatin + 'ay' + ' '
    