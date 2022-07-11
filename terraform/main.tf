terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.1.7"
}

# add provider and credentials
provider "aws" {
  region  = var.aws-region
  shared_config_files      = ["~/.aws/config"]
  shared_credentials_files = ["~/.aws/credentials"]
}

# add EC2  instance
resource "aws_instance" "ec2_server" {
  ami           = var.ami
  instance_type = var.instance-type
  key_name = var.public-key

  tags = {
    Name = "Scraper"
  }
}

# add bucket
resource "aws_s3_bucket" "my_s3_bucket" {
    bucket_prefix = var.bucket-prefix
     acl = var.acl
     versioning {
       enabled = var.versioning
     }     
  
}
