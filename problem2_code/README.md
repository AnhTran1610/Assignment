## How to delete the  AWS security Group Ingress  rule  using boto3.

#### A security group acts as a virtual firewall for your EC2 instances to control incoming and outgoing traffic. Inbound rules control the incoming traffic to your instance, and outbound rules control the outgoing traffic from your instance. An inbound rule permits instances to receive traffic from the specified IPv4 or IPv6 CIDR address range, or from the instances associated with the specified security group.ss

#### The tf file create for easy test that script running on AWS cloud. It will scans over all the instances, and remove the loose rule from instances which does not have that special tag. And the following rule should be removed: Inbound 0.0.0.0/0 on port 22
-------------

**Files:** 
```
    rm_loose_securitygroup_rule.py.py
```

## Apply the script

1. First configure the aws credentials using aws-cli.

        aws configure

2. Now, from the current directory run the following command to validate the script.

        python3 rm_loose_securitygroup_rule.py
