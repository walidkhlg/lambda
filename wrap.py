import boto3, os, zipfile , argparse, datetime


current_time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

# zip lambda project folder
def lambdazip(path):
    zipname = 'serverless'+current_time+'.zip'
    newzip = zipfile.ZipFile(zipname, 'a')
    for root, dirs, files in os.walk(path):
        for i in files:
            newzip.write(os.path.join(root, i), i, zipfile.ZIP_DEFLATED)
    newzip.close()
    return zipname

# check test status ( fail / pass)
def check_tests():
    filename = run_tests()
    test_report_file = os.path.abspath(os.path.join(os.path.dirname(__file__), filename))
    with open(test_report_file, 'r') as test_report:
        data = test_report.read()
        print(data)
        if 'failed' in data or 'error' in data:
            return False
        return True

# run tests and write them in a log file
def run_tests():
    filename = "pytest_report"+current_time+".log"
    os.system('pytest test.py -v > ' + filename)
    return filename


parser = argparse.ArgumentParser(description='Wrap lambda to s3')
parser.add_argument('-p', '--path', help='Path to lambda poject folder', default='C:\\Users\\to124924\\PycharmProjects\\serverls')
parser.add_argument('-b', '--bucket', help='bucket name for lambda function', default='s3-lambda-walid')
params = parser.parse_args()

# run the tests , check if passed
if (check_tests()):
    print("Tests passed , Zipping lambda function")
    lambda_zip_file_name = lambdazip(params.path)
    session = boto3.Session(profile_name='compte-lab-26')
    s3 = session.client('s3')
    s3.upload_file(lambda_zip_file_name, params.bucket, lambda_zip_file_name)
else:
    print('Tests failed')
