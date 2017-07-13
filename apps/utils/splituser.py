
#username split functions #first_name #last_name 
def get_first_name(fullname):
    firstname = ''
    try:
        firstname = fullname.split()[0] 
    except Exception as e:
        print str(e)
    return firstname

def get_last_name(fullname):
    lastname = ''
    try:
        lastname = fullname.split(' ', 1)[-1]
    except Exception as e:
            print str(e)
    return lastname

def get_last_word(string):
    return string.split()[-1]