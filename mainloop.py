import os
import json
from PyInquirer import style_from_dict, prompt, Token
import pyfiglet
from pprint import pprint
from simral.driver import DppaSimralDriver as dppa
from simral.config import Config as cfg
from executor.import_dppa import skpd_prompt,dppa_operation_prompt,import_dppa_operation
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
    # with open("dpa.json","r") as f:
    #     jsonData=json.load(f)
    # choices=[f'{d["kode_skpd"]} {d["nama_skpd"]}' for d in jsonData]
    # choices.append("Back")
    # skpd_prompt={
    #     'type':'list',
    #     'name':'skpd',
    #     'message':'Pilih SKPD yang akan diimport:',
    #     'choices':choices
    # }
    answers=skpd_prompt()
    return dppa_operation_prompt(answers)

def ask_dppa_operations(skpd):
    skpd_prompt={
        'type':'list',
        'name':'operation',
        'message':'Pilih Operasi pada SKPD: {}'.format(skpd),
        'choices':['Import DPPA','Input DPPA']
    }
    answers=prompt(skpd_prompt)
    return dppa_operations(skpd,answers['operation'])

def dppa_operations(skpd,operation='Import DPPA'):
    skpdStrings=skpd.strip().split(" ",1)
    print(f'{skpdStrings[0]} {skpdStrings[1]}')
    print(operation)
    config=cfg.Config()
    sd=dppa.DppaSimralDriver(skpdStrings[0],skpdStrings[1])
    sd.connect(r'./chromedriver.exe',False)
    sd.get_captcha()
    captcha_prompt={
        'type': 'input',
        'name': 'captcha',
        'message': 'Masukkan kode captcha?',
        'filter': lambda val: int(val)
    }
    answer=prompt(captcha_prompt)
    anggaran_config=config.get_simral_perubahan_config()
    sd.login(anggaran_config['username'],anggaran_config['password'],anggaran_config['cfg'],answer['captcha'])
    sd.select_modul("Perubahan","objTreeMenu_1_node_2_2")
    sd.import_pilih_kegiatan(anggaran_config['periode'],'5.02.0.00.0.00.01.0004','Bidang Akutansi dan Teknologi Informasi')
    sd.import_kegiatan(anggaran_config['jenis_perubahan'])

def ask_direction():
    directions_prompt = {
        'type': 'list',
        'name': 'operation',
        'message': 'Pilih Operasi Pada Simral?',
        'choices': ['APBD-P', 'Validasi SP2D', 'BKU Pendapatan PPKD',"Exit"]
    }
    answers = prompt(directions_prompt,style=custom_style_2)
    return answers['operation']

# TODO better to use while loop than recursion!


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
    elif (direction == 'Exit'):
        print("Bye")
        exit(0)
    else:
        print('You cannot go that way. Try again')
        main_loop()


def encounter1():
    direction = ask_direction()
    if (direction == 'Forward'):
        print('You attempt to fight the wolf')
        print('Theres a stick and some stones lying around you could use as a weapon')
        encounter2b()
    elif (direction == 'Right'):
        print('You befriend the dwarf')
        print('He helps you kill the wolf. You can now move forward')
        encounter2a()
    else:
        print('You cannot go that way')
        encounter1()


def encounter2a():
    direction = ask_direction()
    if direction == 'Forward':
        output = 'You find a painted wooden sign that says:'
        output += ' \n'
        output += ' ____  _____  ____  _____ \n'
        output += '(_  _)(  _  )(  _ \\(  _  ) \n'
        output += '  )(   )(_)(  )(_) ))(_)(  \n'
        output += ' (__) (_____)(____/(_____) \n'
        print(output)
    else:
        print('You cannot go that way')
        encounter2a()


def encounter2b():
    prompt({
        'type': 'list',
        'name': 'weapon',
        'message': 'Pick one',
        'choices': [
            'Use the stick',
            'Grab a large rock',
            'Try and make a run for it',
            'Attack the wolf unarmed'
        ]
    }, style=custom_style_2)
    print('The wolf mauls you. You die. The end.')


if __name__ == '__main__':
    main()