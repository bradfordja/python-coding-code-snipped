from marshmallow import (
    Schema,
    ValidationError as MarshmallowValidationError,
    fields,
    validate,
    validates_schema,
)

from app.models.user import Role


class UserCreateSchema(Schema):
    username = fields.String(
        required=True,
        validate=[
            validate.Length(min=3, max=50),
            validate.Regexp(r"^[a-zA-Z0-9_.-]+$"),
        ],
    )

    email = fields.Email(required=True)

    full_name = fields.String(
        required=True,
        validate=validate.Length(min=2, max=100),
    )

    password = fields.String(
        required=True,
        load_only=True,
        validate=validate.Length(min=8, max=128),
    )

    role = fields.String(
        load_default=Role.VIEWER.value,
        validate=validate.OneOf(
            [role.value for role in Role]
        ),
    )


class UserUpdateSchema(Schema):
    email = fields.Email(required=False)

    full_name = fields.String(
        required=False,
        validate=validate.Length(min=2, max=100),
    )

    password = fields.String(
        required=False,
        load_only=True,
        validate=validate.Length(min=8, max=128),
    )

    role = fields.String(
        required=False,
        validate=validate.OneOf(
            [role.value for role in Role]
        ),
    )

    disabled = fields.Boolean(required=False)

    @validates_schema
    def validate_not_empty(self, data, **kwargs):
        if not data:
            raise MarshmallowValidationError(
                "At least one field must be supplied"
            )


class LoginSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True, load_only=True)