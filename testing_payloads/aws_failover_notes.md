- create rds with multiple replicas
- create a bastion host
- create a bastion security group
- create an aurora security group
- create a bastion host
- use ssm to port forward the bastion host to your localhost - so you can access postgres as it was local

AWS_PROFILE=reddit_reader aws secretsmanager get-secret-value --secret-id=reddit_refresh_token

AWS_PROFILE=console_app_access_admin aws secretsmanager get-secret-value --secret-id=reddit_refresh_token

AWS_PROFILE=console_app_access_admin aws ec2 describe-instances

AWS_PROFILE=console_app_access_admin aws ssm start-session --target i-03f36d71c87fcd755 --region eu-central-1\

# if missing, install the session manager:
curl "https://s3.amazonaws.com/session-manager-downloads/plugin/latest/ubuntu_64bit/session-manager-plugin.deb" -o "session-manager-plugin.deb"
sudo dpkg -i session-manager-plugin.deb


# port forward postgres to your localhost through the bastion
see ./aws_rds_port_forward_failover_sequence.md


JEEZ, don't forget that the db instances need to be in the aurora security group


----

### logging on the bastion to see which one is the current write:
```shell
while sleep 5; do
    getent hosts rds-aurora-failover-1.cluster-cvi8qy2gksxh.eu-central-1.rds.amazonaws.com
done
#watch -n 5 getent hosts rds-aurora-failover-1.cluster-cvi8qy2gksxh.eu-central-1.rds.amazonaws.com
```