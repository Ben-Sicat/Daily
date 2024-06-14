
def __init__(self):
    pass

def trebuchet(self):
    """
        This function will solve the first problem of the Advent of Code. 
    """
        # i need to read the data in trebuchet.txt
    data = open("trebuchet.txt", "r")
        # i'll be storing the data in a list
    data_list = [line.strip() for line in data]
    temp = ""   
    last = "" 
    sum = 0
    for code in data_list:
        for char in code:
            if char.isdigit(): 
                if len(temp) == 0:
                    temp = char
                else:
                    last = char
                    
                if last == "":
                    last = temp
        sum += int(temp+last)
        temp = ""
        last = ""
            
    print(sum)
    
#answer is 55477 




















