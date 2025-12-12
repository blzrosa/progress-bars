from ast import literal_eval
from typing import Optional, Tuple, get_args

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
Instances store channel values internally and expose them via the properties 
"""
    for comp_name in components.keys():
        desc += f"`{comp_name}`"
        if comp_name != list(components.keys())[-1]:
            desc += ", "
    desc += ".\nEach property provides a getter and a setter."
    desc += "\nSetters validate that the provided value is within the\n"
    desc += "allowed range and will raise DefaultChannelOutOfBounds(channel, value)"
    desc += "\nif the value is outside that range.\n"
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
    attr_mapping: Optional[dict[str, str]],
) -> str:
    if attr_mapping is None:
        attr_mapping = {}
    mapped_components: dict[str, str] = {
        comp: attr_mapping[comp] if comp in attr_mapping else short
        for comp, short in components.items()
    }
    docstring = ""
    docstring += generate_title_description(name)
    docstring += "\n"
    docstring += generate_parameters_description(mapped_components, ranges)
    docstring += "\n"
    docstring += generate_description_section(components)
    docstring += "\n"
    docstring += generate_properties_section(components, ranges)
    docstring += "\n"
    docstring += generate_notes_section(mapped_components)
    return docstring


def get_annotations(
    cls: BaseColorSpace,
) -> tuple[dict[str, str], dict[str, tuple[int | float, int | float]]]:
    properties: dict[str, property] = {
        name: attr
        for name, attr in cls.__dict__.items().__reversed__()
        if isinstance(attr, property)
    }
    components: dict[str, str] = {}  # full name → short alias (first letter)
    ranges: dict[str, Tuple[int | float, int | float]] = {}
    for comp_name, prop in properties.items():
        components[comp_name] = comp_name[0].lower()
        range_: str = get_args(prop.fget.__annotations__["return"])[1]
        try:
            # Parse the string "[min, max]" into a tuple/list
            min_val, max_val = literal_eval(range_)
            ranges[comp_name] = (min_val, max_val)
        except (ValueError, SyntaxError):
            # Handle cases where metadata isn't a valid range string
            print(f"Warning: Could not parse range for {comp_name} from {range_}")
            continue
    return components, ranges


def generate_colorclass_docstring(
    cls: BaseColorSpace,
    attr_mapping: Optional[dict[str, str]] = None,
) -> str:
    name: str = cls.__name__
    components, ranges = get_annotations(cls)

    return generate_space_docstring(name, components, ranges, attr_mapping)


if __name__ == "__main__":
    from src.colors.types.colors import (
        A98RGB,
        CIELAB,
        CMYK,
        HSL,
        HSV,
        HWB,
        LCH,
        DisplayP3,
        Oklab,
        Oklch,
        ProPhotoRGB,
        Rec2020,
        XYZd50,
        XYZd65,
        sRGB,
        sRGBLinear,
    )

    color_classes = [
        sRGB,
        HSV,
        HSL,
        HWB,
        DisplayP3,
        Rec2020,
        A98RGB,
        ProPhotoRGB,
        CIELAB,
        LCH,
        Oklab,
        Oklch,
        XYZd65,
        XYZd50,
        sRGBLinear,
        CMYK,
    ]
    for color_class in color_classes:
        print("─" * 40)
        print("\n\n")

        if color_class != CMYK:
            print(generate_colorclass_docstring(color_class))
        else:
            print(generate_colorclass_docstring(color_class, {"black": "k"}))

        print("\n\n")
        input("Press Enter to continue...")
