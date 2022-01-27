from os import execl
import pymssql

db_config = {
    'host': 'LAPTOP-S5QSRMBL',
    'user': 'root',
    'password': 'root',
    'db': 'S_T_U201911741',
    'charset': 'cp936',
    #'cursorclass': pymssql.cursors.DictCursor
}
Student = {
    '11741',
    '鄢湧棚',
    '男',
    '20',
    'cse',
    '是'
}
Student_list = (
    'Sno',
    'Sname',
    'Ssex',
    'Sage',
    'Sdept',
    'Scholarship'
)
Course_list = (
    'Cno',
    'Cname',
    'Cpno',
    'Ccredit'
)

def printc(str):
    print(str.encode('latin-1').decode('gbk'), end="")

def Add_student_info(cursor,conDB):
    print ("请输入学生信息（学号，姓名，性别，年龄，专业，奖学金获得情况）")
    stu_in = input()
    Student = stu_in.split()
    #print (Student)
    sql_add = "insert into student values('" + Student[0] + "','" + \
        Student[1] + "','" + Student[2] + "','" + Student[3] \
            + "','" + Student[4] + "','" + Student[5] + "');"
    #print (sql_add)
    cursor.execute(sql_add)
    conDB.commit()
    return

def Update_student_info(cursor,conDB):
    print("请输入要修改的内容（0.学号 1.姓名 2.性别 3.年龄 4.专业 5.奖学金）(先输入序号，再输入内容)")
    flag = input()
    item = flag.split()
    item[0] = int(item[0])
    if(item[0] != 3):
        item[1] = "'" + item[1] + "'"
    #print (item)
    print("请输入要修改的学生的学号或姓名")
    opt = input()
    if(opt.isdigit()):
        sno = opt
        sql_update = "update student set " + Student_list[item[0]] + " = " + item[1] + " where Sno = '" + sno + "';"
    else:
        sname = opt
        sql_update = "update student set " + Student_list[item[0]] + " = " + item[1] + " where Sname = '" + sname + "';"
    #print (sql_update)
    cursor.execute(sql_update)
    conDB.commit()
    return

def Add_new_course(cursor,conDB):
    print("请输入课程信息（课程号，课程名，先修课程（无则填NULL），学分）")
    course_in = input()
    course = course_in.split()
    #print(course)
    sql_add = "insert into course values('" + course[0] + "', '" + course[1] + "', " + course[2] + "," + course[3] + ");"
    #print (sql_add)
    cursor.execute(sql_add)
    conDB.commit()
    return

def Update_course_info(cursor,conDB):
    print("请输入修改课程的课程号或课程名")
    info_in = input()
    print("请输入要修改的内容（0.课程 1.课程名 2.先修课程 3.学分）")
    flag = input()
    item = flag.split()
    item[0] = int(item[0])
    if(item[0] != 3):
        item[1] = "'" + item[1] + "'"
    if(info_in.isdigit()):
        cno = info_in
        sql_update = "update course set " + Course_list[item[0]] + " = " + item[1] + " where Cno = '" + cno + "';"
    else:
        cname = info_in
        sql_update = "update course set " + Course_list[item[0]] + " = " + item[1] + " where Cname = '" + cname + "';"
    #print (sql_update)
    cursor.execute(sql_update)
    conDB.commit()
    return

def Delete_not_select_course(cursor,conDB):
    sql = "delete from course where Cno not in(select distinct Cno from SC);"
    cursor.execute(sql)
    conDB.commit()
    print("Cleanup complete.")
    return

def Add_student_grades(cursor,conDB):
    print("请输入学生学号，课程号，成绩（输入0停止输入）")
    while(True):
        a = input()
        if (a == '0'):
            break
        SC = a.split()
        sql_add = "insert into SC values('" + SC[0] + "', '" + SC[1] + "', " + SC[2] + ");"
        #print (sql_add)
        cursor.execute(sql_add)
        conDB.commit()
    return

def Update_student_grades(cursor, conDB):
    print("请输入要修改的学生学号，课程号和成绩")
    SC_in = input()
    SC = SC_in.split()
    sql_update = "update SC set grade = " + SC[2] + " where Sno = '" + SC[0] + "' and Cno = '" + SC[1] + "';"
    #print(sql_update)
    cursor.execute(sql_update)
    conDB.commit()
    return

def Get_dept_statistics(cursor,conDB):
    sql1 = "select distinct Sdept from student;"
    cursor.execute(sql1)
    dept_get = cursor.fetchall()
    size = len(dept_get)
    for i in range (0,size):
        temp = str(dept_get[i])
        dept = temp[2:4]
        if(temp[4].isalpha()):
            dept = dept + temp[4]
        print(dept)
        #最大，最小，平均
        sql_max_min_avg = "SELECT MAX(Grade) MAX, MIN(Grade) MIN, AVG(Grade) AVG FROM SC where Sno in (select Sno from student where Sdept = '"+dept+"');"
        cursor.execute(sql_max_min_avg)
        max_min_avg = cursor.fetchall()
        print("max_min_avg:",max_min_avg[0][0],max_min_avg[0][1],max_min_avg[0][2])
        #不及格人数
        sql_failed = "select count(*) from SC, Student where grade<60 and Sc.Sno=Student.sno and Student.Sdept='"+dept+"';"
        cursor.execute(sql_failed)
        failed = cursor.fetchall()
        print("failed:",failed[0][0])
        #优秀率
        sql2 = "select count(*) from student where Sdept = '"+dept+"';"
        cursor.execute(sql2)
        total = cursor.fetchall()
        print("total:",total[0][0])
        sql3 = "select count(*) from SC, Student where grade >= 80 and SC.Sno=Student.Sno and Student.Sdept = '"+dept+"';"
        cursor.execute(sql3)
        execelent = cursor.fetchall()
        print("execelent:",execelent[0][0])
        a = float(total[0][0])
        b = float(execelent[0][0])
        print("execelent rate:",b/a)
        print("")
    return

def Get_grade_order(cursor, conDB):
    sql1 = "select distinct Sdept from student;"
    cursor.execute(sql1)
    dept_get = cursor.fetchall()
    size = len(dept_get)
    for i in range (0,size):
        temp = str(dept_get[i])
        dept = temp[2:4]
        if(temp[4].isalpha()):
            dept = dept + temp[4]
        sql2 = "select Sname, Cname, grade from SC, student, Course where SC.Sno = Student.Sno and SC.Cno = Course.Cno and Sdept = '" + dept + "' order by grade desc;"
        cursor.execute(sql2)
        ret = cursor.fetchall()
        i = len(ret)
        print(dept)
        if(i != 0):
            for j in range(0,i):
                printc(ret[j][0])
                printc(ret[j][1])
                print(ret[j][2])
        else:
            print("没有学生成绩")
    return

def Get_stu_info(cursor,conDB):
    Sno = input("请输入学生学号:")
    sql1 = "select * from student where Sno = '"+Sno+"';"
    cursor.execute(sql1)
    base_info = cursor.fetchall()
    sql2 = "select SC.Cno, Cname from SC, Course where Sno = '"+Sno+"' and SC.Cno = Course.Cno;"
    cursor.execute(sql2)
    course_info = cursor.fetchall()
    print("基础信息：")
    printc(base_info[0][1])
    printc(base_info[0][2])
    print("\t\t",base_info[0][3],"\t\t",end="")
    printc(base_info[0][4])
    printc(base_info[0][5])
    print("")
    if(len(course_info) == 0):
        print("该学生没有选课")
    else:
        print("选课信息")
        print(course_info[0][0], end="")
        printc(course_info[0][1])
        print("\n")
    return

def Show_menu():
    print("""
    功能菜单：(输入对应数字选择)
    1.添加学生信息
    2.修改学生信息
    3.添加新课程
    4.修改课程信息
    5.录入学生成绩
    6.修改学生成绩
    7.统计学生的平均成绩、最好成绩、最差成绩、优秀率、不及格人数
    8.显示学生排名
    9.查询学生信息
    0.退出
    """)