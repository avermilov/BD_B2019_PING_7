# Task 6
## Query 1.
Для Олимпийских игр 2004 года сгенерируйте список (год рождения, количество игроков, количество золотых медалей), содержащий годы, в которые родились игроки, количество игроков, родившихся в каждый из этих лет, которые выиграли по крайней мере одну золотую медаль, и количество золотых медалей, завоеванных игроками, родившимися в этом году.
```sql
SELECT EXTRACT(YEAR FROM Players.birthdate), COUNT(DISTINCT Players.player_id), COUNT(Results.medal)
FROM Players
INNER JOIN Results ON Players.player_id = Results.player_id
INNER JOIN Events ON Results.event_id = Events.event_id
INNER JOIN Olympics ON Events.olympic_id = Olympics.olympic_id
WHERE Olympics.year = 2004 AND Results.medal ='GOLD'
GROUP BY EXTRACT(YEAR FROM Players.birthdate);
```
## Query 2.
Перечислите все индивидуальные (не групповые) соревнования, в которых была ничья в счете, и два или более игрока выиграли золотую медаль.
```sql
SELECT Events.event_id
FROM Events
INNER JOIN Results ON Events.event_id = Results.event_id
WHERE Results.medal = 'GOLD' AND Events.is_team_event = 0
GROUP BY Events.event_id
HAVING COUNT(Results.medal) >= 2;
```
## Query 3.
Найдите всех игроков, которые выиграли хотя бы одну медаль (GOLD, SILVER и BRONZE) на одной Олимпиаде. (player-name, olympic-id).
```sql
SELECT DISTINCT Players.name, Events.olympic_id
FROM Players
INNER JOIN Results ON Results.player_id = Players.player_id
INNER JOIN Events ON Events.event_id = Results.event_id
WHERE Results.medal IN ('GOLD', 'SILVER', 'BRONZE');
```
## Query 4.
В какой стране был наибольший процент игроков (из перечисленных в наборе данных), чьи имена начинались с гласной?
```sql
SELECT CountryVowelGroups.country_id
FROM (
         SELECT Players.country_id, COUNT(*) AS vowels_num
         FROM Players
         WHERE UPPER(LEFT(Players.name, 1)) IN ('A', 'E', 'I', 'O', 'U')
         GROUP BY Players.country_id
) AS CountryVowelGroups
JOIN (
    SELECT Players.country_id, count(*) AS player_num
    FROM Players
    GROUP BY Players.country_id
) AS CountryPlayerGroups ON CountryVowelGroups.country_id = CountryPlayerGroups.country_id
ORDER BY CAST(vowels_num AS DECIMAL) / player_num DESC
LIMIT 1;
```
## Query 5.
Для Олимпийских игр 2000 года найдите 5 стран с минимальным соотношением количества групповых медалей к численности населения.
```sql
SELECT Countries.country_id
FROM Olympics
INNER JOIN Events ON Events.olympic_id = Olympics.olympic_id
INNER JOIN Results ON Events.event_id = Results.event_id
INNER JOIN Players ON Players.player_id = Results.player_id
INNER JOIN Countries ON Countries.country_id = Players.country_id
WHERE Olympics.year = 2000 AND Events.is_team_event = 1
GROUP BY Countries.country_id, Countries.population
ORDER BY CAST(COUNT(Results.medal) AS DECIMAL) / Countries.population
LIMIT 5;
```
