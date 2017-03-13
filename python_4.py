import pprint


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
  for i, major in enumerate(majors):
    if major > number:
      continue
    else:
      if number // major > 10:
        num_row[major] = row_making(number // major, {}, majors[i:])
        number = number % major
      else:
        num_row[major] = number // major
        number = number % major
  return num_row

number = 200

majors_numbers = sorted(majors, reverse=True)
numb_row = row_making(number, {}, majors_numbers)

pprint.pprint(numb_row)

def hundreds_of_text(numb_row, text_number):
    decade = None
    for number, count in sorted(numb_row.items(), reverse=True):
        if type(count) == type(dict()):
            text_number = hundreds_of_text(count, text_number)
            text_number.append(majors[number])
        if number == 1000000 and len(text_number) == 0:
            text_number.append(majors[1][count])
            text_number.append(majors[number])
        if number == 1000 and len(text_number) == 0:
            text_number.append(majors[1][count])
            text_number.append(majors[number])
        if number == 100:
            text_number.append(majors[1][count])
            text_number.append(majors[number])
        if number == 10:
            decade = count
            text_number.append(majors[10][10 * decade])
        if number == 1:
            if decade == 1:
                decade = 10 * decade + count
                text_number.pop(len(text_number) - 1)
                text_number.append(majors[10][decade])
                continue
            if decade > 1:
                text_number.pop(len(text_number) - 1)
                text_number.append(majors[10][10 * decade])
                text_number.append(majors[number][count])
                continue
            text_number.append(majors[number][count])
    return text_number

print (" ".join(hundreds_of_text(numb_row, [])))
