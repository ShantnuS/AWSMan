import boto3

def delete_elastic_IP(ec2, allocation_id):
    try:
        ec2.release_address(AllocationId=allocation_id)
        print("Released address: " + allocation_id)
    except:
        print("Could not release: " + allocation_id)


ec2 = boto3.client('ec2')

filters = [
    {'Name': 'domain', 'Values': ['vpc']}
]
ips = ec2.describe_addresses(Filters=filters)

for ip in ips['Addresses']:
    if ip.get("InstanceId") is not None:
        print("Address %s is associatied with %s" % (str(ip.get('AllocationId')), str(ip.get('InstanceId'))))
    else:
        print("Address %s is associatied with Nothing!" % (str(ip.get('AllocationId'))))
        allocation_id = ip.get('AllocationId')
        delete_elastic_IP(ec2, allocation_id)