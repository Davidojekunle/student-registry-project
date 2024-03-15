import tkinter as tk
from tkinter.ttk import Combobox
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
import re
import random
import sqlite3
import os
root = tk.Tk()
root.geometry('500x600')
root.title("Student  Management and Registration system")

bg_color = '#273b7a'
login_stud_icon = tk.PhotoImage(file='images/login_student_img.png')
login_admin_icon = tk.PhotoImage(file='images/admin_img.png')
add_icon = tk.PhotoImage(file='images/add_student_img.png')
lock_icon = tk.PhotoImage(file='images/locked.png')
unlocked_icon = tk.PhotoImage(file='images/unlocked.png')
add_studentimg = tk.PhotoImage(file='images/add_image.png')



def init_database():
   if os.path.exists('student_accounts.db'):

      connection = sqlite3.connect('student_accounts.db')
      cursor = connection.cursor()

      cursor.execute("""
      SELECT * FROM data
       """)
      
      connection.commit()
      print(cursor.fetchall())
      connection.close()
      
   else:
    connection = sqlite3.connect('student_accounts.db')

    cursor = connection.cursor()

    cursor.execute("""
   CREATE TABLE data (
   id_number text,
   password text,
   name text,
   age text,
   gender text,
   phone_number text,
   class text,
   email text,
   image blob
    )
    """)
   connection.commit()
   connection.close()


# def check_id_already_exists(id_number):
#    connection = sqlite3.connect('student_accounts.db')
#    cursor = connection.cursor()

#    cursor.execute(f"""
#    SELECT id_number FROM data WHERE id_number == '{id_number}'
#    """)

   # connection.commit()
   # response = cursor.fetchall()
   # connection.close()


def add_data(id_number, password, name, age, gender,
              phone_number, student_class, email, pic_data):
    
    connection = sqlite3.connect('student_accounts.db')
    cursor = connection.cursor()

    cursor.execute("""
    INSERT INTO data VALUES('{id_number}','{password}', '{name}','{age}', '{gender}','{phone_number}','{student_class}','{email}', ?)
   """, [pic_data])



    connection.commit()
    connection.close()

   

def confirmation_box(message):
   answer = tk.BooleanVar()
   answer.set(False)   

   def action(ans):
      answer.set(ans)
      confirmation_box_fn.destroy()
      
   confirmation_box_fn = tk.Frame(root, highlightbackground=bg_color, highlightthickness=3)
   confirmation_box_fn.place(x=100, y=120, width=320, height=220)

   message_lb = tk.Label(confirmation_box_fn, text=message, font=('Bold',15 ))
   message_lb.pack(pady=20)

   cancel_btn = tk.Button(confirmation_box_fn, text="Cancel", font=('Bold', 15), bd=0, bg=bg_color, fg='white', command=lambda: action(False))
   cancel_btn.place(x=50, y=160)

   yes_btn = tk.Button(confirmation_box_fn, text="Yes", font=('Bold', 15), bd=0, bg=bg_color, fg='white', command=lambda:action(True))
   yes_btn.place(x=190, y=160, width=80)

   
   root.wait_window(confirmation_box_fn)
   return answer.get()

def message_box(message):
   messageboxfr= tk.Frame(root, highlightbackground=bg_color, highlightthickness=3)
   messageboxfr.place(x=100, y=120, width=320, height=220)

   close_btn = tk.Button(messageboxfr, text='X', bd=0 , font=('Bold', 12),
                        fg=bg_color, command=lambda: messageboxfr.destroy())
   close_btn.place(x=290, y=5)
   
   messagelb =tk.Label(messageboxfr, text=message, font=('Bold', 15))
   messagelb.pack(pady=50)
   pass

def welcome_page():

    def switch_to_student_login():
       welcomepage_frame.destroy()
       root.update()
       student_login_page()
    def switch_to_admin_page():
       welcomepage_frame.destroy()
       admin_login_page()
    def switch_to_addpage():
       welcomepage_frame.destroy()
       root.update()
       add_account_page()
    welcomepage_frame = tk.Frame(root, highlightbackground=bg_color,highlightthickness=4 )
    heading = tk.Label(welcomepage_frame, 
                    text='Welcome to Student Registration & \n Mangament System',
                    bg=bg_color, fg='white', font=('Bold', 18))
    heading.place(x=0, y=0, width=400)

    stu_login_button  = tk.Button(welcomepage_frame, text='login Student', bg =bg_color , fg='white', font=('Bold', 15), bd=0, command= switch_to_student_login)
    stu_login_button.place(x=120, y=125, width=200)
    stu_login_img  = tk.Button(welcomepage_frame,image=login_stud_icon,  bd=0)
    stu_login_img.place(x=60, y=100)

    admin_login_button  = tk.Button(welcomepage_frame, text='login Admin', bg =bg_color , fg='white', font=('Bold', 15), bd=0, command= switch_to_admin_page)
    admin_login_button.place(x=120, y=225, width=200)
    admin_login_img  = tk.Button(welcomepage_frame,image=login_admin_icon,  bd=0)
    admin_login_img.place(x=60, y=200)

    add_button  = tk.Button(welcomepage_frame, text='New Student', bg =bg_color , fg='white', font=('Bold', 15), bd=0, command=switch_to_addpage)
    add_button.place(x=120, y=325, width=200)

    add_img  = tk.Button(welcomepage_frame,image=add_icon,  bd=0)
    add_img.place(x=60, y=300)

    welcomepage_frame.pack(pady=30)
    welcomepage_frame.pack_propagate(False) 
    welcomepage_frame.configure(width=400,height=420)

def student_login_page():
    def show_hide_password():
      if spassword_entry['show'] == "*":
        spassword_entry.config(show='')
        show_hide_btn.config(image=unlocked_icon)
      else:
        spassword_entry.config(show="*")
        show_hide_btn.config(image=lock_icon)
    def swtich_to_welcomepage():
       studentloginpage_frame.destroy()
       welcome_page()
    
    studentloginpage_frame = tk.Frame(root,highlightbackground=bg_color, 
                                    highlightthickness=3)

    head = tk.Label(studentloginpage_frame, text="Student Login Page", bg=bg_color,fg='white', font=('Bold', 18))
    head.place(x=0, y=0, width=400)

    back_button = tk.Button(studentloginpage_frame,  text='🔙', font=('Bold', 20), fg=bg_color, bd=0, command=swtich_to_welcomepage )
    back_button.place(x=5, y=40)
    student_iconlb = tk.Label(studentloginpage_frame, image=login_stud_icon) 
    student_iconlb.place(x=150, y=40)

    id_number_lb = tk.Label(studentloginpage_frame, text='Enter Student ID Number', font=('Bold', 15), fg=bg_color)
    id_number_lb.place(x=80, y=140)
 
    id_number_entry = tk.Entry(studentloginpage_frame, font=('Bold', 15),
                            justify=tk.CENTER, highlightcolor=bg_color,
                            highlightbackground='gray', highlightthickness=2)
    id_number_entry.place(x=80, y=190)

    spassword_lb = tk.Label(studentloginpage_frame, text='Enter Student Password', font=('Bold', 15), fg=bg_color)
    spassword_lb.place(x=80, y=240)

    spassword_entry = tk.Entry(studentloginpage_frame, font=('Bold', 15),
                            justify=tk.CENTER, highlightcolor=bg_color,
                            highlightbackground='gray', highlightthickness=2,show="*" )
    spassword_entry.place(x=80, y=290)
    show_hide_btn = tk.Button(studentloginpage_frame, image=lock_icon , bd=0, command=show_hide_password)
    show_hide_btn.place(x=310, y=280)
    login_btn = tk.Button(studentloginpage_frame, text="Login", font=('Bold', 15), bg=bg_color, fg='white')
    login_btn.place(x=95, y=340, width=200, height=40)

    forgetpassword_btn = tk.Button(studentloginpage_frame, text="⚠️\n Forgotten Password", fg=bg_color, bd=0)
    forgetpassword_btn.place(x=150, y=390)
    studentloginpage_frame.pack(pady=30)
    studentloginpage_frame.pack_propagate(False) 
    studentloginpage_frame.configure(width=400,height=450)
def admin_login_page():
    def show_hide_password():
        if spassword_entry['show'] == "*":
            spassword_entry.config(show='')
            show_hide_btn.config(image=unlocked_icon)
        else:
            spassword_entry.config(show="*")
            show_hide_btn.config(image=lock_icon)
    def switch_to_welcomescreen():
       adminlogin_page_frame.destroy()
       welcome_page()

    adminlogin_page_frame= tk.Frame(root,highlightbackground=bg_color, 
                                        highlightthickness=3)
    back_button = tk.Button(adminlogin_page_frame,  text='🔙', font=('Bold', 20), fg=bg_color, bd=0, command=switch_to_welcomescreen )
    back_button.place(x=5, y=40)

    header = tk.Label(adminlogin_page_frame, text="Admin login Page", bg=bg_color,fg='white', font=('Bold', 18))
    header.place(x=0, y=0, width=400)

    admin_icon_lb = tk.Label(adminlogin_page_frame, image=login_admin_icon)
    admin_icon_lb.place(x=150, y=40)

    id_number_lb = tk.Label(adminlogin_page_frame, text='Enter Admin User Name', font=('Bold', 15), fg=bg_color)
    id_number_lb.place(x=80, y=140)

    id_number_entry = tk.Entry(adminlogin_page_frame, font=('Bold', 15),
                            justify=tk.CENTER, highlightcolor=bg_color,
                            highlightbackground='gray', highlightthickness=2)
    id_number_entry.place(x=80, y=190)

    spassword_lb = tk.Label(adminlogin_page_frame, text='Enter  Password', font=('Bold', 15), fg=bg_color)
    spassword_lb.place(x=80, y=240)

    spassword_entry = tk.Entry(adminlogin_page_frame, font=('Bold', 15),
                            justify=tk.CENTER, highlightcolor=bg_color,
                            highlightbackground='gray', highlightthickness=2,show="*" )
    spassword_entry.place(x=80, y=290)
    show_hide_btn = tk.Button(adminlogin_page_frame, image=lock_icon , bd=0, command=show_hide_password)
    show_hide_btn.place(x=310, y=280)
    login_btn = tk.Button(adminlogin_page_frame, text="Login", font=('Bold', 15), bg=bg_color, fg='white')
    login_btn.place(x=95, y=340, width=200, height=40)

    adminlogin_page_frame.pack(pady=30)
    adminlogin_page_frame.pack_propagate(False)
    adminlogin_page_frame.configure(width=400 , height=430)

student_gender = tk.StringVar()
class_list = ['JSS1', 'JSS2', 'JSS3', 'SS1', 'SS2', 'SS3']
def add_account_page():
    pic_path = tk.StringVar()
    pic_path.set('')
    add_account_page_frame = tk.Frame(root,highlightbackground=bg_color, 
                                            highlightthickness=3)


    def open_pic():
       path = askopenfilename()

       if path:
         img = ImageTk.PhotoImage(Image.open(path).resize((100, 100)))
         pic_path.set(path)
         add_pic_button.config(image=img)
         add_pic_button.image = img


    

    def switch_to_welcome():

        ans = confirmation_box(message="Do You Want To \n Leave \n Registration Form")
        if ans:
            add_account_page_frame.destroy()
            root.update()
            welcome_page()

    def remove_highlght(entry):
       if entry ['highlightbackground']  != 'gray':
          if entry.get() != '':
             entry.config(highlightcolor=bg_color,highlightbackground ='gray' )
       

    def check_invalid_email(email):
        pattern =  "^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$'"
        match = re.match(pattern=pattern, string=email)
        return match
    def generate_id_number():
       generate_id = ''

       for r in range(4):
          generate_id += str(random.randint(0, 9))

      #  check_id_already_exists(id_number=generate_id)
      #  print('id number;', generate_id)

       username= "fstc"+generate_id
       student_id.config(state=tk.NORMAL)
       student_id.delete(0, tk.END)
       student_id.insert(tk.END, username)
       student_id.config(state='readonly')
       

       
       
    def check_input_validation():
       if student_name_entry.get() =='':
          student_name_entry.configure(highlightcolor='red', highlightbackground='red')
          student_name_entry.focus()
          message_box(message="Student full name is Required")

       elif student_age_ent.get() =='':
          student_age_ent.config(highlightcolor='red',highlightbackground='red' )
          student_age_ent.get()
          message_box(message="Student Age is Required")

       elif student_contactentry.get() =='':
          student_contactentry.config(highlightcolor='red',highlightbackground='red' )
          student_contactentry.get()
          message_box(message="Student Contact is Required")

       elif student_classbtn.get() =='':
          
          student_classbtn.get()
          message_box(message="Select Student Class")
          

       elif student_emailentry.get() =='':
          student_emailentry.config(highlightcolor='red',highlightbackground='red' )
          student_name_entry.focus()
          
          message_box(message="Student Email is Required")

      #  elif not check_invalid_email(student_name_entry.get().lower()):
      #      print(student_emailentry.get())
      #      student_emailentry.config(highlightcolor='red',
      #                                highlightbackground='red' )
      #      student_name_entry.focus()
           


       elif account_passwordentry.get() == '':
          account_passwordentry. cofig(highlightcolor='red', highlightbackground= 'red')
          account_passwordentry.get()
          message_box(message="Password is Required")

       else:
          pic_data = b''

          if pic_path.get() != '':
             resize = Image.open(pic_path.get()).resize((100,100))
             resize.save('temo_pic.png')

             read_data = open('temo_pic.png', 'rb')
             pic_data= read_data.read()
             read_data.close()

          else:
             read_data = open('images/add_student_img.png', 'rb')
             pic_data =read_data.read()
             read_data.close()

          add_data(id_number=student_id.get(),
                   password=account_passwordentry.get(),
                   name= student_name_entry.get(),
                   age= student_age_ent.get(),
                   gender=student_gender.get(),
                   phone_number=student_contactentry.get(),
                   student_class=student_classbtn.get(),
                   email=student_emailentry.get(),
                   pic_data=pic_data)
          message_box("Account Successfully Created")
       

    add_pic_frame = tk.Frame(add_account_page_frame, highlightbackground=bg_color, highlightthickness=2)
    add_pic_button = tk.Button(add_pic_frame, image=add_studentimg, bd=0, command=open_pic)
    add_pic_button.pack()
    add_pic_frame.place(x=5, y=5, width=105, height=105)
    student_namelb = tk.Label(add_account_page_frame, text="Enter  Full Name. ", font=('Bold', 12))
    student_namelb.place(x=5, y=130)


    student_name_entry = tk.Entry(add_account_page_frame,font=('Bold', 15),
                                highlightcolor=bg_color, highlightbackground='grey',
                                    highlightthickness=2 )
    student_name_entry.place(x=5, y=150, width=180)
    student_name_entry.bind('<KeyRelease>', 
                            lambda e: remove_highlght(entry=student_name_entry))
    

    student_genderlb = tk.Label(add_account_page_frame, text='Select Student Gender', font=('Bold',
                                                                                            
                                                                                             12))
    student_genderlb.place(x=5, y=210)
    male_btn = tk.Radiobutton(add_account_page_frame, text='Male', font=('Bold', 12), variable=student_gender, value='male')
    male_btn.place(x=5, y=235)

    female_btn = tk.Radiobutton(add_account_page_frame, text='Female', font=('Bold', 12), variable=student_gender, value='female')
    female_btn.place(x=75, y=235)

    student_gender.set('male')

    student_agelb = tk.Label(add_account_page_frame, text='Enter Student Age', font=('Bold', 12))
    student_agelb.place(x=5, y=280)
    

    student_age_ent = tk.Entry(add_account_page_frame, font=('Bold', 15), highlightcolor=bg_color, highlightbackground='gray', highlightthickness=2)
    student_age_ent.place(x=5, y=305, width=180)
    student_age_ent.bind('<KeyRelease>', 
                            lambda e: remove_highlght(entry=student_age_ent))

    student_contactlb = tk.Label(add_account_page_frame, text='Enter Contact Phone Number', font=('Bold', 12))
    student_contactlb.place(x=5, y=360)
    

    student_contactentry = tk.Entry(add_account_page_frame,font=('Bold', 15), highlightcolor=bg_color, highlightbackground='gray', highlightthickness=2 )
    student_contactentry.place(x=5, y=385, width=180)
    student_contactentry.bind('<KeyRelease>', 
                            lambda e: remove_highlght(entry=student_contactentry))

    student_classlb = tk.Label(add_account_page_frame, text='Select Student Class', font=('Bold', 12))
    student_classlb.place(x=5, y=440)

    student_classbtn = Combobox(add_account_page_frame, font=('Bold', 15), state='readonly', values=class_list)
    student_classbtn.place(x=5, y=475, width=180, height=30)
    student_classbtn.bind('<KeyRelease>', 
                            lambda e: remove_highlght(entry=student_classbtn))

    student_idlb = tk.Label(add_account_page_frame, text='Student ID Number', font=('Bold', 12),bd=0 )
    student_idlb.place(x=240, y=35)

    student_id = tk.Entry(add_account_page_frame, font=('Bold', 14), width=60)
    student_id.place(x=380, y=35, width=80)
    student_id.insert(tk.END, 'fstca345')
    student_id. configure(state='readonly')

    generate_id_number()

    id_infolb = tk.Label(add_account_page_frame, text="""Automatically Generate ID Number 
                ! Remember using this ID number
                    Student will login Account """, justify=tk.LEFT)
    id_infolb.place(x=240, y=65)

    student_emaillb = tk.Label(add_account_page_frame, text='Enter Student Email', font=('Bold', 12))
    student_emaillb.place(x=240, y=130)

    email_infolb = tk.Label(add_account_page_frame, text="""Via Email Address Student
    Can Recover
    ! In Case Forgetting Passowrd And Also
    Student will get Fututre Notifications""", justify=tk.LEFT)
    email_infolb.place(x=240, y=200)


    student_emailentry = tk.Entry(add_account_page_frame,font=('Bold', 15), highlightcolor=bg_color, highlightbackground='gray', highlightthickness=2 )
    student_emailentry.place(x=240, y=160, width=180)
    student_emailentry.bind('<KeyRelease>', 
                            lambda e: remove_highlght(entry=student_emailentry))

    account_passwordlb = tk.Label(add_account_page_frame,text='Create Account Passowrd', font=('Bold', 12))
    account_passwordlb.place(x=240,y=275)


    account_passwordentry = tk.Entry(add_account_page_frame,font=('Bold', 15), highlightcolor=bg_color, highlightbackground='gray', highlightthickness=2 )
    account_passwordentry.place(x=240, y=307, width=180)
    account_passwordentry.bind('<KeyRelease>' ,
                               lambda e: remove_highlght(entry=account_passwordentry))

    passwordinfolb = tk.Label(add_account_page_frame, text="""Via Student Created Password
    And Provided  Student ID Number
    Student Can Login Account""", justify=tk.LEFT)
    passwordinfolb.place(x=240, y=345)

    home_button = tk.Button(add_account_page_frame, text='Home',font=('Bold' ,15), bg='red', fg='white', bd=0, command=switch_to_welcome)
    home_button.place(x=240, y=420)

    submit_button = tk.Button(add_account_page_frame, text='Submit',font=('Bold' ,15), bg=bg_color, fg='white', bd=0, command=check_input_validation)
    submit_button.place(x=360, y=420)

    add_account_page_frame.pack(pady=5)
    add_account_page_frame.pack_propagate(False)
    add_account_page_frame.configure(width=480, height=580)
init_database()
add_account_page()

root.mainloop()





