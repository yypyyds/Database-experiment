import sys   
from config import *
import pymssql
print(sys.getdefaultencoding())

conDB = pymssql.connect(db_config['host'], db_config['user'], db_config['password'], db_config['db'], db_config['charset'])

if conDB:
    print("连接成功")
    Show_menu()
    cursor = conDB.cursor()
    opt = input()
    while(opt != '0'):
        if (opt == '1'):
            Add_student_info(cursor,conDB)
        elif(opt == '2'):
            Update_student_info(cursor,conDB)    
        elif(opt == '3'):
            Add_new_course(cursor,conDB)    
        elif(opt == '4'):
            Update_course_info(cursor,conDB)   
        elif(opt == '5'):
            Add_student_grades(cursor, conDB)    
        elif(opt == '6'):
            Update_student_grades(cursor, conDB)    
        elif(opt == '7'):
            Get_dept_statistics(cursor, conDB)
        elif(opt == '8'):
            Get_grade_order(cursor, conDB)
        elif(opt == '9'):
            Get_stu_info(cursor,conDB)
        elif(opt == '0'):
            break
        print("******操作完成******")
        Show_menu()
        opt = input()
else:
    print ("连接失败")
# 连接用完后记得关闭以释放资源
conDB.close()