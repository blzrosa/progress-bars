from typing import Any, Callable


def channel_getter_setter(
    channel_name: str,
    validate_method: Callable[[str, Any], Any],
    alias: str = "",
):
    """
    A decorator to create a getter and setter for a color channel.

    The setter uses the specified validation method to ensure the value is
    within the allowed range.

    Parameters
    ----------
    channel_name : str
        The name of the channel (e.g., 'red', 'green', 'blue').
    validate_method : Callable[[str, Any], Any]
        The validation method to call in the setter.
    alias : str, optional
        An optional alias for the private attribute name.
    """
    type_ = validate_method.__annotations__["value"]

    def decorator(cls) -> Any:
        if alias == "":
            private_attr: str = f"_{channel_name.lower()}"
        else:
            private_attr: str = f"_{alias.lower()}"

        def getter(self) -> type_:
            return getattr(self, private_attr)

        def setter(self, value: type_) -> None:
            validate_method(channel_name, value)
            setattr(self, private_attr, value)

        setattr(cls, channel_name, property(getter, setter))
        return cls

    return decorator
