
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
    style_names = ["candy", "mosaic", "rain_princess", "udnie", "wave", "la_muse", "scream", "the_shipwreck_of_the_minotaur", "the_great_wave_off_kanagawa", "the_starry_night", "the_scream", "the_kiss", "the_night_watch", "the_birth_of_venus", "the_creation_of_adam", "the_persistence_of_memory", "the_son"] 
    
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(self):
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
                        + Secound value is a config for type "INT", "STRING" or "FLOAT".
        """
        return {
            "required": {
                "clip": ("CLIP", {}),
                "style": (self.style_names, {"default": "None"}),
                "positive": ("STRING", {
                    "multiline": True, #True if you want the field to look like the one on the ClipTextEncode node
                    "default": ""
                }),
                "negative": ("STRING", {
                    "multiline": True,
                    "default": "",
                }),
                "postive_style":("BOOL",{
                    "default": True
                }),
                "negative_style":("BOOL",{
                    "default": True
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

    RETURN_TYPES = ("CONDITIONING","CONDITIONING","STRING","STRING")
    RETURN_NAMES = ("positive","negative","positive","negative")

    FUNCTION = "apply_style"

    #OUTPUT_NODE = False

    CATEGORY = "Example"

    def encode(self, clip, text):
        tokens = clip.tokenize(text)
        cond, pooled = clip.encode_from_tokens(tokens, return_pooled=True)
        return ([[cond, {"pooled_output": pooled}]], )
    
    def test(self,clip, style, positive, negative, postive_style, negative_style, positive_1, negative_1):


    """
        The node will always be re executed if any of the inputs change but
        this method can be used to force the node to execute again even when the inputs don't change.
        You can make this node return a number or a string. This value will be compared to the one returned the last time the node was
        executed, if it is different the node will be executed again.
        This method is used in the core repo for the LoadImage node where they return the image hash as a string, if the image hash
        changes between executions the LoadImage node is executed again.
    """
    #@classmethod
    #def IS_CHANGED(s, image, string_field, int_field, float_field, print_to_screen):
    #    return ""

# Set the web directory, any .js file in that directory will be loaded by the frontend as a frontend extension
# WEB_DIRECTORY = "./somejs"

# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "Example": Example
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "Example": "Example Node"
}
