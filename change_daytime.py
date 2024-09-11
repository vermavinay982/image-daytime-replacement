import argparse
import os
from skimage import exposure
import numpy as np
import cv2
from matplotlib import pyplot as plt

load_image = lambda img_path: cv2.imread(img_path)

def plot_changes(src, ref, op):
    plt.subplot(1, 3, 1)
    plt.imshow(cv2.cvtColor(src, cv2.COLOR_BGR2RGB))
    plt.grid(False); plt.axis(False)

    plt.subplot(1, 3, 2)
    plt.imshow(cv2.cvtColor(ref, cv2.COLOR_BGR2RGB))
    plt.grid(False); plt.axis(False)

    plt.subplot(1, 3, 3)
    plt.imshow(cv2.cvtColor(op, cv2.COLOR_BGR2RGB))
    plt.grid(False); plt.axis(False)
    plt.show()

def do_histogram_matching(src, ref):
    matched = exposure.match_histograms(src, ref, channel_axis=2)
    matched = np.array(matched, "uint8")
    new_image = matched

    return new_image

def change_daytime(input, reference, output, plot=False):
    src = load_image(input)
    ref = load_image(reference)
    op = do_histogram_matching(src, ref)    
    
    if plot:
        plot_changes(src, ref, op)
    
    flag = cv2.imwrite(output, op)
    print(f"==> Image Written: {flag} - at {output}")

def main():
    parser = argparse.ArgumentParser(description='Change image colors based on the time of day.')
    parser.add_argument('--input','-i', type=str, default='input.jpg', help='Path to the input image')
    parser.add_argument('--reference','-ref', type=str, default=None, help='Reference image or data for color adjustment')
    parser.add_argument('--output','-o', type=str, default='output.jpg', help='Path to save the output image')
    parser.add_argument('--new_daytime','-d', type=str, default=None, help='Specify the new time of day (e.g., "morning", "afternoon", "evening", "night")')
    parser.add_argument('--root_folder','-root', type=str, default='assets', help='Root folder for assets')
    parser.add_argument('--plot', action='store_true', help='Flag to plot and visualize the image after processing')

    args = parser.parse_args()

    print(f"\nInput Image: {args.input}")
    print(f"Output Image: {args.output}")
    print(f"Reference: {args.reference}")
    print(f"New Daytime: {args.new_daytime}")
    print(f"Root Folder: {args.root_folder}\n")
    
    root_folder = args.root_folder
    reference = args.reference
    input = args.input
    output = args.output
    new_daytime = args.new_daytime

    if reference is None:
        match new_daytime:
            case "evening":
                reference = os.path.join(root_folder, "evening.jpg")
            case "afternoon":
                reference = os.path.join(root_folder, "afternoon.jpg")
            case "morning":
                reference = os.path.join(root_folder, "morning.jpg")
            case "night":
                reference = os.path.join(root_folder, "night.jpg")
            case _:
                reference = None
            
    if reference is None and new_daytime is None:
        print("!! Specify either Reference Image, or Daytime !!")
        exit()


    change_daytime(input, reference, f"{new_daytime}_{output}", plot=args.plot)


if __name__=="__main__":
    main()