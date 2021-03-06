# -*- coding: utf-8 -*- 

"""
需求：
    1、在尺寸为 2048 * 2048 的黑色背景图片中，依次填充 images 中的气球图片（不要改变原图尺寸），
       气球图片的间隔至少大于 20 个像素，填充完成并保存，如果填充溢出，可保存多张图片。。
    2、annotations.json 中对应每一个气球的标注的掩膜坐标信息，请根据 annotations 
       中的格式生成新的 json 标注文件，并确保新生成的 json 标注文件里的掩膜坐标信息对
       应需求 1 中保存的图片。
    3、请验证需求 2 中新生成 json 文件掩膜标注信息的正确性。
"""

def merge(images, annotations_file):
    """
    input:
        images: 气球图片。
        annotations_file: 气球标注信息。
    """
    pass