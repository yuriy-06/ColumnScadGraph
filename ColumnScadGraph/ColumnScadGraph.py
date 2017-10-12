import re
import matplotlib.pyplot as plt


class ColumnScadGraph:
    def __init__(self, rsuFileName):
        self.rsuFileName = rsuFileName  # для отладочных целей

        self.mLines = self.openReadClose(rsuFileName)  # записали из файлов массивы строк

        self.mn1 = []  # массивы усилий -- загружение 1
        self.mn2 = []  # загружение 2

    @staticmethod
    def openReadClose(name):
        f = open(name, "r")
        m = f.readlines()
        f.close()
        return m

    def patUsil(self, force):  # конструирует именованную группу рег. выражений, в зависимости от вида усилия,
        # переданного текстовой строкой
        pat = "-{,1}\d*\.\d+E{,1}[-+]{,1}\d*"
        return "(?P<" + force + ">" + pat + ")" # вызывается в self.patNumber

    def patNumber(self, num, loadCase = "1"):
        searchPat = ""  # сконструируем наш паттерн для поиска
        for i in ["n", "mk", "my", "qz", "mz", "qy"]:
            if i != "qy":
                searchPat = searchPat + self.patUsil(i) + "\s+"
            else:
                searchPat = searchPat + self.patUsil(i)
        return str(num) + "\s+" + "(?P<section>\d+)" + "\s" + loadCase + "\s" + searchPat

    "нужно 2 паттерна, для двух загружений"

    def numbers(self, mArg):
        for ke in mArg:
            pat1 = self.patNumber(ke, "1")
            pat2 = self.patNumber(ke, "2")
            fPat1 = re.compile(pat1)
            fPat2 = re.compile(pat2)
            self.mn1.append(self.eachFileN(self.mLines, fPat1, ke))
            # append еще раз оборачивает выводимое значение в массив, поэтому для каждого КЕ свой массив (3 скобки)
            # массив усилий -> массив сечений -> массив КЕ
            self.mn2.append(self.eachFileN(self.mLines, fPat2, ke))
        self.plotMy(self.mn1, 'загружение 1_My')
        self.plotMy(self.mn2, "загружение 2_My")
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
        return m

    def plotMy(self, m, title):
        self.plot(m, title, 2)

    def plotMz(self, m, title):
        self.plot(m, title, 4)

    def plot(self, m, title, forceCase):  # forceCase - это вид усилий
        # массив ke -> массив сечений -> массив усилий
        x = 0
        plt.title(title)
        for ke in m:
            plt.plot([x, x + 1], [ke[0][forceCase], ke[1][forceCase]])  # распечатали первые 2 сечения
            x = x + 1
            plt.plot([x, x + 1], [ke[1][forceCase], ke[2][forceCase]])  # распечатали 2-е и третье сечение
            x = x + 1
        plt.show()
