#### Answers to the questions on the loaded data

This is on data that is successfully loaded into the postgres database. Invalid rows are not included. They will need to be looked at and loaded after discovering what causes them to fail to load and then correcting an issues. 

#### Answers
i. What is the number of unique users?

```sql
SELECT count(distinct user_id) 
FROM stage.user_events;
```
`863`

ii. Who are the marketing ad providers?

```sql
SELECT DISTINCT provider 
FROM stage.marketing_events;
```
```Instagram
 Facebook
 Snapchat
 Spotify
```

iii. Which user property is changed the most frequently?

```sql
SELECT COUNT(*) property_event_count, property 
FROM stage.user_events 
GROUP BY property 
ORDER BY 1 DESC
LIMIT 1;
```
` drinking | 224 `

iv. How many users were shown a Snapchat ad on July 3rd, 2019?

```sql
SELECT COUNT(DISTINCT(phone_id)) 
FROM stage.marketing_events 
WHERE UPPER(provider) = 'SNAPCHAT';
```
`261`

v. Which ad was shown the most to users who identify as moderates?

```sql
  SELECT  ad_id, COUNT(me.ad_id) ad_count 
   FROM stage.marketing_events me 
    INNER JOIN stage.user_events ue 
        ON me.phone_id = ue.phone_id 
   WHERE UPPER(property) = 'POLITICS' AND UPPER(ue.value) = 'MODERATE' 
   GROUP BY ad_id ORDER BY 2 DESC LIMIT 1;
```

```  
ad_id | ad_count 
-------+----------
     2 |        4
```

Since we have no information on how these ads are performing, the only metric we can use to compare the ads would be to count the number of times each ad was triggered or displayed to users. We can sub-divide this number by the ad provider to see how many times an ad has been triggered at each of the platforms. 

1. By pure count of the number of times each ad is triggered, we have the following as the top five ads

```sql
SELECT ad_id, count(*) 
FROM stage.marketing_events 
GROUP BY ad_id 
ORDER BY ad_id desc 
LIMIT 5;
```
```
 ad_id | count 
-------+-------
    22 |    13
    21 |    10
    20 |    15
    19 |    23
    18 |    23
```

2. By looking at the top ads for each platform/provider we have the following four rows as top ads for each platform


```sql
WITH ranked as (
    SELECT  ad_id, COUNT(me.ad_id) ad_count, provider, rank() over (partition by provider order by count(me.ad_id) DESC) as ranking 
    FROM stage.marketing_events me 
     INNER JOIN stage.user_events ue 
       ON me.phone_id = ue.phone_id 
   GROUP BY ad_id, provider  
   ORDER BY ranking, ad_count desc)
SELECT MIN(ranking) ranking, MAX(ad_id) ad_id, provider, MAX(ad_count) ad_count 
FROM ranked 
WHERE ranking <= 5 
GROUP BY provider 
ORDER BY ranking, ad_count DESC;

```

```
 ranking | ad_id | provider  | ad_count 
---------+-----+-----------+----------
       1 |   3 | Spotify   |       23
       1 |  15 | Facebook  |       15
       1 |   8 | Snapchat  |       14
       1 |  21 | Instagram |       13
```


