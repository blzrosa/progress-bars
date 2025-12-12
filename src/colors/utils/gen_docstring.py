from ast import literal_eval
from typing import Mapping, get_args

from src.colors.types.space import BaseColorSpace


def generate_title_description(
    name: str,
) -> str:
    return f"""
{name}
----------
Represents colors in the {name} color space 
with an alpha channel for transparency.
"""


def generate_parameters_description(
    components: dict[str, str],  # name, alias
    ranges: dict[str, tuple[int | float, int | float]],
) -> str:
    params = "Parameters\n----------\n"
    for comp_name, comp_alias in components.items():
        comp_range = ranges[comp_name]
        if isinstance(comp_range[0], int):
            range_desc = f"inclusive range [{comp_range[0]}, {comp_range[1]}]"
        else:
            range_desc = f"inclusive range [{comp_range[0]:.1f}, {comp_range[1]:.1f}]"
        params += (
            f"{comp_alias} : {'int' if isinstance(comp_range[0], int) else 'float'}\n"
        )
        params += (
            f"    Initial {comp_name} channel value. Expected in the {range_desc}.\n"
        )
    return params


def generate_description_section(
    components: dict[str, str],  # name, alias
) -> str:
    desc = """Description
-----------
Instances store channel values internally and expose them via the
"""
    for comp_name in components.keys():
        desc += f"properties `{comp_name}`"
        if comp_name != list(components.keys())[-1]:
            desc += ", "
    desc += ". Each property provides a getter and a setter."
    desc += " Setters validate that the provided value is within the\n"
    desc += "allowed range and will raise DefaultChannelOutOfBounds(channel, value)"
    desc += " if the value is outside that range.\n"
    return desc


def generate_properties_section(
    components: dict[str, str],  # name, alias
    ranges: dict[str, tuple[int | float, int | float]],
) -> str:
    props = "Properties\n----------\n"
    for comp_name, _ in components.items():
        comp_range = ranges[comp_name]
        if isinstance(comp_range[0], int):
            range_desc = f"[{comp_range[0]}, {comp_range[1]}]"
        else:
            range_desc = f"[{comp_range[0]:.1f}, {comp_range[1]:.1f}]"
        props += f"**{comp_name}** :"
        props += f" {'int' if isinstance(comp_range[0], int) else 'float'}\n"
        props += f"    - Get or set the {comp_name} channel {range_desc}."
        props += " Setting an out-of-range value\n"
        props += f"    - raises DefaultChannelOutOfBounds('{comp_name}', value).\n"
    return props


def generate_notes_section(
    components: dict[str, str],  # name, alias
) -> str:
    notes = """Notes
----------
- Channel values are stored privately (e.g., """
    for comp_alias in components.values():
        notes += f"_{comp_alias}, "
    notes = notes.rstrip(", ")
    notes += """) and should be
    manipulated through the provided properties to ensure validation.
- The class is mutable via the property setters.
"""
    return notes


def generate_space_docstring(
    name: str,
    components: dict[str, str],  # name, alias
    ranges: dict[str, tuple[int | float, int | float]],
) -> str:
    docstring = ""
    docstring += generate_title_description(name)
    docstring += "\n"
    docstring += generate_parameters_description(components, ranges)
    docstring += "\n"
    docstring += generate_description_section(components)
    docstring += "\n"
    docstring += generate_properties_section(components, ranges)
    docstring += "\n"
    docstring += generate_notes_section(components)
    return docstring


def generate_colorclass_docstring(cls: type[BaseColorSpace]) -> str:
    name = cls.__name__
    components: Mapping[str, str] = {
        item: item[0] for item in cls.__annotations__.keys()
    }
    ranges = {}
    for item, type_ in cls.__annotations__.items():
        # Get arguments from Annotated (e.g., Annotated[int, "[0, 255]"])
        args = get_args(type_)

        # args[0] is the type, args[1] is the metadata string
        if len(args) > 1 and isinstance(args[1], str):
            try:
                # Parse the string "[min, max]" into a tuple/list
                min_val, max_val = literal_eval(args[1])
                ranges[item] = (min_val, max_val)
            except (ValueError, SyntaxError):
                # Handle cases where metadata isn't a valid range string
                print(f"Warning: Could not parse range for {item} from {args[1]}")
                continue

    return generate_space_docstring(name, components, ranges)
