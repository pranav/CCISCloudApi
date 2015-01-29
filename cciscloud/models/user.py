from cciscloud.providers.s3 import S3Provider


class User():
    def __init__(self, username):
       self.username = username

    @property
    def total_cost(self):
        s3 = S3Provider()
        _cost = 0.0
        for row in s3.get_detailed_costs():
            if row['user:creator'] == self.username:
                _cost += float(row['Cost'])
        return _cost