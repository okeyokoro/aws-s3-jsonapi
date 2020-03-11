
### USEFUL LINKS

Quick Start
https://github.com/aws-samples/aws-modern-application-workshop/tree/python-cdk/module-2#creating-the-core-infrastructure-using-the-aws-cdk

Clear
https://www.youtube.com/watch?v=bGDMeD6kOz0

Clearer
https://www.youtube.com/watch?v=hiKPPy584Mg

Clearest
https://www.youtube.com/watch?v=LX5lHYGFcnA

### NOTES

Think of a VPC (Virtual Private Cloud) as a networking abstraction for isolating
**separate projects** within an AWS account. You basically get a
**mini-AWS** (**datacenter-network** in **a region**) for **every project** you embark on.

You get a default VPC the moment you sign up for an AWS account.

A VPC must live within a Region

Within a VPC/Region you can have multiple Subnets/Availability-Zones

Each Resource within a Subnet/Availability-Zone is shrouded by a Security-Group

You connect Resources by connecting Security-Groups

You can also nest multiple Resources (across Subnets/AZs) within a single Security-Group

You cannot reach a Resource unless it's Security Group lets you

---

Within a Subnet, Resources are given internal IP addresses
Resources within a Subnet talk to each other using the internal IP addresses

You can also map certain internal IP addresses to **public** IP addresses
to make your Resources available through the internet
^ You do this mapping at the VPC layer
^ the specific Entity that controls this process at the VPC layer is the **Internet Gateway**

---

A convenient way to have Resources that are **reachable from the internet**
connected to Resources that **are NOT reachable from the internet**
without having to do a lot of networking configuration:

Is to have **public subnets** and **private subnets**
(NOTE: by default a Subnet is neither public nor private; each usecase require configuration)

You keep your webservers, api gateway, lambdas in the **public subnet**

and your data: s3, rds from the **private subnet**

#### SUBNET CONCEPTS

Subnet: Public|Private , Availability Zone

Public|Private: for security

Availability Zone: for adding redundancy/fault-tolerance/high-availabilit
to your architecture (AZs are independent of each other)

---

A lot of times you want to have your **private subnets** (which aren't reachable from the internet)
connect to the internet to install software updates etc.
You can do this through a **NAT Gateway** (offered by AWS; it only allows responses to requests made from within the subnet)

---

Security Groups work as Firewalls at the Resource level
NACLs (Network Access Control Lists) work as Firewalls at the Subnet level
Favor Security Groups over NACLs
Keep NACLs short if you must use them

### ADVANCED

You can connect VPCs!

**You can connect VPCs across multiple regions!**
This lets you have a datacenter-network in multiple regions
(1 VPC/datacenter-network in US, another VPC/datacenter-network in Europe, etc)
This would let a multi-national company effectively serve users in different regions

**You can connect VPCs across AWS Accounts**
If your company gets acquired; you can connect your companies VPC to your acquirers' VPC!

NOTE: while connecting VPCs, make sure the CIDR ranges of the two VPCs are not overlapping

There are two ways to connect VPCs:

- VPC Peering; direct connection between VPCs (NOTE: A VPC can only have 25 peers)

- Transit Gateway; all VPCs communicate through a centralized service (NOTE: VPCs must be in the same region (for now) )



https://www.youtube.com/watch?v=8K7GZFff_V0

https://www.youtube.com/watch?v=rQvl-V3tLiQ

https://www.youtube.com/watch?v=fnxXNZdf6ew

https://www.youtube.com/watch?v=jZAvKgqlrjY

https://www.youtube.com/watch?v=7acKgdDOOu4

https://www.youtube.com/watch?v=8C9xNVYbCVk

https://www.youtube.com/watch?v=-mL3zT1iIKw

https://www.youtube.com/watch?v=0QS1TWLooo0

https://www.youtube.com/watch?v=95nfMj4PVDA

https://www.youtube.com/watch?v=vbyjpMeYitA

https://www.youtube.com/watch?v=RY9ERVyNsyI

https://www.youtube.com/watch?v=dv7fpOIkiRU

