from util import *
style_name = "Enhance"
positive_prompt = "Enter positive prompt here"

styles = load_all_styles()

if "{prompt}" in styles[style_name]["positive"]:
    positive_prompt = styles[style_name]["positive"].replace(
        '{prompt}', "of " + positive_prompt)
else:
    positive_prompt = styles[style_name]["positive"] + \
        ", " + positive_prompt

print(positive_prompt)
