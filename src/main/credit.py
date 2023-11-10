import tkinter as tk
from tkinter import *
from datetime import datetime, timedelta
import calendar
import matplotlib.pyplot as plt
from tkinter import messagebox
from tkcalendar import DateEntry
import tkinter.ttk as ttk


def func():
   number_credit = number_credit_tf.get()
   credit = int(credit_tf.get())
   currency = currency_tf.get()
   date_start = datetime.strptime(date_start_tf.get(), '%d.%m.%Y')
   term = int(term_tf.get())
   dates = [datetime.strftime(date_start, '%d.%m.%Y')]

   for i in range(60):
      next_month = date_start + timedelta(days=30)
      next_month = next_month.replace(day=date_start.day)
      dates.append(next_month.strftime("%d.%m.%Y"))
      date_start = next_month
   procent = int(procent_tf.get()) / 100
   repayment_method = repayment_method_tf.get()
   procents = [0.00]
   loan_debt = [credit]
   od = [0.00]

   if repayment_method == "Аннуитет":
      payment = int(
         credit * (procent / 12 * (1 + procent / 12) ** term) / (((1 + procent / 12) ** term) - 1))
      for i in range(len(dates) - 1):
         date_current = datetime.strptime(dates[i], '%d.%m.%Y')
         date_next = datetime.strptime(dates[i + 1], '%d.%m.%Y')
         if date_current.month == 12 and calendar.isleap(date_next.year) is True:
            pro = credit * procent / 365 * (datetime(date_current.year, date_current.month,
                                                                 31) - date_current).days + credit * procent / 366 * (
                                (date_next - datetime(date_next.year, date_next.month, 1)).days + 1)
            procents.append(round(pro, 2))
         elif date_current.month == 12 and calendar.isleap(date_current.year) is True:
            pro = credit * procent / 366 * ((datetime(date_current.year, date_current.month,
                                                                  31) - date_current).days) + credit * procent / 365 * (
                                   (
                                           date_next - datetime(
                                      date_next.year,
                                      date_next.month,
                                      1)).days + 1)
            procents.append(round(pro, 2))
         elif date_next.month >= 2 and calendar.isleap(date_current.year) is True:
               pro = credit * procent / 366 * (date_next - date_current).days
               procents.append(round(pro, 2))
         else:
               pro = credit * procent / 365 * (date_next - date_current).days
               procents.append(round(pro, 2))
         if credit > payment:
            credit = credit - payment + pro
            loan_debt.append(round(credit, 2))
         else:
            loan_debt.append(0)
         loan = payment - pro
         if loan > loan_debt[-2]:
            od.append(round(credit, 2))
         else:
            od.append(round(loan, 2))


      plt.plot(dates, od, label='Погашение основного долга')
      plt.plot(dates, procents, label='Погашение процентов')
      plt.title('График платежей по кредиту')
      plt.xlabel('Дата платежа')
      plt.ylabel('Сумма')
      plt.legend()
      plt.show()

      with open(f'{number_credit}', 'w', encoding='utf-8') as file:
         file.write(
            "____________________________________________________________________________________________________________________________________\n"
            "| Дата платежа | Погашение основного долга | Погашение процентов | Процентная ставка | Аннуитетный платеж | Остаток основного долга |\n"
            "|______________|___________________________|_____________________|___________________|____________________|_________________________|\n"
            )
         for i in range(len(dates)):
            file.write(
               f'| {dates[i]:<12} | {od[i]:<25} | {procents[i]:<19} | {procent * 100:<16}% | {payment:<18} | {loan_debt[i]:>19} {currency} |\n')
         file.write(
         '|___________________________________________________________________________________________________________________________________|')
   if repayment_method == 'Дифференцированные платежи':
      char = int(credit / term)
      for i in range(len(dates) - 1):
         date_current = datetime.strptime(dates[i], '%d.%m.%Y')
         date_next = datetime.strptime(dates[i + 1], '%d.%m.%Y')
         if date_current.month == 12 and calendar.isleap(date_next.year) is True:
            pro = credit * procent / 365 * (datetime(date_current.year, date_current.month,
                                                31) - date_current).days + credit * procent / 366 * (
                             (date_next - datetime(date_next.year, date_next.month, 1)).days + 1)
            procents.append(round(pro, 2))
         elif date_current.month == 12 and calendar.isleap(date_current.year) is True:
            pro = credit * procent / 366 * ((datetime(date_current.year, date_current.month,
                                                 31) - date_current).days) + credit * procent / 365 * ((
                                                                                                          date_next - datetime(
                                                                                                     date_next.year,
                                                                                                     date_next.month,
                                                                                                     1)).days + 1)
            procents.append(round(pro, 2))
         elif date_next.month >= 2 and calendar.isleap(date_current.year) is True:
            pro = credit * procent / 366 * (date_next - date_current).days
            procents.append(round(pro, 2))
         else:
            pro = credit * procent / 365 * (date_next - date_current).days
            procents.append(round(pro, 2))
         if credit - char < char:
            loan_debt.append(0)
         else:
            credit = credit - char
            loan_debt.append(round(credit, 2))
         if char > loan_debt[-1]:
            od.append(round(credit, 2))
         else:
            od.append(round(char, 2))

      plt.plot(dates, od, label='Погашение основного долга')
      plt.plot(dates, procents, label='Погашение процентов')
      plt.title('График платежей по кредиту')
      plt.xlabel('Дата платежа')
      plt.ylabel('Сумма')
      plt.legend()
      plt.show()

      with open(f'{number_credit}', 'w', encoding='utf-8') as file:
         file.write(
            "____________________________________________________________________________________________________________________________________\n"
            "| Дата платежа | Погашение основного долга | Погашение процентов | Процентная ставка | Ежемесячный платеж | Остаток основного долга |\n"
            "|______________|___________________________|_____________________|___________________|____________________|_________________________|\n"
            )
         for i in range(len(dates)):
            file.write(
               f'| {dates[i]:<12} | {od[i]:<25} | {procents[i]:<19} | {procent * 100:<16}% | {round((procents[i] + char), 2):<18} | {loan_debt[i]:>19} {currency} |\n')
         file.write(
         '|___________________________________________________________________________________________________________________________________|')

   if repayment_method == "В конце срока":
      for i in range(len(dates) - 1):
         date_current = datetime.strptime(dates[i], '%d.%m.%Y')
         date_next = datetime.strptime(dates[i + 1], '%d.%m.%Y')
         if date_current.month == 12 and calendar.isleap(date_next.year) is True:
            pro = credit * procent / 365 * (datetime(date_current.year, date_current.month,
                                                31) - date_current).days + credit * procent / 366 * (
                             (date_next - datetime(date_next.year, date_next.month, 1)).days + 1)
            procents.append(round(pro, 2))
         elif date_current.month == 12 and calendar.isleap(date_current.year) is True:
            pro = credit * procent / 366 * ((datetime(date_current.year, date_current.month,
                                                 31) - date_current).days) + credit * procent / 365 * ((
                                                                                                          date_next - datetime(
                                                                                                     date_next.year,
                                                                                                     date_next.month,
                                                                                                     1)).days + 1)
            procents.append(round(pro, 2))
         elif date_next.month >= 2 and calendar.isleap(date_current.year) is True:
            pro = credit * procent / 366 * (date_next - date_current).days
            procents.append(round(pro, 2))
         else:
            pro = credit * procent / 365 * (date_next - date_current).days
            procents.append(round(pro, 2))
         if i != 59:
            loan_debt.append(credit)
         else:
            loan_debt.append(0.00)
         if i != 59:
            od.append(0.00)
         else:
            od.append(credit)

      plt.plot(dates, od, label='Погашение основного долга')
      plt.plot(dates, procents, label='Погашение процентов')
      plt.title('График платежей по кредиту')
      plt.xlabel('Дата платежа')
      plt.ylabel('Сумма')

      plt.legend()

      with open(f'{number_credit}', 'w', encoding='utf-8') as file:
         file.write(
            "____________________________________________________________________________________________________________________________________\n"
            "| Дата платежа | Погашение основного долга | Погашение процентов | Процентная ставка | Ежемесячный платеж | Остаток основного долга |\n"
            "|______________|___________________________|_____________________|___________________|____________________|_________________________|\n")
         for i in range(len(dates)):
            file.write(
               f'| {dates[i]:<12} | {od[i]:<25} | {procents[i]:<19} | {procent * 100:<16}% | {round((procents[i] + od[i]), 2):<18} | {loan_debt[i]:>19} {currency} |\n')
         file.write(
            '|___________________________________________________________________________________________________________________________________|')
      plt.show()

   else:
      messagebox.showinfo('Ошибка', f'Введите корректный способ погашения')

window = Tk()
window.title("Декстоп-приложение на Python")
window.geometry('800x600')
frame = Frame(
   window, #Обязательный параметр, который указывает окно для размещения Frame.
   padx=10, #Задаём отступ по горизонтали.
   pady=10 #Задаём отступ по вертикали.
)
frame.pack(expand=True)

number_credit = Label(
    frame,
    text='Номер кредитного договора'
)
number_credit.grid(row=3, column=1)

credit = Label(
   frame,
   text="Введите сумму кредита"
)
credit.grid(row=4, column=1)

currency = Label(
   frame,
   text="Введите валюту"
)

currency.grid(row=5, column=1)

date_start = Label(
   frame,
   text="Введите дату начала кредитования"
)
date_start.grid(row=6, column=1)

term = Label(
   frame,
   text="Введите срок кредитования"
)

term.grid(row=7, column=1)

procent = Label(
   frame,
   text="Введите процент"
)
procent.grid(row=8, column=1)

repayment_method = Label(
   frame,
   text="Введите способ погашения"
)
repayment_method.grid(row=9, column=1)

number_credit_tf = Entry(
    frame
)
number_credit_tf.grid(row=3, column=2)

credit_tf = Entry(
   frame
)
credit_tf.grid(row=4, column=2)

currency_tf = ttk.Combobox(frame, values=['RUB', 'USD', 'EUR'])

currency_tf.grid(row=5, column=2)

date_start_tf = DateEntry(
   frame,
   date_pattern="dd.mm.YYYY"
)
date_start_tf.grid(row=6, column=2)

term_tf = Entry(
   frame
)

term_tf.grid(row=7, column=2)

procent_tf = Entry(
   frame
)
procent_tf.grid(row=8, column=2)

repayment_method_tf = ttk.Combobox(frame, values=['Аннуитет', 'Дифференцированные платежи', 'В конце срока'])

repayment_method_tf.grid(row=9, column=2)

cal_btn = Button(
   frame, #Заготовка с настроенными отступами.
   text='Рассчитать график платежей', #Надпись на кнопке.
   command=func
)
cal_btn.grid(row=10, column=2)

menu = tk.Menu()
file_menu = tk.Menu(menu, tearoff=0)
file_menu.add_command(label="Создать график")
menu.add_cascade(label="График погашения", menu=file_menu)
menu.add_command(label="Досрочное погашение")

window.config(menu=menu)

window.mainloop()

