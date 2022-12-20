import os
from flask import Flask, request, send_file, Response
from flask_cors import CORS
import modules.generator as gen
import modules.powerpoint as pp
import modules.helpers as hp
import ast

# App setup
app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

########### ROUTES ###########


@app.route("/")
def index() -> str:
    return "<p>GPT Presentation Generator</p>"


@app.route("/powerpoint", methods=['POST', 'OPTIONS'])
def create_powerpoint():
    if request.method == "OPTIONS":
        temp_res = Response("foo bar baz")
        temp_res.headers['Access-Control-Allow-Origin'] = '*'
        temp_res.headers['Access-Control-Allow-Headers'] = '*'
        temp_res.status_code = 204
        return temp_res

    # Get Request info for presentation creation
    prompt = request.json['prompt']

    # Generate bullet points with prompt
    bullet_prompt = (f"Return a python list of 6 JSON objects summarizing the following with"
                     " the keys being a main idea with key name 'Main Idea' and the values being an array of details "
                     "of said main idea with key name being 'Details': {prompt}")
    raw_output = gen.generate_completion(bullet_prompt, 500, 0.1)
    starting_index = raw_output.find("[")

    result_lst: list = ast.literal_eval(raw_output[starting_index:])
    main_points = hp.get_keys_nested_dict(result_lst)

    # Make array of generated DALLE images with each subtopic
    slide_images = []
    for key in main_points:
        default_prompt = "Logo, visual effects studio, minimalist, modern"
        living_thing = gen.get_bullet_type(prompt)
        if living_thing:
            image_output = gen.get_image_response(
                f"Abstract image, {default_prompt}, {key}")
        else:
            image_output = gen.get_image_response(default_prompt + key)
        slide_images.append(image_output)

    # generate the unique title
    prompt_begin = "In 4 to 6 words, what is the topic of the following JSON data"
    generative_title_prompt = prompt_begin + str(result_lst)
    title = gen.generate_completion(generative_title_prompt, 7, .5)

    # create the presentation
    presentation_name = "DeckedOut_Presentation"
    presentation_id = pp.create_presentation(presentation_name)
    pp.fill_title_page(presentation_id, title)

    insert_index = 1
    for slide in result_lst:
        main_point = slide["Main Idea"]

        details = slide["Details"]
        bullets = "\n- ".join(details)

        img = slide_images[insert_index - 1]['url']

        page_id = 'Page' + str(insert_index)
        pp.fill_presentation(presentation_id, page_id, insert_index, main_point,
                             bullets, img)

        insert_index += 1

    # downlaod the pptx, send it, then delete it from the local machine and the google drive
    pp.download_ppt(presentation_id, presentation_name)
    # if you need to check what the presentation looks like, just comment this out
    pp.delete_slides(presentation_id)
    filename = presentation_name + ".pptx"
    res = send_file(filename)
    os.remove(filename)

    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers['Access-Control-Allow-Headers'] = '*'
    return res


if __name__ == '__main__':
    app.run(port=8000, debug=True)
