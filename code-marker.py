import sublime
import sublime_plugin
#view.run_command('py_help_me')
#ctrl+shift+o  pacages/user/Default.sublime-keymap

SCOPE, ICON = "markup.deleted", "dot"
regions = {}

class CodeMarkerClearAllCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        for key in list(regions):
            reg = self.view.get_regions(key)
            if reg:
                self.view.erase_regions(key)
                del regions[key]



class CodeMarkerAddCommand(sublime_plugin.TextCommand):
    def _get_new_region_name(self, region):
        return 'reg_{}-{}'.format(region.begin(), region.end())


    def _clear_region(self, key):
        reg = self.view.get_regions(key)
        if reg:
            self.view.erase_regions(key)
            del regions[key]
            return True

        return False


    def _clear_selected_region(self, name):
        res = self._clear_region(name)
        
        if res:
            self.view.show_popup('Deleted', sublime.HIDE_ON_MOUSE_MOVE)


    def _clear_interception_regions(self, region):
        for key in list(regions):
            r = regions[key]
            if((r.begin() >= region.begin() and r.begin() <= region.end())
                 or (r.end() <= region.end() and r.end() >= region.begin())
                 or r.begin() <= region.begin() and r.end() >= region.begin()):
                
                self._clear_region(key)


    def _add_region(self, region):
        reg_name = self._get_new_region_name(region)

        if reg_name in regions:
            print(reg_name)
            self._clear_selected_region(reg_name)
            return

        self._clear_interception_regions(region)
        regions[reg_name] = region
        self.view.add_regions(reg_name, [region], SCOPE, ICON)


    def run(self, edit):
        cursor_position = self.view.sel()[0].begin()
        #self.view.insert(edit, cursor_position, "Hello, World!")
        #selected_text = self.view.substr(self.view.sel()[0])
        #self.view.sel().add(sublime.Region(10, 50))
        selected_region = self.view.sel()[0]
        self._add_region(selected_region)