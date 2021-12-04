## Task 1

1) Вначале имеем (B, D), так как (BD)+
2) D → EG, значит добавляем E и G, то есть (B, D, E, G)
3) BE → C, значит добавляем C, то есть (B, C, D, E, G)
4) C → A, значит добавляем A, то есть (A, B, C, D, E, G)

Таким образом, замыкание - (A, B, C, D, E, G)

## Task 2

A)
  * CustomerNo → CustomerName 
  * ProductNo → ProductName
  * ProductNo → Tax
  * SubTotal, Tax → Total
  * UnitPrice, Quantity → SubTotal
  * ProductNo, CustomerNo, OrderDate → UnitPrice, Quantity, SubTotal, Tax, Total
  * ProductNo → UnitPrice

Б) CustomerNo, OrderDate, ProductNo

## Task 3

А) AB или AC

Б) Преобразование пошагово:

1. Для каждой зависимости из F посмотрим на отношения:
    * (A, C, B)
    * (A, B, C)
    * (A, D)

2. Таким образом, 3NF для R это R1(A, D) и R2(A, B, C)
