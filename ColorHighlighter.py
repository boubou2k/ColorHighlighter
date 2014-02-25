import sublime, sublime_plugin
import os
import re
import string

NAMES_TO_HEX = {'aliceblue': '#f0f8ffFF', 'antiquewhite': '#faebd7FF',
    'aqua': '#00ffffFF', 'aquamarine': '#7fffd4FF', 'azure': '#f0ffffFF',
    'beige': '#f5f5dcFF', 'bisque': '#ffe4c4FF', 'black': '#000000FF',
    'blanchedalmond': '#ffebcdFF', 'blue': '#0000ffFF',
    'blueviolet': '#8a2be2FF', 'brown': '#a52a2aFF', 'burlywood': '#deb887FF',
    'cadetblue': '#5f9ea0FF', 'chartreuse': '#7fff00FF',
    'chocolate': '#d2691eFF', 'coral': '#ff7f50FF',
    'cornflowerblue': '#6495edFF', 'cornsilk': '#fff8dcFF',
    'crimson': '#dc143cFF', 'cyan': '#00ffffFF', 'darkblue': '#00008bFF',
    'darkcyan': '#008b8bFF', 'darkgoldenrod': '#b8860bFF',
    'darkgray': '#a9a9a9FF', 'darkgrey': '#a9a9a9FF', 'darkgreen': '#006400FF',
    'darkkhaki': '#bdb76bFF', 'darkmagenta': '#8b008bFF',
    'darkolivegreen': '#556b2fFF', 'darkorange': '#ff8c00FF',
    'darkorchid': '#9932ccFF', 'darkred': '#8b0000FF',
    'darksalmon': '#e9967aFF', 'darkseagreen': '#8fbc8fFF',
    'darkslateblue': '#483d8bFF', 'darkslategray': '#2f4f4fFF',
    'darkslategrey': '#2f4f4fFF', 'darkturquoise': '#00ced1FF',
    'darkviolet': '#9400d3FF', 'deeppink': '#ff1493FF',
    'deepskyblue': '#00bfffFF', 'dimgray': '#696969FF', 'dimgrey': '#696969FF',
    'dodgerblue': '#1e90ffFF', 'firebrick': '#b22222FF',
    'floralwhite': '#fffaf0FF', 'forestgreen': '#228b22FF',
    'fuchsia': '#ff00ffFF', 'gainsboro': '#dcdcdcFF', 'ghostwhite': '#f8f8ffFF',
    'gold': '#ffd700FF', 'goldenrod': '#daa520FF', 'gray': '#808080FF',
    'grey': '#808080FF', 'green': '#008000FF', 'greenyellow': '#adff2fFF',
    'honeydew': '#f0fff0FF', 'hotpink': '#ff69b4FF', 'indianred': '#cd5c5cFF',
    'indigo': '#4b0082FF', 'ivory': '#fffff0FF', 'khaki': '#f0e68cFF',
    'lavender': '#e6e6faFF', 'lavenderblush': '#fff0f5FF',
    'lawngreen': '#7cfc00FF', 'lemonchiffon': '#fffacdFF',
    'lightblue': '#add8e6FF', 'lightcoral': '#f08080FF',
    'lightcyan': '#e0ffffFF', 'lightgoldenrodyellow': '#fafad2FF',
    'lightgray': '#d3d3d3FF', 'lightgrey': '#d3d3d3FF',
    'lightgreen': '#90ee90FF', 'lightpink': '#ffb6c1FF',
    'lightsalmon': '#ffa07aFF', 'lightseagreen': '#20b2aaFF',
    'lightskyblue': '#87cefaFF', 'lightslategray': '#778899FF',
    'lightslategrey': '#778899FF', 'lightsteelblue': '#b0c4deFF',
    'lightyellow': '#ffffe0FF', 'lime': '#00ff00FF', 'limegreen': '#32cd32FF',
    'linen': '#faf0e6FF', 'magenta': '#ff00ffFF', 'maroon': '#800000FF',
    'mediumaquamarine': '#66cdaaFF', 'mediumblue': '#0000cdFF',
    'mediumorchid': '#ba55d3FF', 'mediumpurple': '#9370d8FF',
    'mediumseagreen': '#3cb371FF', 'mediumslateblue': '#7b68eeFF',
    'mediumspringgreen': '#00fa9aFF', 'mediumturquoise': '#48d1ccFF',
    'mediumvioletred': '#c71585FF', 'midnightblue': '#191970FF',
    'mintcream': '#f5fffaFF', 'mistyrose': '#ffe4e1FF', 'moccasin': '#ffe4b5FF',
    'monnoroch': '#000000FF', 'navajowhite': '#ffdeadFF', 'navy': '#000080FF',
    'oldlace': '#fdf5e6FF', 'olive': '#808000FF', 'olivedrab': '#6b8e23FF',
    'orange': '#ffa500FF', 'orangered': '#ff4500FF', 'orchid': '#da70d6FF',
    'palegoldenrod': '#eee8aaFF', 'palegreen': '#98fb98FF',
    'paleturquoise': '#afeeeeFF', 'palevioletred': '#d87093FF',
    'papayawhip': '#ffefd5FF', 'peachpuff': '#ffdab9FF', 'peru': '#cd853fFF',
    'pink': '#ffc0cbFF', 'plum': '#dda0ddFF', 'powderblue': '#b0e0e6FF',
    'purple': '#800080FF', 'red': '#ff0000FF', 'rosybrown': '#bc8f8fFF',
    'royalblue': '#4169e1FF', 'saddlebrown': '#8b4513FF', 'salmon': '#fa8072FF',
    'sandybrown': '#f4a460FF', 'seagreen': '#2e8b57FF', 'seashell': '#fff5eeFF',
    'sienna': '#a0522dFF', 'silver': '#c0c0c0FF', 'skyblue': '#87ceebFF',
    'slateblue': '#6a5acdFF', 'slategray': '#708090FF',
    'slategrey': '#708090FF', 'snow': '#fffafaFF', 'springgreen': '#00ff7fFF',
    'steelblue': '#4682b4FF', 'tan': '#d2b48cFF', 'teal': '#008080FF',
    'thistle': '#d8bfd8FF', 'tomato': '#ff6347FF', 'turquoise': '#40e0d0FF',
    'violet': '#ee82eeFF', 'wheat': '#f5deb3FF', 'white': '#ffffffFF',
    'whitesmoke': '#f5f5f5FF', 'yellow': '#ffff00FF', 'yellowgreen': '#9acd32FF'
}

version = "3.0"

# Constants
PACKAGES_PATH = sublime.packages_path()
SUBLIME_PATH = os.path.abspath(os.path.join(PACKAGES_PATH, os.pardir)) + os.path.sep

hex_digits = string.digits + "ABCDEF"

loglist = ["Version: " + version]
PREFIX = "mcol_"
sets_name = "ColorHighlighter.sublime-settings"

ch_settings = sublime.load_settings(sets_name)

def log(s):
    global loglist
    loglist.append(s)
    #print s

def write_file(fl, s):
    f = open(fl, 'w')
    f.write(s)
    f.close()

def read_file(fl):
    f = open(fl, 'r')
    res = f.read()
    f.close()
    return res


# Color formats:
# #FFFFFFFF
# #FFFFFF
# #FFF
# rgb(255,255,255)
# words
# black

max_len = max(len("#FFB"), len("#FFFFFF"), len("#FFFFFFAA"), len("rgb(199, 255, 255)"), len("rgba(255, 255, 255, 0.555)"))

regex1 = re.compile("[r][g][b][(]\d{1,3}[,][ ]*\d{1,3}[,][ ]*\d{1,3}[)]")
regex2 = re.compile("[#][\dA-F]{8}")
regex3 = re.compile("[#][\dA-F]{6}")
regex4 = re.compile("[#][\dA-F]{3}")
regex5 = re.compile("[r][g][b][a][(]\d{1,3}[,][ ]*\d{1,3}[,][ ]*\d{1,3}[,][ ]*(\d+|\d*\.\d+)[)]")


def tohex(r,g,b):
    sr = "%X" % r
    if len(sr) == 1:
        sr = '0' + sr
    sg = "%X" % g
    if len(sg) == 1:
        sg = '0' + sg
    sb = "%X" % b
    if len(sb) == 1:
        sb = '0' + sb
    return "#%s%s%sFF" % (sr,sg,sb)

def isInColorS(s, pos):
    m = regex1.search(s)
    if m != None and m.group(0) != None and m.start(0) <= pos and m.end(0) >= pos:
        s = m.group(0)
        s = s[3+1:-1]
        n = s.find(",")
        r = s[0:n]
        s = s[n+1:]
        n = s.find(",")
        g = s[0:n]
        s = s[n+1:]
        b = s
        return sublime.Region(m.start(0), m.end(0)), tohex(int(r), int(g), int(b))

    m = regex5.search(s)
    if m != None and m.group(0) != None and m.start(0) <= pos and m.end(0) >= pos:
        s = m.group(0)
        s = s[4+1:-1]
        n = s.find(",")
        r = s[0:n]
        s = s[n+1:]
        n = s.find(",")
        g = s[0:n]
        s = s[n+1:]
        n = s.find(",")
        b = s[0:n]
        return sublime.Region(m.start(0), m.end(0)), tohex(int(r), int(g), int(b))

    s = s.upper()

    # check #FFFFFFFF
    m = regex2.search(s)
    if m != None and m.group(0) != None and m.start(0) <= pos and m.end(0) >= pos:
        return sublime.Region(m.start(0), m.end(0)), m.group(0)

    # check #FFFFFF
    m = regex3.search(s)
    if m != None and m.group(0) != None and m.start(0) <= pos and m.end(0) >= pos:
        return sublime.Region(m.start(0), m.end(0)), m.group(0) + "FF"

    # check #FFF
    m = regex4.search(s)
    if m != None and m.group(0) != None and m.start(0) <= pos and m.end(0) >= pos:
        s = m.group(0)
        return sublime.Region(m.start(0), m.end(0)), s[0] + s[1]*2 + s[2]*2 + s[3]*2 + "FF"

    return None, None

def get_current_word(view, sel):
    n = sel.begin() - 1
    k = sel.end()
    while k - n <= max_len and (view.substr(n).isalpha() or view.substr(n) == "-"):
        n -= 1
    while k - n <= max_len and (view.substr(k).isalpha() or view.substr(k) == "-"):
        k += 1
    return sublime.Region(n + 1, k)

def isInColor(view, sel):
    b = sel.begin()
    if b != sel.end():
        return None, None

    wd = get_current_word(view, sel)
    res = NAMES_TO_HEX.get(view.substr(wd))
    if res != None:
        return wd, res

    lwd, lres = None, None
    for i in range(1, max_len):
        s = view.substr(sublime.Region(b - i, b + i))
        wd, res = isInColorS(s, i)
        if res == None and lres != None:
            i = i - 1
            return sublime.Region(lwd.begin() + (b - i), lwd.end() + (b - i)), lres
        lwd, lres = wd, res

    if lres == None:
        return None, None

    i = max_len - 1
    return sublime.Region(lwd.begin() + (b - i), lwd.end() + (b - i)), lres

class HtmlGen:
    colors = []
    color_scheme = None
    need_upd = False
    need_restore = False
    need_backup = False
    string = ""
    gen_string = """
<dict>
<key>name</key>
<string>mon_color</string>
<key>scope</key>
<string>%s</string>
<key>settings</key>
<dict>
<key>background</key>
<string>%s</string>
<key>caret</key>
<string>%s</string>
<key>foreground</key>
<string>%s</string>
</dict>
</dict>\n
"""

    def get_y(self, col):
        return (0.3 * int(col[1:3],16) + 0.59 * int(col[3:5],16) + 0.11 * int(col[5:7],16)) * (int(col[7:9],16) / 255.0)

    def get_cont_col(self, col):
        if self.get_y(col) > 255.0/2:
            return "#000000FF"
        return "#FFFFFFFF"

    def region_name(self, s):
        return PREFIX + s[1:]

    def add_color(self, col):
        if col in self.colors: return
        self.colors.append(col)
        cont = self.get_cont_col(col)
        self.string += self.gen_string % (self.region_name(col), col, cont, cont)
        self.need_upd = True

    def need_update(self):
        return self.need_upd

    def update(self, view):
        if not self.need_upd: return
        self.need_upd = False

        cs = self.color_scheme
        if cs == None:
            self.color_scheme = view.settings().get('color_scheme')
            cs = self.color_scheme
        # do not support empty color scheme
        if cs == "":
            log("Empty scheme, can't backup")
            return
        cont = None
        print(PACKAGES_PATH + cs + ".chback")
        if os.path.exists(SUBLIME_PATH + cs + ".chback"):
            cont = read_file(SUBLIME_PATH + cs + ".chback")
            log("Already backuped")
        else:
            cont = read_file(SUBLIME_PATH + cs)
            write_file(SUBLIME_PATH + cs + ".chback", cont) # backup
            log("Backup done")

        # edit cont
        n = cont.find("<array>") + len("<array>")
        try:
            cont = cont[:n] + self.string + cont[n:]
        except UnicodeDecodeError:
            cont = cont[:n] + self.string.encode("utf-8") + cont[n:]

        write_file(SUBLIME_PATH + cs, cont)
        self.need_restore = True

    def restore_color_scheme(self):
        if not self.need_restore: return
        self.need_restore = False
        cs = self.color_scheme
        # do not support empty color scheme
        if cs == "":
            log("Empty scheme, can't restore")
            return
        if os.path.exists(SUBLIME_PATH + cs + ".chback"):
            log("Starting restore scheme: " + cs)
            # TODO: move to other thread
            write_file(SUBLIME_PATH + cs, read_file(SUBLIME_PATH + cs + ".chback"))
            self.colors = []
            self.string = ""
            log("Restore done.")
        else:
            log("No backup :(")

    def set_color_scheme(self, view):
        self.color_scheme = view.settings().get('color_scheme')
        self.need_backup = True


    def change_color_scheme(self, view):
        cs = view.settings().get('color_scheme')
        if cs != self.color_scheme:
            self.restore_color_scheme()
            self.set_color_scheme(view)
            self.update(view)

htmlGen = HtmlGen()

# Commands

# # treat hex vals as colors
# class HexValsAsColorsCommand(sublime_plugin.WindowCommand):
#     def run(self):
#         ch_settings.set("hex_values", not ch_settings.get("hex_values"))
#         sublime.save_settings(sets_name)

#     def is_checked(self):
#         return ch_settings.get("hex_values")

# # treat hex vals as colors
# class XHexValsAsColorsCommand(sublime_plugin.WindowCommand):
#     def run(self):
#         ch_settings.set("0x_hex_values", not ch_settings.get("0x_hex_values"))
#         sublime.save_settings(sets_name)

#     def is_checked(self):
#         return ch_settings.get("0x_hex_values")

# command to print log
class chlogCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        res = ""
        for l in loglist:
            res += l + "\n"
        if res == "":
            return
        log("Log printed.")
        #self.view.insert(edit, 0, res + "\n\n\n")

# command to restore color scheme
class RestoreColorSchemeCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        htmlGen.restore_color_scheme()

all_regs = []
inited = False

class ColorSelection(sublime_plugin.EventListener):
    def on_new(self, view):
        global inited
        if inited: return
        inited = True
        sets = view.settings()
        htmlGen.set_color_scheme(view)
        sets.add_on_change("color_scheme", lambda self = self, view = view : htmlGen.change_color_scheme(view))
        # htmlGen.change_color_scheme(view)

    def on_clone(self, view):
        self.on_new(view)

    # def on_close(self, view):
    #     htmlGen.restore_color_scheme()

    def on_selection_modified(self, view):
        selection = view.sel()
        words = []
        for s in selection:
            wd, col = isInColor(view, s)
            if col != None:
                htmlGen.add_color(col)
                words.append((wd, col))

        if htmlGen.need_update():
            htmlGen.update(view)

        global all_regs
        for s in all_regs:
            view.erase_regions(s)
        all_regs = []

        i = 0
        for wd in words:
            w, c = wd
            i += 1
            s = "mon_CH" + str(i)
            all_regs.append(s)
            view.add_regions(s, [w], htmlGen.region_name(c))
