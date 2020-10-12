The data loader will extract csv files in the `./dataset` directory, perform some validation and transformation steps and load each csv into a table in the attached postgres database.

Any rows found to be invalid, will be dumped into `./dataset/invalid_data/` path to be looked at by a human to correct any errors and reload if possible. 

Ideally this data would be stored in s3 or any other cloud storage space so that it can be accessed by either a human or other processes that ingests this data.

To run the data loader, please follow the following steps:

#### Build Images
Run the following command in your terminal to build the __postgres__ and __data_loader__ docker images

```docker-compose build```

#### Run Containers

Once the build is over run the docker image which will bring up the postgres database and automatically execute the python command that loads marketing and user data

```docker-compose up```

#### Connect to Postgres database using `psql`

In order to run queries on the loaded data, you can connect to the database as follows

```psql -h localhost -p 5432 -U postgres  ad_events```

