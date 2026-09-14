[app]
title = KP BTR App
package.name = kpbtr
package.domain = org.astrology
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,se1
version = 1.0
# pyswisseph ग्रहों के लिए और geopy अपने आप लोकेशन लेने के लिए
requirements = python3,kivy,pyswisseph,geopy,requests,urllib3
orientation = portrait
osx.python_version = 3
osx.kivy_version = 1.9.1
fullscreen = 0
android.permissions = INTERNET, ACCESS_FINE_LOCATION
