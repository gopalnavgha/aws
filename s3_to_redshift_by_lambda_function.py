import json
import psycopg2
import os

def lambda_handler(event, context):
    print("event collected is {}".format(event))
    for record in event['Records']:
        s3_bucket = record['s3']['bucket']['name']        
        s3_key = record['s3']['object']['key']        
        from_path = "s3://{}/{}".format(s3_bucket, s3_key)
        print("from path {}".format(from_path))
        Access_key = os.getenv('AWS_Access_key')
        Access_Secrete = os.getenv('AWS_Access_Secrete')
        dbname = os.getenv('dbname')
        host = os.getenv('host')
        user = os.getenv('user')
        password = os.getenv('password')
        tablename = os.getenv('tablename')
        connection = psycopg2.connect(dbname = dbname,
                                       host = host,
                                       port = '5439',
                                       user = user,
                                       password = password)                                       
        
        curs = connection.cursor()        
        querry = "COPY {} FROM '{}' CREDENTIALS 'aws_access_key_id={};aws_secret_access_key={}' CSV IGNOREHEADER 1;".format(tablename,from_path,Access_key,Access_Secrete)
        print("query is {}".format(querry))        
        curs.execute(querry)
        connection.commit()       
        curs.close()       
        connection.close()
