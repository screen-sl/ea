# Getting Started

To get started, you need to have docker and docker-compose installed locally. 
docker-compose also attaches a single volume to the drill container so that `core-site.xml` 
can be loaded in with AWS secrets

Another container is created for the purpose of running the management commands that
have been implemented in Python. The following volumes are attached to the container: `data/` and 
`data-fixed/`. The management commands are accessible by running: 

`make dev-bash`

# Configure PRIVATE.txt

In `docker-env/PRIVATE.txt` place AWS secrets. The AWS secrets are stored in 2 locations, PRIVATE.txt 
and core-site.xml. This is not DRY and should be reviewed.

```
AWS_ACCESS_KEY_ID=xxxxx
AWS_SECRET_ACCESS_KEY=xxxxx
```

# Configure core-site.xml

Loaded in by docker-compose volume from `docker/drill/core-site.xml` 

```<configuration>

<property>
  <name>fs.s3.endpoint</name>
  <value>s3-eu-west-1.amazonaws.com</value>
</property>

<property>
  <name>fs.s3a.access.key</name>
  <value>xxxxxxxx</value>
</property>

<property>
  <name>fs.s3a.secret.key</name>
  <value>xxxxx</value>
</property>

</configuration>
```
# Bring Up Stack

`make stack-full-refresh`

This will build the images and start the drill container. Once running, it should be accessible locally 
at http://localhost:8047

# Setup drill to set global configuration

`make setup-drill`

We need to update some of the default options 
`store.format='jsonlines'` and `store.json.read_numbers_as_double=true`

# Create Storage Plugin

First conect to the dev container.

`make dev-bash`

Then run the management command to create the Storage Plugin, overriding the defaults.

`ealpha create-s3-storage-plugin --name s3testing --bucket sstestingbucket`

# Create S3 bucket

First conect to the dev container.

`make dev-bash`

Then run the management command to create bucket in S3.

`ealpha create-s3-bucket --bucket simonstestingbucket123`

# Clean up malformed JL files

It was observed that some of the input files were malformed. The following command
will expect an `data/` with the uncompressed jl files and `data-fixed` directory 
where the corrected files will be written.

`make fix-malformed-jl`

# Upload files to S3

First conect to the dev container.

`make dev-bash`

To upload the files that were cleaned run the following:

`ealpha load-file-to-s3 --bucket sstesting`

# Run A Query in drill

Once data is loaded, it should be possible 
to run the default query in drill. 

`make query-drill`

The default query will just log response code for now.

# Additional Queries

To run custom queries, run the following make target to get into the container.

`make dev-bash`

The query below will write to the `write` workspace in `s3` storage-plugin:

```ealpha query-drill --query 'CREATE TABLE `s3`.`write`.`20170131/20170131-bestbuy.jl` AS SELECT * FROM `s3`.`read`.`20170131/20170131-bestbuy.jl` LIMIT 10'```

# Tasks

## Part 4

Step 4: Place the sample file in the S3 bucket. Write a query to return the results for the file 
in the 20170131 folder the file is called 20170131-bestbuy.jl 

```ealpha query-drill --query 'SELECT * FROM `s3`.`read`.`20170131/20170131-bestbuy.jl`'```

## Part 5

Step 5: Write a query to return all rows from all files that have a “quarter” of “2016-Q4”

```ealpha query-drill --query 'SELECT * FROM `s3`.`read`.`20161*/*.jl`'```

## Part 6

Step 6: Export the results of Step 5 into a JSONLines table.

```ealpha query-drill --query 'CREATE TABLE s3.`write`.`2016Q4` AS SELECT * FROM `s3`.`read`.`20161*/*.jl`'```

# Gotchas
Ensure that there is an object with the desired key prefix for the schemas referenced in the S3 plugin 
otherwise you will get errors when you attempt to write to it. 