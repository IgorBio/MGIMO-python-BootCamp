#!/usr/bin/env python3
# def lists_sum(*args, unique=False):
#     if not unique:
#         summary = 0
#         for i in args:
#             summary += sum(i)
#         return summary
#     elif unique:
#         temp = []
#         for i in args:
#             for j in i:
#                 if j not in temp:
#                     temp.append(j)
#         return temp[-1]




# import datetime
# import math

# birthdays = {"Иванов Иван Иванович": datetime.date(1989, 5, 1), "Петров Петр Петрович": datetime.date(1998, 5, 6)}
#
# def gift_count(budget: int, month: int, birthdays: dict):
#     m_dict = {}
#     for i, j in birthdays.items():
#         if m == j.month:
#             m_dict[i] = j
#     count = 0
#     if not m_dict:
#         print("В этом месяце нет именинников.")
#     else:
#         print(f"Именинники в месяце {month}:", end=" ")
#         values = list(birthdays.items())
#         values.sort(key=lambda x: (x[1], x[0]))
#         for key, item in values:
#             print(f"{key} {'(' +item.strftime('%d.%m.%Y') + ')'}", end=", ")
#             count += 1
#         print(f". При бюджете {budget}  они получат по {math.floor(budget / count)} рублей.")
#


# import datetime
#
# date = datetime.date(*[int(i) for i in input().split("-")[::-1]])
# print((date - datetime.timedelta(days=date.weekday())).strftime("%d-%m-%Y"))

