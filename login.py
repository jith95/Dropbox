def menu():
    d = {}
    with open(r"C:\Users\SREEJITH\Desktop\IITGN\DB\Database.txt") as f:
        for line in f:
           (key, val) = line.split()
           d[key] = val
    def listfile():
        pass
    def uploadfile():
        pass
    def downloadfile():
        pass
    def deletefile():
        pass
    def sharefile():
        pass
    def showlog():
        pass
    def signout():
        print("Thank You...")
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
                print("\n1.List files:")
                print("\n2.Upload files:")
                print("\n3.Download files:")
                print("\n4.Delete files:")
                print("\n5.Share files:")
                print("\n6.Show log:")
                print("\n7.Sign out:")
                while 1:
                    choice=int(input("Enter choice(1-7): "))
                    if(choice==1):
                        listfile()
                        break
                    if(choice==2):
                        uploadfile()
                        break
                    if(choice==3):
                        downloadfile()
                        break
                    if(choice==4):
                        deletefile()
                        break
                    if(choice==5):
                        sharefile()
                        break
                    if(choice==6):
                        showlog()
                        break
                    if(choice==7):
                        signout()
                        break
                    if(choice>7 or choice<1):
                        print("Incorrect choice")
                break
            else:
                print("Passwords don't match")
                

    print("Welcome...")
    welcome = input("Do you have an acount? y/n: ")
    if welcome == "n":
        signup()
     
    if welcome == "y":
        login()
menu()        
