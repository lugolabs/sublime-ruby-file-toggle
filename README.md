# Ruby File Toggle for Sublime Text

A plugin that switches from implementation to test file and vice-versa. Supports
minitest and rspec.

## Installation

### Setup Package Control Repository

1. Follow the instructions from https://sublime.fnando.com.
2. Open the command pallete, run “Package Control: Install Package“, then search
   for “Ruby File Toggle“.

### Git Clone

Clone this repository into the Sublime Text “Packages” directory, which is
located where ever the “Preferences” -> “Browse Packages” option in sublime
takes you.

## Usage

By default, you can toggle between files using `super+.`.

You could set up a keyboard shortcut by adding a keybinding like the following:

```json
[
  {
    "keys": ["super+."],
    "command": "ruby_file_toggle",
    "context": [
      {
        "key": "selector",
        "operator": "equal",
        "operand": "source.ruby"
      }
    ]
  }
]
```

Notice that nothing will happen if you don’t have either `minitest` or `rspec`
as your dependency on your Gemfile’s lock file.

## License

Copyright (c) 2020 Nando Vieira

MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION Ruby File Toggle SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
switches from implementation to test file and vice-versa. Supports minitest and
rspec.
