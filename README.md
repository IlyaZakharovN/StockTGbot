# StockTGbot

Это телеграм-бот, дающий информацию последнем выгодном моменте покупки и продажи акций, котороый рассчитан через пересечение экспонециальные скользящих средних (EMA) с периодами 9 и 21 с поправкой на EMA с периодом 200 (покупать, когда EMA 9 пересекает EMA 21 снизу вверх, и обе EMA находятся над EMA 200; продавать, когда EMA 21 пересекает EMA 9 сверху вниз, и обе EMA находятся под EMA 200).

Используются следующие библиотеки Python:
yfinance - для получение информации об инструментах с Yahoo Finance;
pandas - для удобного расчета пересечений EMA 9 и 21.


Примеры работы:
1. 
![image](https://user-images.githubusercontent.com/95462920/155878014-a08e6cce-a556-4e0d-b2e8-dd44d93a7ee8.png)

В то же время "под капотом":
![image](https://user-images.githubusercontent.com/95462920/155878056-f4987f88-f132-449f-a92c-6e1d567af7ed.png)

2) ![image](https://user-images.githubusercontent.com/95462920/155878077-777b133f-ad84-45b8-aa65-13779d085cbd.png)
![image](https://user-images.githubusercontent.com/95462920/155878090-64cb5d78-2130-4559-8abe-c61187b59b92.png)

