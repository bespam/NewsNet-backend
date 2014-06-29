import time
import paramiko
import pdb
import urllib2
#location of the boto config
import os
os.environ["BOTO_CONFIG"]='C:/Dropbox/AWS/.boto'

import boto
from boto.ec2.blockdevicemapping import BlockDeviceType, BlockDeviceMapping
#connecting to the AWS s3
#s3 = boto.connect_s3()
#bucket = s3.get_bucket('aws-publicdatasets')
#k = bucket.get_key("common-crawl/parse-output/valid_segments.txt")
#s = k.get_contents_as_string()
#list = s.split("\n")

#connecting to the AWS ec2
ec2 = boto.connect_ec2()
xvdb = BlockDeviceType()
xvdb.ephemeral_name='ephemeral0'
bdm = BlockDeviceMapping()
bdm['/dev/xvdb'] = xvdb
image_id = 'ami-fb8e9292'
image_name = 'Amazon Linux AMI 2014.03.1'
new_reservation = ec2.run_instances(image_id=image_id, key_name='ec2-key', security_groups=['web'], instance_type='m1.small', block_device_map=bdm)

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
#stdin, stdout, stderr = ssh.exec_command('cd /media/ephemeral0')
#print stdout.readlines(), stderr.readlines()
pdb.set_trace()
#ssh to server and sudo chmod 777 /media/ephemeral0 and sudo yum install python27
stdin, stdout, stderr = ssh.exec_command('mkdir /media/ephemeral0/wdc')
print stdout.readlines(), stderr.readlines()
#mount drive
#stdin, stdout, stderr = ssh.exec_command('sudo mount -t xfs /dev/xvda1 ~/wdc')
print stdout.readlines(), stderr.readlines()
#aws configure
stdin, stdout, stderr = ssh.exec_command('aws configure')
stdin.write(boto.config.get_value('Credentials', 'aws_access_key_id')+"\n")
stdin.write(boto.config.get_value('Credentials', 'aws_secret_access_key')+"\n")
stdin.write("\n")
stdin.write("\n")
print stdout.readlines(), stderr.readlines()
#copy index_process.py
sftp = ssh.open_sftp()
sftp.put('index_process.py','/media/ephemeral0/wdc/index_process.py' )
print "index_process.py copied successfully!"
#copy data from S3
stdin, stdout, stderr = ssh.exec_command('aws s3 cp s3://wdc-weighted-graph/index-out/index-temp3.gz/part-temp3-0.gz /media/ephemeral0/wdc --recursive')
print stdout.readlines(), stderr.readlines()
stdin, stdout, stderr = ssh.exec_command('aws s3 cp s3://wdc-weighted-graph/index-out/index-temp3.gz/part-temp3-2.gz /media/ephemeral0/wdc --recursive')
print stdout.readlines(), stderr.readlines()
pdb.set_trace()
ec2.terminate_instances(instance_ids=[instance])
