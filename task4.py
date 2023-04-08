import mysql.connector
mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Qzxcvbnm@123',
    database='db31'
    )
cur = mydb.cursor()
s="DELETE FROM book WHERE title='nigga3'"
cur.execute(s)
mydb.commit()
# s="UPDATE book SET price=price+10 WHERE price>98"
# cur.execute(s)
# mydb.commit()
# cur = mydb.cursor()
# s="SELECT * from book"
# cur.execute(s)
# result = cur.fetchall()
# for rec in result:
#     print(rec)
#print(mydb.connection_id)
# cur = mydb.cursor()
# s="INSERT INTO book (bookid,title,price) VALUES(%s,%s,%s)"
# x = 1
# while True:
#     if x == 1:
#         row1=(int(input("id?:")),input("title?:"),input('price?:'))
#         cur.execute(s,row1)
#         mydb.commit()
#         x = int(input("Enter 1 to add more else 0"))
#     elif x == 0:
#         break
# s= "CREATE TABLE book(bookid integer(4),title varchar(20),price float(5,2))"
# cur.execute(s)
