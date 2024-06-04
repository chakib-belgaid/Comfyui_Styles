from .util import *


class Prompt_Styler:
    """
    A example node

    Class methods
    -------------
    INPUT_TYPES (dict):
        Tell the main program input parameters of nodes.
    IS_CHANGED:
        optional method to control when the node is re executed.

    Attributes
    ----------
    RETURN_TYPES (`tuple`):
        The type of each element in the output tulple.
    RETURN_NAMES (`tuple`):
        Optional: The name of each output in the output tulple.
    FUNCTION (`str`):
        The name of the entry-point method. For example, if `FUNCTION = "execute"` then it will run Example().execute()
    OUTPUT_NODE ([`bool`]):
        If this node is an output node that outputs a result/image from the graph. The SaveImage node is an example.
        The backend iterates on these output nodes and tries to execute all their parents if their parent graph is properly connected.
        Assumed to be False if not present.
    CATEGORY (`str`):
        The category the node should appear in the UI.
    execute(s) -> tuple || None:
        The entry point method. The name of this method must be the same as the value of property `FUNCTION`.
        For example, if `FUNCTION = "execute"` then this method's name must be `execute`, if `FUNCTION = "foo"` then it must be `foo`.
    """
    styles = load_all_styles()
    style_names = ["default"] + list(styles.keys())

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        """
        Return a dictionary which contains config for all input fields.
        Some types (string): "MODEL", "VAE", "CLIP", "CONDITIONING", "LATENT", "IMAGE", "INT", "STRING", "FLOAT".
        Input types "INT", "STRING" or "FLOAT" are special values for fields on the node.
        The type can be a list for selection.

        Returns: `dict`:
            - Key input_fields_group (`string`): Can be either required, hidden or optional. A node class must have property `required`
            - Value input_fields (`dict`): Contains input fields config:
                * Key field_name (`string`): Name of a entry-point method's argument
                * Value field_config (`tuple`):
                    + First value is a string indicate the type of field or a list for selection.
                    + Second value is a config for type "INT", "STRING" or "FLOAT".
        """
        return {
            "required": {
                "clip": ("CLIP", {}),
                "style_name": (cls.style_names, {"label": "style", "default": "default"}),
                "positive": ("STRING", {
                    "multiline": True,
                    "dynamicPrompts": True,
                    "placeholder": "Enter positive prompt here"
                }),
                "enable_positive_style": ("BOOLEAN", {
                    "default": True,
                    "tooltip": "Apply style to positive prompt"
                }),
                "negative": ("STRING", {
                    "multiline": True,
                    "dynamicPrompts": True,
                    "placeholder": "Enter negative prompt here"
                }),
                "enable_negative_style": ("BOOLEAN", {
                    "default": True,
                    "tooltip": "Apply style to negative prompt"
                }),
            },
            "optional": {
                "positive_1": ("STRING", {
                    "forceInput": True
                }),
                "negative_1": ("STRING", {
                    "forceInput": True
                }),
            }
        }

    RETURN_TYPES = ("CONDITIONING", "CONDITIONING", "STRING", "STRING")
    RETURN_NAMES = ("positive", "negative", "positive", "negative")

    FUNCTION = "apply_style"

    # OUTPUT_NODE = False

    CATEGORY = "Prompt Styler"

    def encode(self, clip, text):
        tokens = clip.tokenize(text)
        cond, pooled = clip.encode_from_tokens(tokens, return_pooled=True)
        return [[cond, {"pooled_output": pooled}]]

    def apply_style(self, clip, positive, negative, enable_positive_style, enable_negative_style, style_name="default", positive_1=None, negative_1=None):
        positive_prompt = positive_1 + ", " + positive if positive_1 else positive
        negative_prompt = negative_1 + ", " + negative if negative_1 else negative
        if enable_positive_style and style_name != "default":
            if "{prompt}" in self.styles[style_name]["positive"]:
                positive_prompt = self.styles[style_name]["positive"].replace(
                    '{prompt}', "of " + positive_prompt)
            else:
                positive_prompt = self.styles[style_name]["positive"] + \
                    ", " + positive_prompt

        if enable_negative_style and style_name != "default":
            negative_prompt = negative_prompt + ", " + \
                self.styles[style_name]["negative"]
        positive_cond = self.encode(clip, positive_prompt)
        negative_cond = self.encode(clip, negative_prompt)

        return positive_cond, negative_cond, positive_prompt, negative_prompt

    # @classmethod
    # def IS_CHANGED(cls, image, string_field, int_field, float_field, print_to_screen):
    #    return ""

# Set the web directory, any .js file in that directory will be loaded by the frontend as a frontend extension
# WEB_DIRECTORY = "./somejs"


# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "Prompt_Styler": Prompt_Styler
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "Prompt_Styler": "Prompt Styler"
}
