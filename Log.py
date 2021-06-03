import datetime

def write(string):
    f=open("LOG.txt", "a+",encoding="utf-8")
    f.write(string)
    f.flush()
    #f.close()

def log(context, src):
    x = str(datetime.datetime.now())
    string = x + '\t[LOG]\t' + context + '\t[SOURCE]\t' + src + '\n'  
    write(string)
    print(string)

def warning(context, src):
    x = str(datetime.datetime.now())
    string = x + '\t[WRN]\t' + context + '\t[SOURCE]\t' + src + '\n'   
    write(string)
    print(string)

def error(context, src):
    x = str(datetime.datetime.now())
    string = x + '\t[ERR]\t' + context + '\t[SOURCE]\t' + src + '\n'   
    write(string)
    print(string)

