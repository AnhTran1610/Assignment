// Generate the SSH keypair that we’ll use to configure the EC2 instance.
// After that, write the private key to a local file and upload the public key to AWS
resource "tls_private_key" "key" {
  algorithm = "RSA"
}
resource "local_file" "private_key" {
  filename          = "TEST.pem"
  sensitive_content = tls_private_key.key.private_key_pem
  file_permission   = "0400"
}
resource "aws_key_pair" "key_pair" {
  key_name   = "TEST"
  public_key = tls_private_key.key.public_key_openssh
}
