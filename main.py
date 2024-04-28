import skimage.filters
from moviepy.editor import *
import random

def make_blur_function(sigma):
    """ Returns a function that applies gaussian blur with the given sigma """
    def blur(image):
        # Returns a blurred version of the image with the given sigma
        print(sigma)
        return skimage.filters.gaussian(image.astype(float), sigma=sigma)
    return blur

def pickduration(cust_length):
    duration = clip.duration
    random_float = random.uniform(0.0,duration)
    print("duration: ",duration)
    print("rand_float: ", random_float)

    while random_float+cust_length+1>duration:
        random_float = random.uniform(0.0, duration)
        print("rand_int: ",random_float)
    return random_float

clip = VideoFileClip("input.mp4")

cust_length =10 # Length of our new video in seconds

random_begin = pickduration(cust_length) # The video begins from a random timestamp

clip = clip.subclip(random_begin, random_begin+cust_length)


clipss = [] # Temporary videos list, each with an increasing Gaussian value

step=0.0 # Temporary video timestamp in seconds, applied from the beginning (hence the 0.0)
range_Length=50 # The final blur value
percentage_to_be_blurred = 0.2 # Suppose we want 20% of the video to be blurred, starting from the beginning
add_to_step = (clip.duration*percentage_to_be_blurred)/range_Length # (10*0.2)/50 = 0.04 seconds for each step adding Gaussian blur
for intg in range(range_Length):
    blur_function = make_blur_function(intg)

    clip_new = clip.subclip(step,step+add_to_step)
    step = step+add_to_step

    clip_blurred = clip_new.fl_image(blur_function)
    clipss.append(clip_blurred)

# The rest of the video will use the final Gaussian blur value
final_appendage = clip.subclip(step,clip.duration)
blur_function = make_blur_function(range_Length-1)
final_blurred = final_appendage.fl_image(blur_function)
clipss.append(final_blurred)

final = concatenate_videoclips(clipss)
final.write_videofile("output.mp4")