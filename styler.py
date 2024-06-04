from .util import *


class Prompt_Styler:

    styles = load_all_styles()
    style_names = ["default"] + list(styles.keys())

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
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


NODE_CLASS_MAPPINGS = {
    "Prompt_Styler": Prompt_Styler
}


NODE_DISPLAY_NAME_MAPPINGS = {
    "Prompt_Styler": "Prompt Styler"
}
