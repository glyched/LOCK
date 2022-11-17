from ast import While
from csv import DictReader, DictWriter, writer
import csv
from http import server
import base64
import hashlib
from hashlib import md5
from msilib.schema import IniFile
from venv import create
from Cryptodome.Cipher import AES
from os import urandom
import os
import pandas as pd

def Service_list(x):
    n=0 
    print('|S.num|','Service')
    print('|-----|','-----------')
    with open(x, 'r') as csv_file:
        file_reader = DictReader(csv_file,('service', 'usrname', 'password', 'note'))
        next(csv_file)
        for line in file_reader:
            n += 1
            print('|',n,'  |',line['service'])
    csv_file.close()

def Service_add(f_name,ser,usr,passw,note):
    with open(f_name,'a') as f:
        writer = csv.writer(f)
        writer.writerow([ser,usr,passw,note])
    f.close()
def derive_key_and_iv(password, salt, key_length, iv_length): 
    d = d_i = b''
    while len(d) < key_length + iv_length:
        d_i = md5(d_i + str.encode(password) + salt).digest() 
        d += d_i
    return d[:key_length], d[key_length:key_length+iv_length]

def encrypt(in_file, out_file, password, key_length=32):
    bs = AES.block_size 
    salt = urandom(bs) 
    key, iv = derive_key_and_iv(password, salt, key_length, bs)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    out_file.write(salt)
    finished = False

    while not finished:
        chunk = in_file.read(1024 * bs) 
        if len(chunk) == 0 or len(chunk) % bs != 0:
            padding_length = (bs - len(chunk) % bs) or bs
            chunk += str.encode(padding_length * chr(padding_length))
            finished = True
        out_file.write(cipher.encrypt(chunk))

def decrypt(in_file, out_file, password, key_length=32):
    bs = AES.block_size
    salt = in_file.read(bs)
    key, iv = derive_key_and_iv(password, salt, key_length, bs)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    next_chunk = ''
    finished = False
    while not finished:
        chunk, next_chunk = next_chunk, cipher.decrypt(in_file.read(1024 * bs))
        if len(next_chunk) == 0:
            padding_length = chunk[-1]
            chunk = chunk[:-padding_length]
            finished = True 
        out_file.write(bytes(x for x in chunk)) 
def Create_file(name):

    paswrd = input('enter your master password(REMEMBER THIS):')
    with open('y.csv','w',encoding='utf-8-sig') as csvfile:
        filewriter = csv.writer(csvfile)
        filewriter.writerow(['service','usrname','password','note'])
        print('main file created... encrypting...')
        print('RE RUN THE PROGRAM AND POINT TO THIS FILE WHEN THE TIME COMES:')
    with open('y.csv','rb') as in_file, open(name,'wb') as outfile:
        encrypt(in_file,outfile,paswrd)
    os.remove('y.csv')
    
def main():
    try:
        h = input('is this the first time using/Do you need a new saves file?(y/n): ')
        if h == 'y':
            t = input('enter the name you want your file to be:')
            Create_file(t)
        else:
            x = input('enter the name of your file:')
            passwrd= input('Enter password:')
        
        try:
                    with open(x, 'rb') as in_file, open('y.csv', 'wb') as out_file:
                                decrypt(in_file, out_file, passwrd)
                    while True:
                        print('|--------------------|')
                        print('|S.num|    options   |')
                        print('|-----|--------------|')
                        print('|1    |  Add login   |')
                        print('|2    | Remove login |')
                        print('|3    |View passwords|')
                        print('|4    |Ecncrypt File |')
                        print('|5    |Change passwrd|')
                        print('|6    |     Exit     |')
                        print('-----------------------')
                        choice = input('Enter your choice: ')
                        if choice == '1':
                            ser = input('Enter the service name: ')
                            usr = input('Enter the username: ')
                            passw = input('Enter the password: ')
                            note = input('Enter the note: ')
                            Service_add('y.csv',ser,usr,passw,note)
                        if choice == '2':
                            Service_list('y.csv')
                            u = int(input('Enter the s.num of service to be removed: '))
                            u=u+1
                            with open('y.csv', 'r') as fr:
                            # reading line by line
                                lines = fr.readlines()
                                
                                # pointer for position
                                ptr = 1
                        
                                # opening in writing mode
                                with open('y.csv', 'w') as fw:
                                    for line in lines:
                                    
                                        # we want to remove 5th line
                                        if ptr != u:
                                            fw.write(line)
                                        ptr += 1
                            
                            
                        if choice == '3':
                            Service_list('y.csv')
                            o = int(input('Enter the S.num of the service to view: '))
                            
                            with open('y.csv', 'r') as csv_file:
                                k = 1
                                file_reader = DictReader(csv_file,('service', 'usrname', 'password', 'note'))
                                next(csv_file)
                                for line in file_reader:
                                        if o == k:
                                            print('---------------------------------------')
                                            print('service : ',line['service'])
                                            print('Username : ', line['usrname'])
                                            print('password: ',line['password'])
                                            print('note : ',line['note'])
                                        k += 1
                        if choice == '4':
                            print('encrypting will do the same thing as exiting, it will delete all traces of the decrypted file and save it to just one file with encryption')
                            print('are you sure you would like to re-encrypt the current changes made y/n:')          
                            l = input()
                            if l == 'y':
                                os.remove(x)
                                with open('y.csv', 'rb') as in_file, open(x, 'wb') as out_file:
                                    encrypt(in_file, out_file, passwrd)
                                os.remove('y.csv')
                                break
                            else:
                                continue  
                        if choice == '5':
                            j = input('enter current password:')
                            if j == passwrd:
                                new_pass = input('enter new password:')
                                check= input('enter new password again:')   
                                if new_pass == check:
                                    os.remove(x)
                                    with open('y.csv', 'rb') as in_file, open(x, 'wb') as out_file:
                                        encrypt(in_file,out_file,new_pass)
                                    os.remove('y.csv')
                                    

                                else:
                                    print('passwords dont match')
                            else:
                                print('incorrect password')
                        if choice == '6':
                            print('securing and exiting...')
                            os.remove(x)
                            with open('y.csv', 'rb') as in_file, open(x, 'wb') as out_file:
                                encrypt(in_file, out_file, passwrd)
                            os.remove('y.csv')
                            break
        except KeyboardInterrupt:
                    print('Exiting the program...')
                    print('securing files...')
                    os.remove(x)
                    with open('y.csv', 'rb') as in_file, open(x, 'wb') as out_file:
                        encrypt(in_file, out_file, passwrd)
                    os.remove('y.csv')
    except:
        print('error')
        print('securing files...')
        os.remove(x)
        with open('y.csv', 'rb') as in_file, open(x, 'wb') as out_file:
            encrypt(in_file, out_file, passwrd)
        os.remove('y.csv')

main()