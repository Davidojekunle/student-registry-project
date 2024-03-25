import tkinter as tk
from tkinter.ttk import Combobox, Treeview
from tkinter.filedialog import askopenfilename, askdirectory
from PIL import Image, ImageTk, ImageDraw, ImageFont, ImageOps
from io import BytesIO
import re
import random
import sqlite3
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import my_email

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

def check_id_already_exists(id_number):
    connection = sqlite3.connect('student_accounts.db')
    cursor = connection.cursor()

    cursor.execute(f"""
   SELECT id_number FROM data WHERE id_number == '{id_number}'
   """)

    connection.commit()
    response = cursor.fetchall()
    connection.close()

    return response


def check_valid_password(id_number, password):
    connection = sqlite3.connect('student_accounts.db')
    cursor = connection.cursor()

    cursor.execute(f"""
   SELECT id_number,password FROM data WHERE id_number == '{id_number}' AND password == '{password}'
   """)

    connection.commit()
    response = cursor.fetchall()
    connection.close()

    return response


def add_data(id_number, password, name, age, gender,
              phone_number, student_class, email, pic_data):
    
    connection = sqlite3.connect('student_accounts.db')
    cursor = connection.cursor()

    cursor.execute(f"""
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


def draw_student_card(studentpicpath, student_data):
  labels = '''
  ID :  
  Name:
  Gender:
  Age:
  Class:
  Contact:
  Email:
  '''
  
  student_card = Image.open('images/student_card_frame.png')
  pic =Image.open(studentpicpath).resize((100, 100))

  student_card.paste(pic, (15, 25))

  draw = ImageDraw.Draw(student_card)
  heading_font = ImageFont.truetype('bahnschrift', 18)
  labels_font = ImageFont.truetype('arial', 15)
  data_font = ImageFont.truetype('bahnschrift', 13)
  draw.text(xy=(150, 60), text='Student Card', fill=(0,0, 0), font=heading_font)

  draw.multiline_text(xy=(15,120), text=labels, fill=(0,0,0),font=labels_font ,spacing=6)
  draw.multiline_text(xy=(95,120), text=student_data,fill=(0,0,0), 
                      font=data_font, spacing= 10) 
  return student_card
  
def student_cardd(student_carb_obj, bypass_login_page= False):
   def save_student_card():
      path = askdirectory()

      if path:
         

         student_carb_obj.save(f'{path}/studnet_card.png')
   def close_cmd():
      student_cardpage_fn.destroy()
      if not bypass_login_page:
         root.update()
         student_login_page()
       
   student_card_Image = ImageTk.PhotoImage(student_carb_obj)
   student_cardpage_fn = tk.Frame(root, highlightbackground=bg_color, highlightthickness=3)

   headinglb = tk.Label(student_cardpage_fn, text='Student Card', bg=bg_color, fg='white', font=('Bold', 15))
   headinglb.place(x=0, y=0 , width=400)

   closebtn = tk.Button(student_cardpage_fn, text='X', bg=bg_color, fg='white', font=('Bold', 13), bd=0,
                        command=close_cmd)
   closebtn.place(x=370, y=0)
   
   
   

   student_cardlb =tk.Label(student_cardpage_fn, image=student_card_Image)
   student_cardlb.image = student_card_Image
   
   student_cardlb.place(x=50,y=50)



   save_student_card_btn = tk.Button(student_cardpage_fn, text='Save Student Card',
                                     bg=bg_color, fg='white', font=('Bold', 15), bd=1, 
                                      command=save_student_card )
   
   save_student_card_btn.place(x=80, y=375)

   print_student_card_btn = tk.Button(student_cardpage_fn, text='🖨️',
                                     bg=bg_color, fg='white', font=('Bold', 18), bd=1 )
   
   print_student_card_btn.place(x=270, y=375)




   student_cardpage_fn.place(x=50, y=30, width=400, height=450)
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

def sendmail_to_student(email, message, subject, file_data=None):
   smtp_server = 'smtp.gmail.com'
   smtp_port = 587

   username =my_email.email_address
   password =my_email.password

   msg = MIMEMultipart()

   msg['Subject'] = subject
   msg['From'] = message
   msg['To'] = email

   msg.attach(MIMEText(_text=message, _subtype= 'html'))
   if file_data:
        attachment = MIMEBase('application', 'octet-stream')
        attachment.set_payload(file_data)
        encoders.encode_base64(attachment)
        attachment.add_header('Content-Disposition', 'attachment', filename='file.pdf')
        msg.attach(attachment)

   smtp_connection = smtplib.SMTP(host=smtp_server, port=smtp_port)
   smtp_connection.starttls()
   smtp_connection.login(user=username, password=password)
   smtp_connection.sendmail(from_addr=username, to_addrs=email, msg=msg.as_string())
   



   pass

def forgetpassword_page():

   def recover_password():
      if check_id_already_exists(id_number=student_ident.get()):
         
         connection = sqlite3.connect('student_accounts.db')
         cursor = connection.cursor()

         cursor.execute(f"""
         SELECT password FROM data WHERE id_number =='{student_ident.get()}'
                        """)


         connection.commit()

         recovered_password = cursor.fetchall()[0][0]
         

         cursor.execute(f"""
         SELECT email FROM data WHERE id_number =='{student_ident.get()}'
                        """)
         connection.commit()

         semail = cursor.fetchall()[0][0]
        

         connection.close()

         confirmation =confirmation_box(message=f""" we will send \n your forgotten password
 via this Email Address:
{semail}
Do you want to continue?""")
         if confirmation:
            msg = f'''<h1> Your forgotten password is: </h1>
            <h2>{recovered_password}</h2>'''
            sendmail_to_student(email=semail, message=msg, subject='password reovery')
      else:
         
         message_box(message='Incorrect Student ID')
         

   forgetpassword_page_fr =tk.Frame(root, highlightbackground=bg_color, highlightthickness=2)
   forgetpassword_page_fr.place(x=75, y=120, width=350, height=250)

   heading_lb =tk.Label(forgetpassword_page_fr, text= '⚠️ Bitch, Forgotten Password?', font=('Bold', 15), bg=bg_color, fg='white')
   heading_lb.place(x=0, y=0, width=350)


   close_btn = tk.Button(forgetpassword_page_fr, text='X',
                         font=('Bold', 13), bg=bg_color, fg='white',bd= 0 , command= lambda: forgetpassword_page_fr.destroy())
   close_btn.place(x=320 ,y=0)
   
   student_idlb =tk.Label(forgetpassword_page_fr, text='Enter Student ID Number', font=('Bold', 13))
   student_idlb.place(x=70, y=40)
   student_ident = tk.Entry(forgetpassword_page_fr, font=('Bold', 15), justify=tk.CENTER)
   student_ident.place(x=70, y=70, width=180)
   
   info_lb = tk.Label(forgetpassword_page_fr,                      
text='''Via Email Address
We will Send You 
Your Forgotten Password
''', justify=tk.LEFT)   
   info_lb.place(x=75, y=110)
   next_btn = tk.Button(forgetpassword_page_fr, text='Next', font=('Bold', 13),
                         bg=bg_color,fg='white', command=recover_password)
   next_btn.place(x=130, y=200, width=80)

def  fectch_student_data(query):
   connection = sqlite3.connect('student_accounts.db')
   cursor = connection.cursor()

   cursor.execute(query)

   connection.commit()
   response = cursor.fetchall()
   connection.close()

   return response


def student_dashboard(student_id):
   get_student_details = fectch_student_data(f"""
SELECT name , age , gender, class, phone_number, email FROM data WHERE id_number =='{student_id}'""")
   print(get_student_details)

   get_student_pic = fectch_student_data(f"""
SELECT image FROM data WHERE id_number =='{student_id}'""")
   student_pic = BytesIO(get_student_pic[0][0])
   

   def logout():
       confirm = confirmation_box('Are you sure you want to log out')
       if confirm:
          dashboard_fm.destroy()
          welcome_page()
          root.update()
   def switch(indicator, page):
      home_btn_indicator.config(bg='#c3c3c3')
      student_card_btn_indicator.config(bg='#c3c3c3')
      security_btn_indicator.config(bg='#c3c3c3')
      edit_data_btn_indicator.config(bg='#c3c3c3')

      indicator.config(bg= bg_color)
      for  i  in pages_fm.winfo_children():
         i.destroy()
         root.update()
          

      page()



   dashboard_fm = tk.Frame(root, highlightbackground=bg_color, highlightthickness=3)
   def home_page():
      student_pic_image_obj = Image.open(student_pic)
      size = 100
      mask = Image.new(mode='L', size=(size, size))

      draw_circle = ImageDraw.Draw(im=mask)
      draw_circle.ellipse(xy=(0,0, size, size), fill=255)

      output = ImageOps.fit(image=student_pic_image_obj, size=mask.size,
                            centering=(1,1))
      
      output.putalpha(mask)
      
      student_picture = ImageTk.PhotoImage(output)

      home_page_fm = tk.Frame(pages_fm)

      student_pic_lb = tk.Label(home_page_fm, image=student_picture)
      student_pic_lb.image  = student_picture
      student_pic_lb.place(x=10, y=10)

      hi_lb = tk.Label(home_page_fm, text=f'Welcome {get_student_details[0][0]}', 
                       font=('Bold', 15))
      hi_lb.place(x=130, y=50)

      student_details =f"""
STUDENT ID: {student_id}\n
Name: {get_student_details[0][0]}\n
Age:{get_student_details[0][1]}\n
Gender: {get_student_details[0][2]}\n
Class: {get_student_details[0][3]}\n
Contact: {get_student_details[0][4]}\n
Email: {get_student_details[0][5]}\n
"""
      student_details_lb = tk.Label(home_page_fm, text=student_details,
                                    font=('Bold', 13), justify=tk.LEFT)
      student_details_lb.place(x=20,y=130)
     
      home_page_fm.pack(fill=tk.BOTH, expand=True)
   

   def student_card_page():
      def save_student_card():
       path = askdirectory()

       if path:
         student_card_image_obj.save(f'{path}/student_card.png')


      student_card_fm = tk.Frame(pages_fm)

      student_details =f"""
{student_id}
{get_student_details[0][0]}
{get_student_details[0][2]}
{get_student_details[0][1]}
{get_student_details[0][3]}
{get_student_details[0][4]}
{get_student_details[0][5]}
"""
      student_card_image_obj = draw_student_card(studentpicpath=student_pic,
                                                 student_data=student_details)
      student_card_img  =ImageTk.PhotoImage(student_card_image_obj)
      cardlb = tk.Label(student_card_fm, image=student_card_img)
      cardlb.image = student_card_img
      cardlb.place(x=20, y=50)








      
      
      save_student_card_btn = tk.Button(student_card_fm, text= 'Save Student Card',font=('Bold', 15),
                                        bd=1, fg= 'white', bg=bg_color, command=save_student_card )
      save_student_card_btn.place(x=80, y=400)
      
      student_card_fm.pack(fill=tk.BOTH, expand=True)
   
   def security_page():    
          def show_hide_password():
            if current_passwordent['show'] == "*":
               current_passwordent.config(show='')
               show_hide_btn.config(image=unlocked_icon)
            
            else:
              current_passwordent.config(show="*")
              show_hide_btn.config(image=lock_icon)
              
      
          security_page_fm = tk.Frame(pages_fm)
          current_passwordlb = tk.Label(security_page_fm, text='Your current password',
                                       font=('Bold',15))
          current_passwordlb.place(x=80, y=30)

          current_passwordent = tk.Entry(security_page_fm, font=('Bold', 15),
                                        justify=tk.CENTER, show='*')
          current_passwordent.place(x=50, y=80)
          def check_pass():
            if spass != current_passwordent.get():
               message_box('wrong password')


          current_password =fectch_student_data(f"SELECT password FROM data WHERE id_number== '{student_id}'")
          spass = current_password[0][0]
          
          def check_pass():
            if spass != current_passwordent.get():
               message_box('wrong password')

            else:
               if new_passwordent.get() != '':
                  confirm  = confirmation_box('Do you want to change \n ypur password')
                  if confirm:
                     connection = sqlite3.connect('student_accounts.db')
                     cursor = connection.cursor()
                     cursor.execute(f"""UPDATE data SET password = '{new_passwordent.get()}'
                                     WHERE id_number =='{student_id}'""")

                     connection.commit()
                     connection.close()
  
                     message_box("You have successfuly changed\n your password")
                     current_passwordent.delete(0, tk.END)
                     new_passwordent.delete(0, tk.END)
                      

               else:
                  message_box('Enter new Password')
             
          
          show_hide_btn = tk.Button(security_page_fm, image=lock_icon, bd=0,
                                    command=show_hide_password)
          show_hide_btn.place(x=280, y=70)

          new_passwordlb = tk.Label(security_page_fm, text='Set New password',
                                    font=('Bold', 12))
          new_passwordlb.place(x=100, y=140)


          new_passwordent = tk.Entry(security_page_fm,font=('Bold', 15), 
                                     justify=tk.CENTER)
          new_passwordent.place(x=50, y=180)

          change_psssword_btn = tk.Button(security_page_fm, text="change password",
                                          font=('Bold', 15), command=check_pass)
          change_psssword_btn.place(x=30, y=250,width=290)
          
          security_page_fm.pack(fill=tk.BOTH, expand=True)



   def edit_data_page():
         def check_input():
            nonlocal get_student_details,  student_pic

            if student_name_entry.get() == '':
              message_box('Stuent Full name is required')

            elif student_contactentry.get() =='':
               message_box('Student Contact Entry is Required')

            elif student_emailentry.get() == '':
               message_box("Studnet Email Address is Required")
            else:
               if pic_path.get() != '':
                  new_student_pic = Image.open(pic_path.get()).resize((100,100))
                  new_student_pic.save('temp_pic.png')

                  with open('temp_pic.png', 'rb') as read_new_pic:
                     new_picture_binary = read_new_pic.read()
                     read_new_pic.close()

                     connection = sqlite3.connect('student_accounts.db')
                     cursor = connection.cursor()

                     cursor.execute(f"UPDATE data SET image=? WHERE id_number =='{student_id}' ",
                                   [new_picture_binary] )
                     
                     connection.commit()
                     connection.close()
                     get_student_details = fectch_student_data(f"""
SELECT name , age , gender, class, phone_number, email FROM data WHERE id_number =='{student_id}'""")
                     print(get_student_details)

                     get_student_pic = fectch_student_data(f"""
SELECT image FROM data WHERE id_number =='{student_id}'""")
                     student_pic = BytesIO(get_student_pic[0][0])
                     message_box('Data successfully updated')

               name = student_name_entry.get()
               email = student_emailentry.get()
               contact_number = student_contactentry.get()
               connection = sqlite3.connect('student_accounts.db')
               cursor = connection.cursor()
               cursor.execute(f"""
UPDATE data SET name='{name}', email='{email}', phone_number='{contact_number}' WHERE id_number =='{student_id}'
""") 
               
               connection.commit()
               connection.close()
               message_box('Data sucessfully Updated')

         
         pic_path = tk.StringVar()


         pic_path.set('')

         def open_pic():
            path = askopenfilename()


            if path:
               img = ImageTk.PhotoImage(Image.open(path).resize((100, 100)))
               pic_path.set(path)
               add_pic_button.config(image=img)
               add_pic_button.image = img


         student_current_pic = ImageTk.PhotoImage(Image.open(student_pic))
      
         edit_data_page = tk.Frame(pages_fm)

         add_pic_frame = tk.Frame(edit_data_page, highlightbackground=bg_color, highlightthickness=2)
         add_pic_button = tk.Button(add_pic_frame, image=student_current_pic, bd=0, command=open_pic)
         add_pic_button.image = student_current_pic
         add_pic_button.pack()
         student_namelb = tk.Label(edit_data_page, text="student Full Name. ", font=('Bold', 12))
         student_namelb.place(x=5, y=130)


         student_name_entry = tk.Entry(edit_data_page,font=('Bold', 15),
                                highlightcolor=bg_color, highlightbackground='grey',
                                    highlightthickness=2 )
         student_name_entry.place(x=5, y=150, width=180)
         student_name_entry.insert(tk.END, get_student_details[0][0])


         student_contactlb = tk.Label(edit_data_page, text=' Contact Phone Number', font=('Bold', 12))
         student_contactlb.place(x=5, y=210)
    

         student_contactentry = tk.Entry(edit_data_page,font=('Bold', 15), highlightcolor=bg_color, highlightbackground='gray', highlightthickness=2 )
         student_contactentry.place(x=5, y=235, width=180)
         student_contactentry.insert(tk.END, get_student_details[0][4])
         


         student_emaillb = tk.Label(edit_data_page, text='Student Email', font=('Bold', 12))
         student_emaillb.place(x=5, y=280)
         student_emailentry = tk.Entry(edit_data_page,font=('Bold', 15), highlightcolor=bg_color, highlightbackground='gray', highlightthickness=2 )
         student_emailentry.place(x=5, y=305, width=180)
         student_emailentry.insert(tk.END, get_student_details[0][5])

         update_data_button = tk.Button(edit_data_page, text='Update',font=('Bold',15),
                                        fg='white', bg=bg_color , bd=0 , command=check_input)
         
         update_data_button.place(x=80, y=470, width= 180)
         

         add_pic_frame.place(x=5, y=5, width=105, height=105)
         edit_data_page.pack(fill=tk.BOTH, expand=True)

   


   options_fm =tk.Frame(dashboard_fm, highlightbackground=bg_color,
                         highlightthickness=2, bg='#c3c3c3')
   

   pages_fm = tk.Frame(dashboard_fm, bg='gray')
   pages_fm.place(x=122, y=5, width=350, height=550)
   home_page()

   

   home_btn = tk.Button(options_fm, text='Home', font=('Bold', 15),
                         bg='#c3c3c3', fg=bg_color, bd=0, command=lambda: switch(indicator=home_btn_indicator, page=home_page))
   home_btn.place(x=10, y=50)

   home_btn_indicator = tk.Label(options_fm, bg=bg_color)
   home_btn_indicator.place(x=5, y=48, width=3, height=40)


   student_card_btn = tk.Button(options_fm, text='Student\n Card', font=('Bold', 15),
                         bg='#c3c3c3', fg=bg_color, bd=0, justify=tk.LEFT, command=lambda: switch(indicator=student_card_btn_indicator,
                                                                                                   page=student_card_page))
   student_card_btn.place(x=10, y=100)

   student_card_btn_indicator = tk.Label(options_fm, bg='#c3c3c3')
   student_card_btn_indicator.place(x=5, y=100, width=3, height=40)

   security_btn = tk.Button(options_fm, text='Security', font=('Bold', 15),
                         bg='#c3c3c3', fg=bg_color, bd=0,
                         command=lambda: switch(indicator=security_btn_indicator,
                                                 page=security_page))
   security_btn.place(x=10, y=170)

   security_btn_indicator = tk.Label(options_fm, bg='#c3c3c3')
   security_btn_indicator.place(x=5, y=170, width=3, height=40)

   edit_data_btn = tk.Button(options_fm, text='Edit Data', font=('Bold', 15),
                         bg='#c3c3c3', fg=bg_color, bd=0,
                         command=lambda: switch(indicator=edit_data_btn_indicator
                                                ,page=edit_data_page))
   edit_data_btn.place(x=10, y=220)

   edit_data_btn_indicator = tk.Label(options_fm, bg='#c3c3c3')
   edit_data_btn_indicator.place(x=5, y=220, width=3, height=40)

   logout_btn = tk.Button(options_fm, text='Logout', font=('Bold', 15),
                         bg='#c3c3c3', fg=bg_color, bd=0, command=logout)
   logout_btn.place(x=10, y=500)

   







   options_fm.place(x=0, y=0, width= 120, height=575)


   dashboard_fm.pack(pady=5)
   dashboard_fm.propagate(False)
   dashboard_fm.configure(width=480, height=580)
def student_login_page():
    
    
    def remove_highlght(entry):
       if entry ['highlightbackground']  != 'gray':
          if entry.get() != '':
             entry.config(highlightcolor=bg_color,highlightbackground ='gray')
             
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


    def login_account():
       verify_idnumber = check_id_already_exists(id_number=id_number_entry.get())
       if verify_idnumber:
          
          verify_password = check_valid_password(id_number=id_number_entry.get(),
                                                 password=spassword_entry.get())
          if verify_password:
              id_number = id_number_entry.get()
              print('Password is correct')
              studentloginpage_frame.destroy()
              student_dashboard(student_id=id_number)
              root.update()
              


          else:
              
              spassword_entry.config(highlightcolor='red',
                                    highlightbackground='red')
              message_box(message='Incorrect password')
       

          
       else:
          
          id_number_entry.config(highlightcolor='red',highlightbackground ='red' )
          message_box(message='Please into a valid ID')
           

   

        
         #  else:
         #  id_number_entry.configure(highlightcolor='red', highlightbackground='red')
         #  id_number_entry.focus()

         #  message_box(message="Invalid user_name")
         #  print('invalid')
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
    id_number_entry.bind('<KeyRelease>',
                          lambda e: remove_highlght(entry=id_number_entry))

    spassword_lb = tk.Label(studentloginpage_frame, text='Enter Student Password', font=('Bold', 15), fg=bg_color)
    
    spassword_lb.place(x=80, y=240)

    spassword_entry = tk.Entry(studentloginpage_frame, font=('Bold', 15),
                            justify=tk.CENTER, highlightcolor=bg_color,
                            highlightbackground='gray', highlightthickness=2,show="*" )
    spassword_entry.place(x=80, y=290)
    spassword_entry.bind('<KeyRelease>',
                          lambda e: remove_highlght(entry=spassword_entry))
    show_hide_btn = tk.Button(studentloginpage_frame, image=lock_icon , bd=0, command=show_hide_password)
    show_hide_btn.place(x=310, y=280)
    login_btn = tk.Button(studentloginpage_frame, text="Login", font=('Bold', 15), bg=bg_color, fg='white', command=login_account)
    login_btn.place(x=95, y=340, width=200, height=40) 

    forgetpassword_btn = tk.Button(studentloginpage_frame, text="⚠️\n Forgotten Password", fg=bg_color, bd=0, command = forgetpassword_page)
    forgetpassword_btn.place(x=150, y=390)
    studentloginpage_frame.pack(pady=30)
    studentloginpage_frame.pack_propagate(False) 
    studentloginpage_frame.configure(width=400,height=450)

def admin_dashboard():
   

   def switch(indicator, page):
         home_btn_indicator.config(bg='#c3c3c3')
         find_student_btn_indicator.config(bg='#c3c3c3')
         announcement_btn_indicator.config(bg='#c3c3c3')
         send_results_btn_indicator.config(bg='#c3c3c3')
         indicator.config(bg=bg_color)
         for  i  in pages_fm.winfo_children():
           i.destroy()
         root.update()
          

         page()
        
   
   def logout():
       confirm = confirmation_box('Are you sure you want to log out')
       if confirm:
          dashboard_fm.destroy()
          welcome_page()
          root.update()

   def home_page():
      home_page_fm = tk.Frame(pages_fm)

      admin_icon_lb = tk.Label(home_page_fm, image=login_admin_icon)
      admin_icon_lb.image = login_admin_icon
      admin_icon_lb.place(x=10, y=10)
      home_page_fm.pack(fill=tk.BOTH, expand=True)
          
      hi_lb = tk.Label(home_page_fm, text='!hi Admin', font=('Bold', 15))
      hi_lb.place(x=120, y=40)

      
      student_numbers_lb = tk.Label(home_page_fm, text='', font=('Bold', 15),
                                    justify=tk.LEFT)
      student_numbers_lb.place(x=20, y=170)
      class_list_lb = tk.Label(home_page_fm, text='Number of Students By Class ⬇️',
                               font=('Bold',13), bg=bg_color, fg='white')
      class_list_lb.place(x=20, y=130)
      for  i in class_list:    
       result = fectch_student_data(query=f"SELECT COUNT (*) FROM  data WHERE class =='{i}'")
       student_numbers_lb['text'] += f"{i} Class: {result[0][0]}\n\n"
       print(i, result)


       
   
   def send_results_page():
    def send_results():
        student_id = student_id_entry.get()
        file_path = file_path_entry.get()

        if student_id and file_path:
            student_email = fectch_student_data(f"SELECT email FROM data WHERE id_number = '{student_id}'")

            if student_email:
                student_email = student_email[0][0]
                subject = "Results from Admin"
                message = f"<h2>Results/File from Admin</h2><p>Please find the attached file.</p>"

                try:
                    with open(file_path, "rb") as file:
                        file_data = file.read()
                        sendmail_to_student(student_email, message, subject, file_data)
                    message_box("File sent successfully!")
                except FileNotFoundError:
                    message_box("File not found. Please check the file path.")
            else:
                message_box("Invalid student ID.")
        else:
            message_box("Please enter the\n student ID and file path.")

    def browse_file():
        file_path = askopenfilename()
        file_path_entry.delete(0, tk.END)  # Clear previous entry
        file_path_entry.insert(0, file_path)  # Insert selected file path

    send_results_page_fm = tk.Frame(pages_fm)

    student_id_label = tk.Label(send_results_page_fm, text="Student ID:", font=('Bold', 12))
    student_id_label.pack(pady=10)

    student_id_entry = tk.Entry(send_results_page_fm, font=('Bold', 12))
    student_id_entry.pack(fill=tk.X, padx=10)

    file_path_label = tk.Label(send_results_page_fm, text="File Path:", font=('Bold', 12))
    file_path_label.pack(pady=10)

    file_path_entry = tk.Entry(send_results_page_fm, font=('Bold', 12))
    file_path_entry.pack(fill=tk.X, padx=10)

    browse_button = tk.Button(send_results_page_fm, text="Browse", command=browse_file, font=('Bold', 12), bg=bg_color, fg='white')
    browse_button.pack(pady=10)

    send_button = tk.Button(send_results_page_fm, text="Send Results", command=send_results, font=('Bold', 12), bg=bg_color, fg='white')
    send_button.pack(pady=10)

    send_results_page_fm.pack(fill=tk.BOTH, expand=True)




   def announcement_page():
    def send_announcement():
        selected_classes = [class_listbox.get(idx) for idx in class_listbox.curselection()]
        announcement_subject = subject_entry.get()
        announcement_text = announcement_entry.get("1.0", tk.END)

        if selected_classes and announcement_text and announcement_subject:
            for selected_class in selected_classes:
                students = fectch_student_data(f"SELECT email FROM data WHERE class = '{selected_class}'")
                emails = [student[0] for student in students]

                subject = f"{announcement_subject} - {selected_class} Class"
                message = f"<h2>{announcement_subject}</h2><p>{announcement_text}</p>"

                for email in emails:
                    sendmail_to_student(email, message, subject)

            message_box("Announcement sent successfully!")
        else:
            message_box("Please select at least one class,\n enter the subject,\n and enter the announcement text.")

    announcement_page_fm = tk.Frame(pages_fm)

    class_label = tk.Label(announcement_page_fm, text="Select Classes:", font=('Bold', 12))
    class_label.pack(pady=10)

    class_listbox = tk.Listbox(announcement_page_fm, selectmode=tk.MULTIPLE, height=5)
    class_listbox.pack(fill=tk.X, padx=10)
    for class_name in class_list:
        class_listbox.insert(tk.END, class_name)

    subject_label = tk.Label(announcement_page_fm, text="Subject:", font=('Bold', 12))
    subject_label.pack(pady=10)

    subject_entry = tk.Entry(announcement_page_fm, font=('Bold', 12))
    subject_entry.pack(fill=tk.X, padx=10)

    announcement_label = tk.Label(announcement_page_fm, text="Announcement:", font=('Bold', 12))
    announcement_label.pack(pady=10)

    announcement_entry = tk.Text(announcement_page_fm, height=10)
    announcement_entry.pack(padx=10)

    send_button = tk.Button(announcement_page_fm, text="Send Announcement", command=send_announcement, font=('Bold', 12), bg=bg_color, fg='white')
    send_button.pack(pady=10)

    announcement_page_fm.pack(fill=tk.BOTH, expand=True)
   
   def find_student_page():
      def find_student():

        
         if  find_by_option_btn.get() == 'ID':
            found_data = fectch_student_data(query=f"""
SELECT id_number, name, class, gender FROM data 
WHERE id_number == '{search_input.get()}'
""")
            
         elif  find_by_option_btn.get() == 'Name':
            found_data = fectch_student_data(query=f"""
SELECT id_number, name, class, gender FROM data 
WHERE name LIKE '%{search_input.get()}%'""")
            

         elif  find_by_option_btn.get() == 'Class':
            found_data = fectch_student_data(query=f"""
SELECT id_number, name, class, gender FROM data 
WHERE class == '{search_input.get()}'""")
            
            
         elif  find_by_option_btn.get() == 'Gender':
            found_data = fectch_student_data(query=f"""
SELECT id_number, name, class, gender FROM data 
WHERE gender  == '{search_input.get()}'""")
            
            

         if found_data:
            for item in record_table.get_children():
               record_table.delete(item)

            for details in found_data:
               record_table.insert(parent='', index='end', values=details)

         else:
            for item in record_table.get_children():
               record_table.delete(item)
      
      def genrate_student_card():
         selection = record_table.selection() 
         selected_id = record_table.item(item=selection, option='values')[0]
         get_student_details = fectch_student_data(f"""
SELECT name , age , gender, class, phone_number, email FROM data WHERE id_number =='{selected_id}'""")
         

         get_student_pic = fectch_student_data(f"""
SELECT image FROM data WHERE id_number =='{selected_id}'""")
         student_pic = BytesIO(get_student_pic[0][0])
         

         student_details =f"""
{selected_id}
{get_student_details[0][0]}
{get_student_details[0][2]}
{get_student_details[0][1]}
{get_student_details[0][3]}
{get_student_details[0][4]}
{get_student_details[0][5]}
"""
         student_card_image_obj = draw_student_card(studentpicpath=student_pic,
                                                 student_data=student_details)
         student_cardd(student_carb_obj=student_card_image_obj, bypass_login_page=True)

        
      search_filters = ['ID', 'Name', 'Class', 'Gender']
      find_student_pagefm = tk.Frame(pages_fm)
      find_student_pagefm.pack(fill=tk.BOTH, expand=True)



      find_student_record_lb = tk.Label(find_student_pagefm,
                                        text=' Find Student Record ', font=('Bold', 13),
                                        fg='white', bg=bg_color)
      find_student_record_lb.place(x=20, y=10, width=300)

      find_by_lb = tk.Label(find_student_pagefm, text='Find By ;', font=('Bold', 12))
      find_by_lb.place(x=15, y=50)

      find_by_option_btn = Combobox(find_student_pagefm, font=('Bold', 12), 
                                    state='readonly', values=search_filters)
      find_by_option_btn.place(x=80, y=50, width=80)
      find_by_option_btn.set('ID')
      
      search_input = tk.Entry(find_student_pagefm, font=('Bold', 12))
      search_input.place(x=20, y=90)
      search_input.bind('<KeyRelease>', lambda e: find_student())

      record_table_lb = tk.Label(find_student_pagefm, text='Record Table', font=('Bold', 13), bg=bg_color, fg='white')
      record_table_lb.place(x=20, y=160, width=300)

      record_table = Treeview(find_student_pagefm)
      record_table.place(x=0, y=200, width=350)
      record_table.bind('<<TreeviewSelect>>',
                        lambda e: generate_student_card_btn.config(state=tk.NORMAL))

      record_table['columns'] = ('id', 'name', 'class','gender')
      record_table.column('#0', stretch=tk.NO, width=0)

      record_table.heading('id', text='ID Number' ,anchor=tk.W)
      record_table.column('id', width=50, anchor=tk.W)

      record_table.heading('name', text='Name' ,anchor=tk.W)
      record_table.column('name', width=50, anchor=tk.W)

      record_table.heading('class', text='Class' ,anchor=tk.W)
      record_table.column('class', width=50, anchor=tk.W)

      record_table.heading('gender', text='Gender' ,anchor=tk.W)
      record_table.column('gender', width=50, anchor=tk.W)

      generate_student_card_btn = tk.Button(find_student_pagefm, text='Generate Student Card',
                                            font=('Bold', 13), bg=bg_color, fg='white', state=tk.DISABLED, command=genrate_student_card)
      generate_student_card_btn.place(x=160, y=450)
      def clear_results(): 
            find_by_option_btn.set('id')
            search_input.delete(0, tk.END)

            for item in record_table.get_children():
               record_table.delete(item)

               generate_student_card_btn.config(state=tk.DISABLED)

      clear_btn = tk.Button(find_student_pagefm, text='Clear', font=('Bold', 13), 
                            bg=bg_color, fg='white', command=clear_results)
      clear_btn.place(x=10, y=450)
         
     
   dashboard_fm = tk.Frame(root, highlightbackground=bg_color,
                           highlightthickness=3)
   
   options_fm = tk.Frame(dashboard_fm, highlightbackground=bg_color,
                         highlightthickness=2, bg='#c3c3c3')
   home_btn = tk.Button(options_fm, text='Home', font=('Bold', 15),
                        fg= bg_color, bg='#c3c3c3', bd=0, command=lambda: switch(indicator=home_btn_indicator, page=home_page))
   home_btn.place(x=10, y=50)
   
   home_btn_indicator = tk.Label(options_fm, text='', bg= bg_color)
   home_btn_indicator.place(x=5, y=48, width=3, height=40 )

   

   
   find_student_btn = tk.Button(options_fm, text='Find\nStudent', font=('Bold', 15),
                        fg= bg_color, bg='#c3c3c3', bd=0, justify=tk.LEFT, command=lambda: switch(indicator=find_student_btn_indicator, page=find_student_page))
   find_student_btn.place(x=10, y=100)
   
   find_student_btn_indicator = tk.Label(options_fm, text='', bg= '#c3c3c3')
   find_student_btn_indicator.place(x=5, y=108, width=3, height=40 )

   announcement_btn = tk.Button(options_fm, text='Announce\n-ment📢', font=('Bold', 15),
                        fg= bg_color, bg='#c3c3c3', bd=0, justify=tk.LEFT, command= lambda : switch(indicator=announcement_btn_indicator, page=announcement_page))
   announcement_btn.place(x=10, y=170) 
   
   announcement_btn_indicator = tk.Label(options_fm, text='', bg= '#c3c3c3')
   announcement_btn_indicator.place(x=5, y=180, width=3, height=40 )

   send_results_btn = tk.Button(options_fm, text='Send\nResults', font=('Bold', 15),
                                 fg=bg_color, bg='#c3c3c3', bd=0, justify=tk.LEFT,
                                 command=lambda: switch(indicator=send_results_btn_indicator, page=send_results_page))
   send_results_btn.place(x=10, y=270)

   send_results_btn_indicator = tk.Label(options_fm, text='', bg='#c3c3c3')
   send_results_btn_indicator.place(x=5, y=248, width=3, height=40)

   logout_btn = tk.Button(options_fm, text='Logout', font=('Bold', 15),
                        fg= bg_color, bg='#c3c3c3', bd=0, justify=tk.LEFT, command=logout)
   logout_btn.place(x=10, y=500)
   
   

   pages_fm = tk.Frame(dashboard_fm,bg='gray')
   pages_fm.place(x=122, y=5, width=350, height=550)
   #home_page()


   
   options_fm.place(x=0,y=0, width=120, height=575)

   dashboard_fm.pack(pady=5)
   dashboard_fm.pack_propagate(False)
   dashboard_fm.configure(width=480, height=580)
   home_page()
def admin_login_page():
    def show_hide_password():
        if password_entry['show'] == "*":
            password_entry.config(show='')
            show_hide_btn.config(image=unlocked_icon)
        else:
            password_entry.config(show="*")
            show_hide_btn.config(image=lock_icon)
    def switch_to_welcomescreen():
       adminlogin_page_frame.destroy()
       welcome_page()

    def login_account():
       if username_entry.get() == 'admin':
          if  password_entry.get() == 'admin':
             adminlogin_page_frame.destroy()
             admin_dashboard()
             root.update()
          else:
             message_box(' wrong Password ')
       else:
          message_box('Wrong user name')
    


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

    username_entry = tk.Entry(adminlogin_page_frame, font=('Bold', 15),
                            justify=tk.CENTER, highlightcolor=bg_color,
                            highlightbackground='gray', highlightthickness=2)
    username_entry.place(x=80, y=190)

    password_lb = tk.Label(adminlogin_page_frame, text='Enter  Password', font=('Bold', 15), fg=bg_color)
    password_lb.place(x=80, y=240)

    password_entry = tk.Entry(adminlogin_page_frame, font=('Bold', 15),
                            justify=tk.CENTER, highlightcolor=bg_color,
                            highlightbackground='gray', highlightthickness=2,show="*" )
    password_entry.place(x=80, y=290)
    show_hide_btn = tk.Button(adminlogin_page_frame, image=lock_icon , bd=0, command=show_hide_password)
    show_hide_btn.place(x=310, y=280)
    login_btn = tk.Button(adminlogin_page_frame, text="Login", font=('Bold', 15), bg=bg_color, fg='white', command=login_account)
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
        pattern = r'^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$'
        match = re.match(pattern=pattern, string=email)
        return match

    def generate_id_number():
       generate_id = ''

       for r in range(4):
          generate_id += str(random.randint(0, 9))

      #  print(check_id_already_exists(id_number=generate_id))
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

       elif  not check_invalid_email(email=student_emailentry.get().lower()):
           
           student_emailentry.config(highlightcolor='red',
                                     highlightbackground='red' )
           message_box('invalid email')
           student_name_entry.focus()
           


       elif account_passwordentry.get() == '':
          account_passwordentry. config(highlightcolor='red', highlightbackground= 'red')
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
             read_data = open('images/add_image.png', 'rb')
             pic_data =read_data.read()
             read_data.close()
             pic_path.set('images/add_image.png')

          add_data(id_number=student_id.get(),
                   password=account_passwordentry.get(),
                   name= student_name_entry.get(),
                   age= student_age_ent.get(),
                   gender=student_gender.get(),
                   phone_number=student_contactentry.get(),
                   student_class=student_classbtn.get(),
                   email=student_emailentry.get(),
                   pic_data=pic_data)
          
          data = f"""
{student_id.get()}
{student_name_entry.get()}
{student_gender.get()}
{student_age_ent.get()}
{student_classbtn.get()}
{student_contactentry.get()}
{student_emailentry.get()}

"""
          get_card = draw_student_card(studentpicpath=pic_path.get(),student_data=data)
        

          student_cardd(student_carb_obj= get_card)
          add_account_page_frame.destroy()
          message_box("Account Successfully Created!")
       

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
#add_account_page()
#forgetpassword_page()
#draw_student_card()
#student_login_page()
#sendmail_to_student(email='temiojekunle74@gmail.com', message='<h1>Hello World<\h1>', subject='testing')
#student_dashboard(student_id='fstc1178')
welcome_page()
#admin_dashboard()
#admin_login_page()
root.mainloop()






