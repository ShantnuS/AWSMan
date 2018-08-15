#DELETES SECURITY GROUPS WHICH ARE NOT USED BY ANY INSTANCE
import boto3

print("AWSMan - Cleaning Security Groups!")
print("----------------------------------")

#Get the list of all security groups and instances
ec2resource = boto3.resource('ec2')
ec2client = boto3.client('ec2')

instances = list(ec2resource.instances.all())
sgs = ec2resource.security_groups.all()

#Delete a particular sg 
def delete_sg(ec2, sg_id):
    print("Deleting: " + sg_id)
    return ec2.delete_security_group(GroupId=sg_id)

#Remove sg's rules so it can be deleted 
def remove_sg_rules(ec2resource, ec2client, sg_id):
    print("Revoking rules for: " + sg_id)
    sg = ec2resource.SecurityGroup(sg_id)
    #Removes all rules from that security group and adds them to a list 
    try:
        response = sg.revoke_ingress(IpPermissions=sg.ip_permissions)
    except:
        print("Continuing...")

    return sg_id

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
revoked_sgs=[]

#Delete any unused security groups using IDs 
for sg in unused_sgs:
    #Need a try except block since some security groups are referenced by other groups rather than instances 
    try:
        response = delete_sg(ec2client, sg)
    except:
        print("Could not delete: " + sg + ", revoking rules!")
        sg_id = remove_sg_rules(ec2resource, ec2client, sg)
        revoked_sgs.append(sg_id)

if not revoked_sgs:
    print("Revoked list was empty!")
else:
    print("Removing from revoked list...")
    for sg in revoked_sgs:
        try:
            response = delete_sg(ec2client, sg)
        except:
            print("Could not delete: " + sg)

print("Deleted all groups that could have been deleted")
print("Remaining groups may be unused but are being referenced by other used groups")
print("DONE!")
