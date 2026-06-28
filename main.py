class Record:

    Grade_eq = {"A+": 10, "A": 9, "B+": 8, "B": 7, "C+": 6, "C": 5, "D": 4 }
    
    def __init__(self):
        pass

    def __str__(self):
        pass




class Student(Record):
    def __init__(self,name,branch,sem):
        self.__name = name
        self.__branch = branch
        self.__sem = sem
        
        self.menu()

    def __str__(self):
        pass
 
    def menu(self):
        print(f"========================= HOME =========================")
        print(f"Select from the following modes: ")
        print(f"1. View Course Info\n2. View Student Info\n3. Check your rank\n4. Others\n5. Exit")
        
        try:
            mode = int(input("Enter the mode: "))

            if mode == 1:
                self.CourseInfo()

            elif mode == 2:
                self.StudentInfo()

            elif mode == 3:
                self.Rankings()

            elif mode == 4:
                self.others()

            elif mode == 5:
                print("Thanks for visiting!!")

            else:
                print("MODE NOT FOUND!!!No such modes available, please select from the availabe modes.\n")
                self.menu()
        except:
            print("INVALID INPUT!!!Please enter a number to choose from the available modes.\n")
            self.menu()
            
    def CourseInfo(self):
        pass

    def StudentInfo(self):
        pass

    def Rankings(self):
        pass

    def others(self):
        pass

    def sgpa_calculate(self):
        pass

    def cgpa_calculate(self):
        pass


user1 = Student("Naveen", "Ele", 4)
