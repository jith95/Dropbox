print("Welcome...")
welcome = input("Do you have an acount? y/n: ")
if welcome == "n":
    while True:
        username  = input("Enter a username:")
        password  = input("Enter a password:")
        password1 = input("Confirm password:")
        if password == password1:
            file = open(r"C:\Users\SREEJITH\Desktop\IITGN\DB\Database.txt", "a+")
            file.write(username+":"+password)
            file.close()
            welcome = "y"
            break
        print("Passwords do NOT match!")
 
if welcome == "y":
    while True:
        login1 = input("Login:")
        login2 = input("Password:")
        file = open(r"C:\Users\SREEJITH\Desktop\IITGN\DB\Database.txt", "r")
        data   = file.readline()
        file.close()
        print(data)
        if data == login1+":"+login2:
            print("Welcome")
            break
        print("Incorrect username or password.")