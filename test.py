

def standardize_length(input):
    hour = 0
    min = 0
    sec = 0

    input = input.replace('PT', '')
    input = input.upper()
    if 'H' in input:
        hour = input.split('H')[0]
        input = input.split('H')[1]
    if 'M' in input:
        min = input.split('M')[0]
        input = input.split('M')[1]
    if 'S' in input:
        sec = input.split('S')[0]
        input = input.split('S')[1]
    return hour, min, sec


test = ['PT1H2M3S', 'PT1H3S', 'PT2M3S', 'PT1H3S', 'PT3S', 'PT2M', 'PT1H']

for s in test:
    result = standardize_length(s)
    print(result[0], 'H', result[1], 'M', result[2], 'S')
