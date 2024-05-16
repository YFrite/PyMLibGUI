from PyMLib.regressions import LinearRegression
from block.ai import AI
from block.input import Input
from block.output import Output

blocks = (AI(name="Линейная регрессия", algorithm=LinearRegression()),
          Input(name="Входные данные"), Output(name="Выходные данные"))
