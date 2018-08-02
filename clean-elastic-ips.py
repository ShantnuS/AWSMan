#RELEASES ELASTIC IPS WHICH ARE NOT ASSIGNED TO ANY INSTANCE
import boto3

#Releases elastic IP specified by its allocation ID 
def release_elastic_IP(ec2, allocation_id):
    try:
        ec2.release_address(AllocationId=allocation_id)
        print("Released address: " + allocation_id)
    except:
        print("Could not release: " + allocation_id)

#Gets list of Elastic IPs
ec2 = boto3.client('ec2')

filters = [
    {'Name': 'domain', 'Values': ['vpc']}
]
ips = ec2.describe_addresses(Filters=filters)

#Releases IP is it doesn't have an instance associated to it
for ip in ips['Addresses']:
    if ip.get("InstanceId") is not None:
        print("Address %s is associatied with %s" % (str(ip.get('AllocationId')), str(ip.get('InstanceId'))))
    else:
        print("Address %s is associatied with Nothing!" % (str(ip.get('AllocationId'))))
        allocation_id = ip.get('AllocationId')
        release_elastic_IP(ec2, allocation_id)