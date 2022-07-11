## Security infrastructure
## User setup
its not a good practice to run applications in production environment as root, thus I am creating a user 'valdas' to have a separate access to application to be developed. For convenience in development, I am assigning administrator rights.

[user_creation](images/user_creation.png)

Since I will be running different AWS applications I am creating policies for the roles to be used, i.e. s3 read/write, some policies are AWS created.

[s3_policy](images/s3_policy.png)

I am also creating a Glue and Lambda roles to be asigned to running applications:

[roles](images/roles.png)