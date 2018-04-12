import re, sys
import matplotlib.pyplot as plt


class ColumnScadGraph:
    def __init__(self, rsuFileName):
        self.rsuFileName = rsuFileName  # для отладочных целей
        self.mLines = self.openReadClose(rsuFileName)  # записали из файлов массивы строк
        self.mn1 = []  # массивы усилий -- загружение 1
        self.mn2 = []  # загружение 2
        self.mn = []  # сумма усилий 2-х загружений
        self.plotCount = 1 # счетчик подокон графика

    def openReadClose(self, name): # считывает строки файла в массив
        f = open(name, "r")
        m = f.readlines()
        f.close()
        return m

    def patUsil(self, force):  # конструирует именованную группу рег. выражений, в зависимости от вида усилия,
        # переданного текстовой строкой
        pat = "-{,1}\d*\.??\d+E??e??[-+]{,1}\d*"
        return "(?P<" + force + ">" + pat + ")" # вызывается в self.patNumber

    def patNumber(self, num, loadCase = "1"):
        searchPat = ""  # сконструируем наш паттерн для поиска
        for i in ["n", "mk", "my", "qz", "mz", "qy"]:
            if i != "qy":
                searchPat = searchPat + self.patUsil(i) + "\s+"
            else:
                searchPat = searchPat + self.patUsil(i)
        #print("^" + str(num) + "\s+" + "(?P<section>\d+)" + "\s" + loadCase + "\s" + searchPat)
        return "^" + str(num) + "\s+" + "(?P<section>\d+)" + "\s" + loadCase + "\s" + searchPat

    "нужно 2 паттерна, для двух загружений"

    def numbers(self, mArg):
        for ke in mArg:
            pat1 = self.patNumber(ke, "1")  # что значит 1-е загружение а не сечение
            pat2 = self.patNumber(ke, "2")
            fPat1 = re.compile(pat1)
            fPat2 = re.compile(pat2)
            self.mn1.append(self.eachFileN(self.mLines, fPat1, ke))
            # append еще раз оборачивает выводимое значение в массив, поэтому для каждого КЕ свой массив (3 скобки)
            # массив усилий -> массив сечений -> массив КЕ
            self.mn2.append(self.eachFileN(self.mLines, fPat2, ke))
        self.sumKEM()  # заполнил self.mn
        #print(self.mn)
        self.plotMy(self.mn, 'loadCase 1_My + loadCase 2_My' + str(mArg))
        self.plotMy(self.mn1, 'loadCase 1_My ' + str(mArg))
        self.plotMy(self.mn2, "loadCase 2_My " + str(mArg))
        plt.show()

    def eachFileN(self, linesInFile, fPat, item):  # парсит массив на наличие строк усилий, удовлетворяющих паттерну,
        #  затем выводит их в массиве
        m = []
        for lineString in linesInFile:
            f = re.search(fPat, lineString)
            if f is not None:  # срабатывает несколько раз для данного КЕ (несколько сечений)
                n = f.group("n")
                mk = f.group("mk")
                my = f.group("my")
                qz = f.group("qz")
                mz = f.group("mz")
                qy = f.group("qy")
                m.append([n, mk, my, qz, mz, qy])
                # выводится массив массивов, в каждом свое сечение
        if m == []:
            pass
            print("\n нет такого КЕ -- ", item)
            print("lineString = ", lineString)
            print("fPat =" , fPat)
        return m

    def plotMy(self, m, title):
        self.plot(m, title, 2)

    def plotMz(self, m, title):
        self.plot(m, title, 4)
        
    def sumForce(self, mf1 , mf2):
        return list(map(lambda x,y: round(float(x)+float(y), 3), mf1, mf2)) 
        
    def sumSection(self, ms1, ms2):  # обрабатывает массив усилий для разных сечений одного КЕ
        return list(map(self.sumForce, ms1, ms2))
        
    def sumKEM(self):  # обрабатывает массив КЕ
        print(self.mn1)
        print(self.mn2)
        self.mn = list(map(self.sumSection, self.mn1, self.mn2))

    def plot(self, m, title, forceCase):  # forceCase - это вид усилий
        plt.subplot(3, 1, self.plotCount)
        #plt.gca().set_aspect('equal')
        #plt.axis('scaled')
        #plt.grid(True)
        self.plotCount += 1
        #ax = plt.gca()
        #ax.spines['bottom'].set_position('center')
        # массив ke -> массив сечений -> массив усилий
        x = 0
        mx=[];my=[]
        plt.title(title)        
        try:
            for ke in m:
            #count = 1
                for i in range(1, len(ke)):                
                    mx.append(x); mx.append(x+1)
                    my.append(ke[i - 1][forceCase]); my.append(ke[i][forceCase])
                    x = x + 1
                    #count = 0
                plt.plot(mx,my); mx=[];my=[]
            plt.plot([0,x], [0,0])
        except IndexError:
            print("IndexError: неполучилось распечататься, m =  " + str(m) + "\n")
            sys.exit()
