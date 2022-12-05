import boto3

# these variables are going to be changing
# they can even transformed into events
open_rules = '0.0.0.0/0'

# exception handling variables
exFromPort = 'FromPort'
exToPort = 'ToPort'
fromPort = '22'
toPort = '22'
region = 'us-east-1'
ipProtocol = 'tcp'

ec2r = boto3.resource('ec2')
client = boto3.client('ec2')

response = client.describe_security_groups()

# function to delete wide open rules
# this is called from main method
def deleteRule(cidrIp, groupId, ipProtocol, fromPort, toPort):
    client.revoke_security_group_ingress(
        CidrIp=cidrIp,
        GroupId=groupId,
        IpProtocol=ipProtocol,
        FromPort=fromPort,
        ToPort=toPort
    )

# get a list of all instances
all_instances = [i for i in ec2r.instances.all()]

    #instances = ec2.instances.filter(Filters=filters)
    # get instances with filter with tag `Name`
instances = [i for i in ec2r.instances.filter(Filters=[{'Name':'tag:AcceptLooseSGRule', 'Values':['true']}])]

    # make a list of filtered instances IDs `[i.id for i in instances]`
    # Filter from all instances the instance that are not in the filtered list
instances_to_delete = [to_del for to_del in all_instances if to_del.id not in [i.id for i in instances]]

    # run over your `instances_to_delete` list and delete the loose security group rule
for instance in instances_to_delete:
    gid=instance.security_groups[0]['GroupId']
    for sg in response["SecurityGroups"]:
        # grab these variables so that they're sent to the revoke security group access
        groupId = sg['GroupId']
        groupName = sg['GroupName']
        if groupId == gid:
            groupId = gid
            for ip in sg['IpPermissions']:
            # there has to be an exception for security groups that don't have ports.
                if exFromPort in ip:
                    fromPort = ip['FromPort']
                    toPort = ip['ToPort']
                    for cidr in ip['IpRanges']:
                # identifying which rules contain a open_rules IP range
                        if cidr['CidrIp'] == open_rules:
                        # delete the rule
                            print("match")
                        deleteRule(cidr['CidrIp'], groupId, ipProtocol,
                                   fromPort, toPort)
