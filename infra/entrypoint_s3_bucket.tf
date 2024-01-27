resource "aws_s3_bucket" "example" {
  bucket = "entrypoint-file-storage-${var.environment}"

  tags = {
    environment = var.environment
  }
}