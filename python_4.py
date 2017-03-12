import pprint


units = {1: 'one', 2: 'two', 3: 'three',
         4: 'four', 5: 'five', 6: 'six',
         7: 'seven', 8: 'eight', 9: 'nine'}

decades = {10: 'ten',      11: 'eleven',    12: 'twelve',
           13: 'thirteen', 14: 'fourteen',  15: 'fifteen',
           16: 'sixteen',  17: 'seventeen', 18: 'eighteen',
           19: 'nineteen', 20: 'twenty',    30: 'thirty',
           40: 'fourty',   50: 'fifty',     60: 'sixty',
           70: 'seventy',  80: 'eighty',    90: 'ninety'}

majors = {1: units, 10: decades, 100: 'hundred',
          1000: 'thousand', 1000000: 'million'}


def row_making(number, num_row, majors):
  for i, major in enumerate(majors):
    if major > number: continue
    else:
      if number // major > 10:
        num_row[major] = row_making(number//major, {}, majors[i:])
        number = number % major
      else:
        num_row[major] = number // major
        number = number % major
  return num_row

number = 123456789
majors_keys = sorted(majors, reverse=True)
num_row = row_making(number, {}, majors_keys)
pprint.pprint(num_row)

text_number = []
for num, count in sorted(num_row.items(), reverse=True):
    if type(count) == type(dict()):
      sub_row = count
      for s_num, s_count in sorted(sub_row.items(), reverse=True):
        if s_num == 100:
          text_number.append(majors[1][s_count])
          text_number.append(majors[s_num])
          text_number.append('and')
        elif s_num == 10:
          text_number.append(majors[s_num][10*s_count])
        elif s_num == 1:
          text_number.append(majors[s_num][s_count])
      text_number.append(majors[num])
    else:
      if num == 100:
        text_number.append(majors[1][count])
        text_number.append(majors[num])
        text_number.append('and')
      elif num == 10:
        text_number.append(majors[num][10*count])
      elif num == 1:
        text_number.append(majors[num][count])
print (" ".join(text_number))