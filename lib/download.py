import sys
import boto3

s3 = boto3.client('s3')
s3.download_file('ace-of-diamonds', 'neural.model', sys.argv[1])
