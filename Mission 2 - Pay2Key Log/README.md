# Parsing log.txt for a client
* **Author**: Robert Yonatan Tiger
* **Parsed File Name**: log.txt

## Objectives:
  1. How many users are in the file?
  2. How many of them are active users?
  3. A list of active users with their related groups in the following format:
   > User:\<username\>|Groups:\<all_groups\>

### 1) How many users are in the file?
1. Using `cat` with `grep` on the pattern **"User name"** will output only the line that has **"User name"** in it like so:
  `User name                    zw85313`
2. Piping to `wc -l` will output the number of rows:
  * `cat log.txt | grep "User name" | wc -l`
    * **Output:**
      `9524`</br>
  There are **9524** users in the file.

### 2) How many of them are active users?
The file has the line of "Account active" followed by a "Yes" or "No" to determine wheter a user is active or not.
1. Again, using `cat` and `grep` with the pattern **"Account active"** will output the line that states wheter the user is active:
  * `cat log.txt | grep "Account active"`
    * **Output:**
      > Account active               No</br>
      > Account active               Yes
2. Filter to see only the the "Yes\No" column with `awk`:
  * `cat log.txt | grep "Account active" | awk '{print $3}'`

3. `grep` only "Yes" pattern:
  * `cat log.txt | grep "Account active" | awk '{print $3}' | grep Yes`

4. Pipe into `wc -l` to have the exact numbers of "Yes" in the row that matches "Account active" pattern:
  * `cat log.txt | grep "Account active" | awk '{print $3}' | grep Yes | wc -l`
    * **Output:**
      > 4216
  The file has **4216** users with active accounts.

### 3) A list of active users with their related groups in the following format:
   > User:\<username\>|Groups:\<all_groups\>

   Check `log_parser_script.py` to see how it's done.
   In the attached `parsed_log.txt` are all the users and groups in the requested format.