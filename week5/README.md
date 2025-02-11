
# 😎 Task 2: Create database and table in your MySQL server
  

1. Create a new database named website.<br>
![task2-1_a](./imgs/task2/task2-1_a.png)<br>
![task2-1_b](./imgs/task2/task2-1_b.png)<br>
2. Create a new table named member, in the website database, designed<br> 
![task2-2_a](./imgs/task2/task2-2_a.png)<br>
![task2-2_a](./imgs/task2/task2-2_b.png)<br>
  

# 😎 Task 3: SQL CRUD
  

1. INSERT a new row to the member table where name, username and password must be set to test. INSERT additional 4 rows with arbitrary data.<br>
![task3-1_a](./imgs/task3/task3-1_a.png)<br>
![task3-1_b](./imgs/task3/task3-1_b.png)<br>
![task3-1_c](./imgs/task3/task3-1_c.png)<br>
2. SELECT all rows from the member table.<br>
![task3-2](./imgs/task3/task3-2.png)<br>
3. SELECT all rows from the member table, in descending order of time.<br>
![task3-3](./imgs/task3/task3-3.png)<br>
4. SELECT total 3 rows, second to fourth, from the member table, in descending order of time. Note: it does not mean SELECT rows where id are 2, 3, or 4.<br>
![task3-4](./imgs/task3/task3-4.png)<br>
5. SELECT rows where username equals to test.<br>
![task3-5](./imgs/task3/task3-5.png)<br>
6. SELECT rows where name includes the es keyword.<br>
![task3-6](./imgs/task3/task3-6.png)<br>
7. SELECT rows where both username and password equal to test.<br>
![task3-7](./imgs/task3/task3-7.png)<br>
8. UPDATE data in name column to test2 where username equals to test.<br>
![task3-8](./imgs/task3/task3-8.png)<br>
  
    

# 😎 Task 4: SQL Aggregation Functions
  

1. SELECT how many rows from the member table.<br>
![task4-1](./imgs/task4/task4-1.png)<br>
2. SELECT the sum of follower_count of all the rows from the member table.<br>
![task4-2](./imgs/task4/task4-2.png)<br>
3. SELECT the average of follower_count of all the rows from the member table.<br>
![task4-3](./imgs/task4/task4-3.png)<br>
4. SELECT the average of follower_count of the first 2 rows, in descending order of follower_count, from the member table.<br>
![task4-4](./imgs/task4/task4-4.png)<br>


# 😎 Task 5: SQL JOIN
  
  
1. Create a new table named message, in the website database. designed as below: <br>
![task5-1_a](./imgs/task5/task5-1_a.png)<br>
![task5-1_b](./imgs/task5/task5-1_b.png)<br>
2. SELECT all messages, including sender names. We have to JOIN the member table to get that.<br>
![task5-2](./imgs/task5/task5-2.png)<br>
3. SELECT all messages, including sender names, where sender username equals to test. We have to JOIN the member table to filter and get that.<br>
![task5-3](./imgs/task5/task5-3.png)<br>
4. Use SELECT, SQL Aggregation Functions with JOIN statement, get the average like count of messages where sender username equals to test.<br>
![task5-4](./imgs/task5/task5-4.png)<br>
5. Use SELECT, SQL Aggregation Functions with JOIN statement, get the average like count of messages GROUP BY sender username.<br>
![task5-5](./imgs/task5/task5-5.png)<br>
