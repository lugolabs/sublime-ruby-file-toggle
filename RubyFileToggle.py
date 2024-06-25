import sublime
import sublime_plugin
import re
import os


settings = None


def plugin_loaded():
    global settings
    settings = sublime.load_settings("Ruby File Toggle.sublime-settings")


def is_debug():
    global settings
    return settings.get("debug")


def debug(*args):
    global settings

    if is_debug():
        print("[Ruby File Toggle]", *args)


CREATE_IMPLEMENTATION_FILE_MESSAGE = """
The implementation file doesn't exist.
Do you want to create it?

Path: %s
"""

CREATE_TEST_FILE_MESSAGE = """
The test file doesn't exist.
Do you want to create it?

Path: %s
"""

TEST_TEMPLATE = """\
require "%s_helper"\
"""


class RubyFileToggleCommand(sublime_plugin.WindowCommand):
    is_rails = False
    is_rspec = False
    is_minitest = False
    gemfile_lock_cache = None

    def run(self):
        folders = self.window.folders()

        if len(folders) == 0:
            return

        current_file = self.window.active_view().file_name()
        current_folder = None

        for folder in folders:
            if current_file.startswith(folder):
                current_folder = folder
                break

        if not current_folder:
            return

        self.is_rails = self.depend_on(current_folder, "rails")
        self.is_minitest = self.depend_on(current_folder, "minitest")
        self.is_rspec = self.depend_on(current_folder, "rspec")

        debug("Rails app?", self.is_rails)
        debug("Minitest?", self.is_minitest)
        debug("RSpec?", self.is_rspec)

        if not self.is_minitest and not self.is_rspec:
            debug("Project must depend on either `minitest` or `rspec`, skipping.")
            return

        relative_path = current_file.replace("%s/" % current_folder, "")

        if relative_path.endswith(
                "_spec.rb") or relative_path.endswith("_test.rb"):
            debug("opening implementation file")
            self.open_implementation_file(current_folder, relative_path)
        else:
            debug("opening spec file")
            self.open_test_file(current_folder, relative_path)

    def open_implementation_file(self, folder, file):
        base_path = re.sub(
            r"^(spec|test)\/(.*?)_(spec|test)\.rb$",
            "\\2.rb",
            file)
        debug("base path:", base_path)

        candidates = [base_path, "lib/%s" % base_path, "app/%s" % base_path]
        debug("candidates:", candidates)

        for path in candidates:
            full_path = os.path.join(folder, path)

            if os.path.isfile(full_path):
                # return self.window.open_file(full_path)
                return self.switch_to(full_path)

        debug("implementation file doesn't exist")

        candidates = [
            os.path.join(folder, "app"),
            os.path.join(folder, "lib")
        ]

        target_dir = os.path.join(folder, "lib")

        for candidate in candidates:
            if os.path.isdir(candidate):
                target_dir = candidate
                break

        full_path = os.path.join(target_dir, base_path)
        relative_path = full_path.replace("%s/" % folder, "")
        debug("full path", full_path)
        debug("relative path:", relative_path)

        if not sublime.ok_cancel_dialog(
                CREATE_IMPLEMENTATION_FILE_MESSAGE % relative_path):
            return

        basedir = os.path.dirname(full_path)

        if not os.path.isdir(basedir):
            self.make_dir_for_path(full_path)

        with open(full_path, "w+") as io:
            print("", file=io)

        self.window.open_file(full_path)

    def open_test_file(self, folder, file):
        framework_suffix = "test"

        if self.is_rspec:
            framework_suffix = "spec"

        if self.is_rails:
            regex = r"^(?:app\/)?(.*?)\.rb$"
        else:
            regex = r"^lib\/(.*?)\.rb$"

        replacement = "{suffix}/\\1_{suffix}.rb".format(
            suffix=framework_suffix)
        base_path = re.sub(regex, replacement, file)
        full_path = os.path.join(folder, base_path)
        relative_path = full_path.replace("%s/" % folder, "")

        debug("base path:", base_path)
        debug("full path:", full_path)

        if os.path.isfile(full_path):
            debug("opening existing file")
            self.switch_to(full_path)
            return

        self.window.run_command("open_rspec_file")

        # if not sublime.ok_cancel_dialog(
        #         CREATE_TEST_FILE_MESSAGE % relative_path):
        #     debug("user doesn't want to create file")
        #     return

        # debug("user wants to create a new file")
        # self.make_dir_for_path(full_path)

        # with open(full_path, "w+") as io:
        #     print(TEST_TEMPLATE % framework_suffix, file=io)

        # self.window.open_file(full_path)

    def switch_to(self, file_path):
        group = self.other_group_in_pair()
        file_view = self.window.open_file(file_path)
        self.window.run_command("move_to_group", { "group": group })
        debug("Opened: " + file_path)
        return True

    def other_group_in_pair(self):
        if self.window.active_group() % 2 == 0:
            target_group = self.window.active_group() + 1
        else:
            target_group = self.window.active_group() - 1
        return min(target_group, self.window.num_groups() - 1)

    def make_dir_for_path(self, filepath):
        basedir = os.path.dirname(filepath)

        if not os.path.isdir(basedir):
            os.makedirs(basedir)

    def depend_on(self, folder, gem):
        gemfile_lock = os.path.join(folder, "Gemfile.lock")
        debug("Gemfile.lock:", gemfile_lock)

        if not os.path.isfile(gemfile_lock):
            debug("Gemfile.lock doesn't exist")
            return False

        if not self.gemfile_lock_cache:
            with open(gemfile_lock) as file:
                self.gemfile_lock_cache = file.read()

        return " {gem} ".format(gem=gem) in self.gemfile_lock_cache
