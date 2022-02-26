def toTime(timeInSec=0):
    hour = (timeInSec//60)
    minute = (timeInSec%60)
    return('{:02}:{:02}'.format(hour,minute))
if __name__ == '__main__':
    print(toTime())