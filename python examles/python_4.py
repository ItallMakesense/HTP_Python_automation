"""
Function that translates integers to words.

More specifically, for a given positive integer it converts into
its English representation.

Example:
int_to_words(12356) # => 'twelve thousand three hundred and fifty six'

"""

units = {1: 'one', 2: 'two', 3: 'three',
         4: 'four', 5: 'five', 6: 'six',
         7: 'seven', 8: 'eight', 9: 'nine'}

decades = {10: 'ten', 11: 'eleven', 12: 'twelve',
           13: 'thirteen', 14: 'fourteen', 15: 'fifteen',
           16: 'sixteen', 17: 'seventeen', 18: 'eighteen',
           19: 'nineteen', 20: 'twenty', 30: 'thirty',
           40: 'fourty', 50: 'fifty', 60: 'sixty',
           70: 'seventy', 80: 'eighty', 90: 'ninety'}

majors = {1: units, 10: decades, 100: 'hundred',
          1000: 'thousand', 1000000: 'million'}


def row_making(number, num_row, majors):
  for index, major in enumerate(majors):
    if major > number:
      continue
    else:
      if number // major > 10:
        num_row[major] = row_making(number // major, {}, majors[index:])
        number = number % major
      else:
        num_row[major] = number // major
        number = number % major
  return num_row


def int_to_text(numb_row, text_number=list(), dozen=False):
  for number, count in sorted(numb_row.items(), reverse=True):
    if type(count) == type(dict()):
      text_number = int_to_text(count, text_number)
      text_number.append(majors[number])
      continue
    if number <= 10:
      if number == 10:
        if count == 1:
          dozen = True
        text_number.append(decades[10 * count])
      if number == 1:
        if dozen:
          text_number.pop(len(text_number) - 1)
          text_number.append(decades[10 + count])
        else:
          text_number.append(units[count])
    else:
      text_number.append(units[count])
      text_number.append(majors[number])
      if len(numb_row) > 1 and text_number[-1] == 'hundred':
        text_number.append('and')
  return text_number


def int_to_words(number):
  numb_row = row_making(int(number), {}, sorted(majors, reverse=True))
  return " ".join(int_to_text(numb_row))

number = input("Type integer number here: ")

print (int_to_words(number))
