import boto3
import yaml
from optparse import OptionParser

def main():
    parser = OptionParser(usage="usage: %prog [options] filename",
                          version="%prog 1.0")
    parser.add_option("--beanstalk_app_name",
                      dest="eb_app",
                      default=False,
                      help="Single or All")
    parser.add_option("--beanstalk_env_name",
                      dest="eb_env",
                      default=False,
                      help="Single or All")
    (options, args) = parser.parse_args()
    print options
    if options.eb_app is False or options.eb_env is False:
        print("It mandatory to Pass options --beanstalk_app_name , --beanstalk_env_name")
        print("Exiting")
        exit()
    else:
        client = boto3.client('elasticbeanstalk')

        response = client.describe_configuration_settings(ApplicationName=options.eb_app, EnvironmentName=options.eb_env)

        env_variables = ''
        for setting in response['ConfigurationSettings'][0]['OptionSettings']:
            if setting['OptionName'] == 'EnvironmentVariables':
                env_variables = setting['Value']
                break


        env_variables_list = env_variables.split(',')

        env_variables_dict = []
        for var in env_variables_list:
            vars = var.split('=')
            env_variables_dict.append({ 'name': vars[0], 'value': vars[1]})


        with open('/tmp/result.yml', 'w') as yaml_file:
            yaml.dump(env_variables_dict,yaml_file,default_flow_style=False)

        print("OutPut YAML at PATH /tmp/result.yml")


if __name__ == '__main__':
    main()
