import time
import paramiko
import pdb
import urllib2
#location of the boto config
import os
os.environ["BOTO_CONFIG"]='C:/Dropbox/AWS/.boto'

import boto
#connecting to the AWS s3
#s3 = boto.connect_s3()
#bucket = s3.get_bucket('aws-publicdatasets')
#k = bucket.get_key("common-crawl/parse-output/valid_segments.txt")
#s = k.get_contents_as_string()
#list = s.split("\n")

#connecting to the AWS ec2
ec2 = boto.connect_ec2()
image_id = 'ami-fb8e9292'
image_name = 'Amazon Linux AMI 2014.03.1'
new_reservation = ec2.run_instances(image_id=image_id, key_name='ec2-key', security_groups=['web'], instance_type='t1.micro')

instance = new_reservation.instances[0]

# Wait a minute or two while it boots
print "Spinning up instance for '%s' - %s. Waiting for it to boot up." % (image_id, image_name)
while instance.state != 'running':
    print ".",
    time.sleep(1)
    instance.update()
print " "
print "Instance is running, ip: %s" % instance.ip_address
print "Waiting until status checks"

#print "Connecting to %s as user %s" % (instance.ip_address, 'ubuntu')
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
while True:
    try:
        ssh.connect(instance.ip_address, username='ec2-user', key_filename='ec2-key.pem')
        break
    except:
        time.sleep(5)
        print ".",
        pass
    
#make dir
stdin, stdout, stderr = ssh.exec_command('mkdir wdc')
print stdout.readlines(), stderr.readlines()
#aws configure
stdin, stdout, stderr = ssh.exec_command('aws configure')
stdin.write(boto.config.get_value('Credentials', 'aws_access_key_id')+"\n")
stdin.write(boto.config.get_value('Credentials', 'aws_secret_access_key')+"\n")
stdin.write("\n")
stdin.write("\n")
print stdout.readlines(), stderr.readlines()
#download arcs file
response = urllib2.urlopen('http://webdatacommons.org/hyperlinkgraph/data/arc.list.txt')
i = 0
for line in response:
    if i < 36:
        i = i +1
        continue
    file = line.strip('\n')
    print file
    #download file
    stdin, stdout, stderr = ssh.exec_command('wget -q -T90 '+file + ' -P wdc')
    print stdout.readlines()
    
    #copy to S3
    stdin, stdout, stderr = ssh.exec_command('aws s3 cp wdc s3://wdc-weighted-graph/arcs --recursive')
    print stdout.readlines(), stderr.readlines()
    
    #remove file once copied
    stdin, stdout, stderr = ssh.exec_command('rm wdc/*')
    print stdout.readlines(), stderr.readlines()
    
    #ssh.close()
ec2.terminate_instances(instance_ids=[instance.id])
