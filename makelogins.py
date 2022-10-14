from distutils.log import info
import random
import csv
import pandas 

alphabet = 'abcdefghijklmnopqrstuvwxyz'

def get_users(filename):
    '''Gets a list of all the current usernames'''
    usernames = set()
    information = {}
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            usernames.add(row[0])
            information[row[0]] = row[1]
    return information, usernames

def generate_info(length):
    '''generates a random login info of the specified length'''
    info = ""
    for i in range(length):
        info = info + alphabet[random.randint(0,len(alphabet)-1)]
    return info

def unique(user, usernames):
    '''checks if the username has already been added previously'''
    return user not in usernames

def add_user(information, usernames, user, password):
    '''adds the new user information'''
    information[user] = password
    usernames.add(user)

def generate_users(information, usernames, number):
    '''randomly generates a specified number of new users'''
    counter = 0
    #Counter to ensure we don't loop a long time if new users cannot be easily randomly generated
    while number > 0 and counter < 10:
        newuser = generate_info(random.randint(1,10))
        if (unique(newuser, usernames)):
            newpass = generate_info(random.randint(1,10))
            add_user(information, usernames,newuser, newpass)
            number -= 1
        counter += 1

def write_users(information, filename):
    with open(filename, 'w') as f:
        writer = csv.writer(f)
        for info in information.keys():
            writer.writerow([info, information[info]])


def main():
    number = input("number of users to generate: ")
    number = int(number)
    information, usernames = get_users("logininfo.csv")
    generate_users(information, usernames, number)
    write_users(information, "logininfo.csv")
    
main()