terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.6.0"
    }
  }
}

provider "aws" {
  profile = "default"
  region  = "us-east-1"
}


resource "aws_vpc" "sessions-vpc-tf" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true

  tags = {
    Name      = "sessions-vpc-tf"
    ManagedBy = "terraform"
  }
}

resource "aws_internet_gateway" "sessions-gw-tf" {
  vpc_id = aws_vpc.sessions-vpc-tf.id

  tags = {
    Name      = "sessions-gw-tf"
    ManagedBy = "terraform"
  }
}

resource "aws_route_table" "sessions-rt-tf" {
  vpc_id = aws_vpc.sessions-vpc-tf.id

  tags = {
    Name      = "sessions-rt-tf"
    ManagedBy = "terraform"
  }

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.sessions-gw-tf.id
  }
}

resource "aws_route_table_association" "sessions-associ-rt-tf" {
  subnet_id      = aws_subnet.sessions-sn-tf.id
  route_table_id = aws_route_table.sessions-rt-tf.id
}

resource "aws_subnet" "sessions-sn-tf" {
  vpc_id     = aws_vpc.sessions-vpc-tf.id
  cidr_block = "10.0.1.0/24"

  tags = {
    Name      = "sessions-sn-tf"
    ManagedBy = "terraform"
  }
}

resource "aws_network_acl" "sessions-acl-tf" {
  vpc_id     = aws_vpc.sessions-vpc-tf.id
  subnet_ids = [aws_subnet.sessions-sn-tf.id]

  egress {
    protocol   = "-1"
    rule_no    = 210
    action     = "allow"
    cidr_block = "0.0.0.0/0"
    from_port  = "0"
    to_port    = "0"
  }

  ingress {
    protocol   = "-1"
    rule_no    = 210
    action     = "allow"
    cidr_block = "0.0.0.0/0"
    from_port  = "0"
    to_port    = "0"
  }

  tags = {
    Name      = "sessions-acl-tf"
    ManagedBy = "terraform"
  }
}

resource "aws_security_group" "sessions-sg-tf" {
  vpc_id = aws_vpc.sessions-vpc-tf.id

  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  ingress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  tags = {
    Name      = "sessions-sg-tf"
    ManagedBy = "terraform"
  }
}

resource "aws_eip_association" "sessions-eip_assoc-tf" {
  instance_id   = aws_instance.sessions-instance-tf7.id
  allocation_id = aws_eip.sessions-eip-tf.id
}

resource "aws_instance" "sessions-instance-tf7" {
  #ami           = "ami-04505e74c0741db8d"
  ami           = "ami-0dbf783f8193d25f3"
  instance_type = "t2.micro"
  key_name      = "sessions-ami-ubuntu"
  subnet_id     = aws_subnet.sessions-sn-tf.id

  tags = {
    Name      = "sessions-instance-tf7"
    ManagedBy = "terraform"
  }
}

resource "aws_eip" "sessions-eip-tf" {
  vpc        = true
  instance   = aws_instance.sessions-instance-tf7.id
  depends_on = [aws_internet_gateway.sessions-gw-tf]
}

output "instance_public_dns" {
  description = "The public_ip and public_dns for logging in to the instance."
  value       = "public_ip = ${aws_instance.sessions-instance-tf7.public_ip}, and public_dns = ${aws_instance.sessions-instance-tf7.public_dns}"
}

