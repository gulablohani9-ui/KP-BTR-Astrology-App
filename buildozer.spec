[app]
title = KPBTR
package.name = kpbtr
package.domain = org.astrology
source.dir = .
# यह लाइन बहुत महत्वपूर्ण है ताकि ephe डेटाबेस ऐप में शामिल हो सके
source.include_exts = py,png,jpg,kv,atlas,se1
version = 1.0
# ऐप को कौन सी लाइब्रेरी चाहिए
requirements = python3,kivy,pyswisseph,requests
orientation = portrait
osx.python_version = 3
osx.kivy_version = 1.9.1
fullscreen = 0
android.permissions = INTERNET, ACCESS_FINE_LOCATION
