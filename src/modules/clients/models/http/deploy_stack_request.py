from pydantic import BaseModel, Field, field_validator

class DeployRequest(BaseModel):
    stack_name: str = Field(..., min_length=3, max_length=50)
    template_file: str = Field(..., pattern=r"^.*\.yml$")
    environment: str = Field(..., pattern=r"^(dev|develop|uat|staging|prd|sandbox)$")
    base_path: str = Field(..., pattern=r"^(containers|fronts|lambdas|workers|api-privada|api-public|apps|base|events)$")
    deploy_version: str = Field(default="1.0.0", pattern=r"^\d+\.\d+\.\d+$")
    region: str = Field(
        default="us-east-1",
        pattern=r"^(mx-central-1|us-east-1)$"
    )

    @field_validator('stack_name')
    def validate_stack_name(cls, v):
        if ' ' in v:
            raise ValueError('stack_name cannot contain spaces')
        return v