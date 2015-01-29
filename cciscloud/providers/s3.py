import io
import csv
import boto
import zipfile
import cStringIO
from cciscloud import config


class S3Provider():
    def __init__(self, aws_acccess_key_id=config.AWS_ACCESS_KEY, aws_secret_access_key_id=config.AWS_SECRET_KEY):
        self.conn = boto.connect_s3(aws_access_key_id=aws_acccess_key_id, aws_secret_access_key=aws_secret_access_key_id)

    def get_detailed_costs(self):
        """
        Get the details cost csv file
        :return: csv.DictReader
        """
        #TODO: Generate path to cost csv
        csv_file = '906142011005-aws-billing-detailed-line-items-with-resources-and-tags-2015-01.csv'
        stringio = cStringIO.StringIO(self.get_file_contents(config.BILLING_BUCKET, "/%s.zip" % csv_file))
        raw_csv = io.TextIOWrapper(zipfile.ZipFile(stringio).open(csv_file))
        return csv.DictReader(raw_csv)

    def get_file_contents(self, bucket, path):
        return self.conn.get_bucket(bucket).get_key(path).get_contents_as_string()
