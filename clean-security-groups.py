#DELETES SECURITY GROUPS WHICH ARE NOT USED BY ANY INSTANCE
import boto3

print("AWSMan - Cleaning Security Groups!")
print("----------------------------------")

#Get the list of all security groups and instances
ec2 = boto3.resource('ec2')

instances = list(ec2.instances.all())
sgs = ec2.security_groups.all()

#Make a list of sg ids 
all_sgs=[]
for sg in sgs:
    all_sgs.append(sg.group_id)

#Make a list of used sg ids 
used_sgs=[]
for instance in instances:
    for sg in instance.security_groups:
        used_sgs.append(sg['GroupId'])

#Make a list of unused sg ids from all - used
unused_sgs=[x for x in all_sgs if x not in used_sgs]

#Delete any unused security groups using IDs 
ec2 = boto3.client('ec2')
for sg in unused_sgs:
    print("Deleting: " + sg)
    #Need a try except block since some security groups are referenced by other groups rather than instances 
    try:
        response = ec2.delete_security_group(GroupId=sg)
    except:
        print("Could not delete: " + sg)
