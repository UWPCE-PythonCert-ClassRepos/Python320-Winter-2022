# Timing Results

## Loading users file:

`accounts.csv`: 2000 users

### insert_one()

Using the old code with many calls to insert_one():

load_users took: 1.32 seconds

### insert_many()

Using the new code with one call to insert_many():

load_users_many took: 0.15 seconds

### insert_many() -- chunked

500 record chunks

load_users_mp took: 0.28 seconds

### insert_many_threading()

Using the new code with one call to insert_many():

load_users_many took: 0.22 seconds

 -- slower with threads -- 4 chunks / threads


## Loading status updates file:

`status_updates.csv`: 20,000 status updates

### updateone()

Using the old code with many calls to update_one():

load_status took: 368.46 seconds -- painfully long!

### update_many()

I coudln't figure out how to use update_many

load_status_many took:

