import os, socket, sys, urllib

from wx.lib.embeddedimage import PyEmbeddedImage

ldc_name = "Live Debian Creator"
ldc_cli_version = "1.4.0"
ldc_gui_version = "1.11.0"

if (sys.platform == "win32"):
    slash = "\\"
    if os.path.isfile(sys.path[0]): #fix for compiled binaries
        homepath = os.path.dirname(sys.path[0]) + slash
    else:
        homepath = sys.path[0] + slash
else:
    slash = "/"

#socket.setdefaulttimeout(10)

def defineBrowserAgent(uiname, uiversion):
    class AppURLopener(urllib.FancyURLopener):
        version = "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)"
        #version = uiname + " " + uiversion + " / " + sys.platform
    urllib._urlopener = AppURLopener()

bookico = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAABHNCSVQICAgIfAhkiAAABPZJ"
    "REFUWIWtl09sFFUcxz/iYN+YTZyNxewiTWiV6FZQtqhkN3pgGw6UW6unJVxEDtaThJMc9WLg"
    "oj1hwJhANURqQkw9NGwTla0c6JqArELSMVCzi63uKJX5UR7Bw8x0Z2d3yxJ5yctM3vu93/f7"
    "+ztv4CGPqamp9A/nL2Q6lTceBqht26pw7kL+7K+10S/tJ9OpBBPASCdnH/k/wFNTU+nzc/+M"
    "2v925a2N21Sq1yKJg/wxV7XWyIHBnYPjD53A9PS0mrv+e/6yw6gT60+72iK7AVJJSBoCBihD"
    "AVC6WK7O3bx3+thFyY30ycSH7+w5FNXXcQgymUzaei49+vHMX/kq/SqpYGiDRbYHlBFoigMu"
    "gklxHsZ1NlG4yygvKiruWauV3vsS2L59e+qZVwfHqsnB3G8LkI2ZHHzdImGBaZi+BgVaqIhi"
    "sqo4uQBlrQDPI2jx5gMQUFu39A3veW3ru9leMmO19aQ2JDm8C5SCuDJBgUJRM6DkKE5WFYUF"
    "cLSAxgOnNeiqBHZt6z2wO2UdSvXGrfimFNYrIzhHbca/LlOcTzL0coJsj8IRKC4pJhfAXvKB"
    "dKBFQu+AdjsnsG/AOpzc+RZWKkc8FgcFGDYApas1SgtAUjxXJOK+a1XUgRHrzc4JlMslqB5C"
    "ZYbg+Sws2rAYByPlSQcntNQtNSLaNGCoxv07HRJAQ63ioM6MI2fGPdt6DngKDbVK1kS9IKBV"
    "PQmN6P4qBNAgGlw/jqJp9vKKBtVILrA4nA+GegAPBCT8Z0P6RF0dvAfgwdRRIu2rYfU+sLKr"
    "mtcCq3UIPGyABmupzIBRoOIkuXzF7oyACq2KDne5FmQC2fC+UyWtZxmIlchtseg1sti2yzf2"
    "z8n8559kdmzbYW/evLnalgAGmLr+Lp00aw3WYomUUaDfKpNJphmIDWEZXvd1N9m80HNj+Fs5"
    "Pvx0TY0AE6sQUGB45SOA0m0kwyWnHfLdh8nGd5NJDGMqEwyXoi5QXJrAltmVsNxabq2mrWVi"
    "qHoitkpCBJwKp6uTVDbaVGKziK5wWWaQoAOGu2IbO5pGkLfuKocD5WrJwVRQXirjXC+DAdY6"
    "1ZSYCng8cnxNk8K1fukF/eA+FqAFpIaiMT0VXgIr5fcohUfosca23EzgTh3cDep5taFdcCN1"
    "bviAMTB98OZqakfAH65vx4rqKBlNm2+8grUeWGCrGW5S9yWwti7ofW5Ucx9rIBK6bIRB2lVN"
    "Y29tQcBonG4Ta6k/NSBeDkSH2Sp0GoiUYYsQ+AB+0rTt4hov/lpQ0lrKDT/F66y3IjLN9rmh"
    "VQVo1b4StHgkWhAIEjioKBFfx91GFzR5wJ5HRINpem3YQfzyklAihgCjxDT1SvLvLLLkR0rA"
    "jdzOmjxwotbVf656+/20YmS9wrIfvSdO8p53A0UAM0RihVqIjNSB/WXRIFpwXVhebgxCkwdu"
    "/33b/kXY94VD/KWPjvY9lduVvaWxCVzYYipxW1eKFhwRajcdat9RemP+vd2jbx6cCIt19Gf0"
    "6fETw28fKR6jf9Ci24LuuFeuMWC2IIlLXxVl70+5ZDckuxWuFuIxqIjgTDOjzvV9UC7OTbbS"
    "3fGvmW3bauyzE/nCFXe4dIMsy45tVX889oT+83RXV5d5bf21MXIyZD3re2WGgnyfOFK9VG0J"
    "/MAEOhmnTp1KXF28mlsXWzezf+/+1legyPgPTicVRBS2XfsAAAAASUVORK5CYII=")
getbookicoIcon = bookico.GetIcon