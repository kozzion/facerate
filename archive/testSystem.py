from SystemFaceRate import SystemFaceRate

system = SystemFaceRate()
url = 'https://www.biography.com/.image/ar_1:1%2Cc_fill%2Ccs_srgb%2Cg_face%2Cq_auto:good%2Cw_300/MTE4MDAzNDEwNzg5ODI4MTEw/barack-obama-12782369-1-402.jpg'

imageResult =  system.processUrl(url)
print(imageResult)
