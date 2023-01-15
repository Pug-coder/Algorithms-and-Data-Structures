# Грамматика для описания MFA
## атрибуты переходов: 
isReading, isWriting (читаемые из входных данных), isDeterministic, isMemoryIndependent; 

## атрибуты узлов: 
isInitial, isFinal (читаемые из входных данных), isTrap) в пользовательском синтаксисе и реализовать генератор графов MFA. 

## запуск:
python main.py 1

dot -Tsvg graph.dot > graph.svg
