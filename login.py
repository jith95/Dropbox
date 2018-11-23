d = {}
with open(r"C:\Users\SREEJITH\Desktop\IITGN\DB\Database.txt") as f:
    for line in f:
       (key, val) = line.split()
       d[key] = val
def signup():
    while True:
        username  = input("Enter a username:")
        password  = input("Enter a password:")
        password1 = input("Confirm password:")
        if password == password1:
            file = open(r"C:\Users\SREEJITH\Desktop\IITGN\DB\Database.txt", "a+")
            #file = open(r"file.txt", "a+")
            file.write(username+" "+password+"\n")
            file.close()
            welcome = "y"
            break
        print("Passwords do NOT match!")
def login():
    s=0
    while True:
        login1 = input("Login:")
        login2 = input("Password:")
        file = open(r"C:\Users\SREEJITH\Desktop\IITGN\DB\Database.txt", "r")
        #file = open(r"file.txt", "r")
        for i in d:
            if i==login1 and d[i]==login2:
                s=1
                break;
        if(s==1):
            print("Welcome")
            
            break
        else:
            print("Passwords don't match")
            

print("Welcome...")
welcome = input("Do you have an acount? y/n: ")
if welcome == "n":
    signup()
 
if welcome == "y":
    d=login()
        
