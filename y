version = 0.1
[default]
[default.deploy]
[default.deploy.parameters]
stack_name = "youtube-video"
s3_bucket = "aws-sam-cli-managed-default-samclisourcebucket-1b279kukqwln1"
s3_prefix = "youtube-video"
region = "ap-south-1"
confirm_changeset = true
capabilities = "CAPABILITY_IAM"
image_repositories = []

[y]
[y.deploy]
[y.deploy.parameters]
stack_name = "sam-app"
s3_bucket = "aws-sam-cli-managed-default-samclisourcebucket-1b279kukqwln1"
s3_prefix = "sam-app"
region = "ap-south-1"
confirm_changeset = true
capabilities = "CAPABILITY_IAM"
image_repositories = []
