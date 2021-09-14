from PyInquirer import style_from_dict, prompt, Token
import pyfiglet
from executor.import_dppa import skpd_prompt,dppa_operation_prompt,import_dppa_operation
from executor.validasi_sp2d import *
from executor.bku_pendapatan import *
import logging

logging.basicConfig(level=logging.INFO)

custom_style_1 = style_from_dict({
    Token.Separator: '#cc5454',
    Token.QuestionMark: '#673ab7 bold',
    Token.Selected: '#cc5454',  # default
    Token.Pointer: '#673ab7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#f44336 bold',
    Token.Question: '',
})


custom_style_2 = style_from_dict({
    Token.Separator: '#6C6C6C',
    Token.QuestionMark: '#FF9D00 bold',
    #Token.Selected: '',  # default
    Token.Selected: '#5F819D',
    Token.Pointer: '#FF9D00 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#5F819D bold',
    Token.Question: '',
})


custom_style_3 = style_from_dict({
    Token.QuestionMark: '#E91E63 bold',
    Token.Selected: '#673AB7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#2196f3 bold',
    Token.Question: '',
})

def ask_skpd():
    answers=skpd_prompt()
    return dppa_operation_prompt(answers)

def ask_validation_file():
    filename=file_prompt()
    validasi_sp2d_operation(filename)

def ask_pendapatan_file():
    filename=file_pendapatan_prompt()
    input_bku_pendapatan(filename)

def ask_direction():
    directions_prompt = {
        'type': 'list',
        'name': 'operation',
        'message': 'Pilih Operasi Pada Simral?',
        'choices': ['APBD-P', 'Validasi SP2D', 'BKU Pendapatan PPKD',"Exit"]
    }
    answers = prompt(directions_prompt,style=custom_style_2)
    return answers['operation']
    
def main():
    title=pyfiglet.figlet_format("S I M R A L\nS U P P O R T",font="slant")
    print(title)
    try:
        while True:
            main_loop()
    except KeyboardInterrupt:
            print("Press Ctrl-C to terminate while statement")
            


def main_loop():
    direction = ask_direction()
    if (direction == 'APBD-P'):
        ask_skpd()
    elif (direction == 'Validasi SP2D'):
        ask_validation_file()
    elif (direction == 'BKU Pendapatan PPKD'):
        ask_pendapatan_file()
    elif (direction == 'Exit'):
        print("Bye")
        exit(0)
    else:
        print('Perintah tidak diketahui')
        main_loop()

if __name__ == '__main__':
    main()