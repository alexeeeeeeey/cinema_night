class Permission:
    name: str
    owner: str

    def __eq__(self, other):
        return (
            isinstance(other, Permission)
            and self.name == other.name
            and self.owner == other.owner
        )

    def __hash__(self):
        return hash((self.name, self.owner))

    def __repr__(self):
        return f"<Permission {self.owner}.{self.name}>"


class PermissionMeta(type):
    def __new__(cls, name, bases, attrs):
        for base in bases:
            for attr_name, attr_value in base.__dict__.items():
                if isinstance(attr_value, Permission) and attr_name not in attrs:
                    attrs[attr_name] = Permission()

        for attr_name, attr_value in attrs.items():
            if isinstance(attr_value, Permission):
                attr_value.name = attr_name
                attr_value.owner = name

        return super().__new__(cls, name, bases, attrs)


class BaseModelPermissions(metaclass=PermissionMeta):
    CREATE = Permission()
    READ = Permission()
    UPDATE = Permission()
    DELETE = Permission()
