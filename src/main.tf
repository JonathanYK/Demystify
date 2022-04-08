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
  instance_id   = aws_instance.sessions-instance-tf6.id
  allocation_id = aws_eip.sessions-eip-tf.id

}

resource "aws_instance" "sessions-instance-tf6" {
  ami           = "ami-04505e74c0741db8d"
  instance_type = "t2.micro"
  key_name      = "sessions-ami-ubuntu"
  subnet_id     = aws_subnet.sessions-sn-tf.id

  tags = {
    Name      = "sessions-instance-tf6"
    ManagedBy = "terraform"
  }

}


#############################################################################

# create the ALB
resource "aws_alb" "sessions-alb-tf" {
  load_balancer_type = "application"
  name = "sessions-alb-tf"
  subnets = aws_subnet.sessions-sn-tf.*.id
  security_groups = [aws_security_group.sessions-sg-tf.id]
}



# point redirected traffic to the app
resource "aws_alb_target_group" "sessions-target-group-tf" {
  name = "sessions-target-group-tf"
  port = 80
  protocol = "HTTP"
  vpc_id = aws_vpc.sessions-vpc-tf.id
  target_type = "ip"
}



# direct traffic through the ALB
resource "aws_alb_listener" "sessions-alb-listener-tf" {
  load_balancer_arn = aws_alb.sessions-alb-tf.arn
  port = 80
  protocol = "HTTP"
  default_action {
    target_group_arn = aws_alb_target_group.sessions-target-group-tf.arn
    type = "forward"
  }
}


# random string for flask secret-key env variable
resource "random_string" "sessions-flask-secret-key-tf" {
  length = 16
  special = true
  override_special = "/@\" "
}


# create the ECS cluster
resource "aws_ecs_cluster" "sessions-ecs-cluster-tf" {
  name = "flask-app"

  tags = {
    Name = "sessions-ecs-cluster-tf"
  }
}


variable "flask_app_image" {
  description = "Dockerhub image for flask-app"
  default = "docker.io/doodmanbro/flask-app:0.1.0"
}

variable "flask_app" {
  description = "FLASK APP variable"
  default = "app"
}

variable "flask_env" {
  description = "FLASK ENV variable"
  default = "production"
}

variable "app_home" {
  description = "APP HOME variable"
  default = "flask-postgres/src/"
}


variable "flask_app_port" {
  description = "Port exposed by the flask application"
  default = 8080
}


# create and define the container task
resource "aws_ecs_task_definition" "sessions-ecs-task-tf" {
  family = "flask-app"
  #requires_compatibilities = ["FARGATE"]
  network_mode = "awsvpc"
  cpu = 512
  memory = 2048
  container_definitions = <<DEFINITION
[
   {
      "name":"flask-app",
      "image":"${var.flask_app_image}",
      "essential":true,
      "portMappings":[
         {
            "containerPort":8080,
            "hostPort":8080,
            "protocol":"tcp"
         }
      ],
      "environment":[
         
         {
            "name":"FLASK_APP",
            "value":"${var.flask_app}"
         },
         {
            "name":"FLASK_ENV",
            "value":"${var.flask_env}"
         },
         {
            "name":"APP_HOME",
            "value":"${var.app_home}"
         },
         {
            "name":"APP_PORT",
            "value":"${var.flask_app_port}"
         },
         {
            "name":"APP_SECRET_KEY",
            "value":"${random_string.sessions-flask-secret-key-tf.result}"
         }
      ]
   }
]
DEFINITION
}


resource "aws_ecs_service" "sessions-flask-service-tf" {
  name = "flask-app-service"
  cluster = aws_ecs_cluster.sessions-ecs-cluster-tf.id
  task_definition = aws_ecs_task_definition.sessions-ecs-task-tf.arn
  desired_count = 2
  launch_type = "FARGATE"

  network_configuration {
    security_groups = [aws_security_group.sessions-sg-tf.id]
    subnets = aws_subnet.sessions-sn-tf.*.id
    assign_public_ip = true
  }

  load_balancer {
    container_name = "flask-app"
    container_port = var.flask_app_port
    target_group_arn = aws_alb_target_group.sessions-target-group-tf.id
  }

  depends_on = [
    aws_alb_listener.sessions-alb-listener-tf
  ]
}



#############################################################################

resource "aws_eip" "sessions-eip-tf" {
  vpc        = true
  instance   = aws_instance.sessions-instance-tf6.id
  depends_on = [aws_internet_gateway.sessions-gw-tf]


}



output "instance_public_dns" {
  description = "The public_ip and public_dns for logging in to the instance."
  value       = "public_ip = ${aws_instance.sessions-instance-tf6.public_ip}, and public_dns = ${aws_instance.sessions-instance-tf6.public_dns}"
}





# Deploy the project on instance!

# make the output to be the url to use the project(lunch the instance)
