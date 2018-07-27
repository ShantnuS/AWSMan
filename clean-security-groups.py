import boto3

ec2 = boto3.resource('ec2', region_name="eu-west-1")

instances = list(ec2.instances.all())
sgs = ec2.security_groups.all()

all_sgs=[]
for sg in sgs:
    all_sgs.append(sg.group_id)
#print(str(all_sgs))
print("")

used_sgs=[]
for instance in instances:
    for sg in instance.security_groups:
        used_sgs.append(sg['GroupId'])
#print(str(used_sgs))
print("")

unused_sgs=[x for x in all_sgs if x not in used_sgs]
print("")
#print(str(unused_sgs))

ec2 = boto3.client('ec2')

for sg in unused_sgs:
    print("Deleting: " + sg)
    #Need a try except block since some security groups are referenced by other groups rather than instances 
    try:
        response = ec2.delete_security_group(GroupId=sg)
    except:
        print("Could not delete: " + sg)
