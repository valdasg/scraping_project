variable "aws-region" {
    description = "AWS region to create resources"
    default     = "eu-central-1"
}

variable "bucket-prefix" {
    type        = string
    description = "Creates unique bucket name"
    default     = "talent-lab"
}

variable "versioning" {
    type        = bool
    description = "(optional) State of versioning"
    default    = "true"
}

variable "acl" {
    type        = string
    description = "Defaults to private"
    default     = "private"
}

variable "ami" {
    type = string
    description = "ami configuration"
    default = "ami-065deacbcaac64cf2"
}

variable "instance-type" {
    type = string
    description = "Scraper"
    default = "c6g.xlarge"
}

variable "public-key" {
    type = string
    description = "Public key name"
    default = "ssh-connect"
}