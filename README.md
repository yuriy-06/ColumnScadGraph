Этот пакет предназначен для рисования упрощенных эпюр (графиков усилий) для серии КЕ балок и колонн.
Усилия используются из расчетной программы  Scad.
Пример использования:
```
from ColumnScadGraph.ColumnScadGraph import ColumnScad as sc
test = sc.ColumnScadGraph(rsuFileName = "g:/temp/analiz/rsu-B-G")
test.numbers([4064, 4065, 4066]) # здесь слева направо КЕ колонны
```