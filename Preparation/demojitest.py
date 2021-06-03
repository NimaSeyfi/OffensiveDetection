import demoji
import regex as re
# demoji.download_codes()

text = u'منو فالو نمیکنید☹️☹️ یعنی یه دوووونه کامنت  وجودره 🤦‍♀️ همه دنبال یه چیزی میگردن ،خاک برسرتون ،واقعا حت ریده به ت تصویری با ۸۵واقعی❤️'

new = demoji.replace(text, "")
print(new)