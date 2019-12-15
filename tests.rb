load "./shortcuts"

require "tempfile"
require "test/unit"

# create a tempfile with contents
def tf_contents(contents)
  file = Tempfile.new("shortcuts-test")
  file.write contents
  file.close
  file
end

class TestShortcuts < Test::Unit::TestCase
  def test_empty_file
    tf = tf_contents("")
    assert_equal(parse_config(tf.path), [])
    tf.unlink
  end

  def test_one_shortcut
    contents = <<CONT
[term-htop]
command="termite -e htop"
CONT
    tf = tf_contents(contents)
    sc = parse_config(tf.path)[0]
    assert_equal(sc.name, "term-htop")
    assert_equal(sc.shebang, "#!/bin/sh")
    assert_equal(sc.links, [])
    assert_equal(sc.mode, 0700)
    assert_equal(sc.command, "termite -e htop")
    tf.unlink
  end

  def test_attributes
    contents = <<CONT
[gp]
command="git pull"
mode="0755"
link="gitp"
links=["gpull"]

CONT
    tf = tf_contents(contents)
    sc = parse_config(tf.path)[0]
    assert_equal(sc.name, "gp")
    assert_equal(sc.command, "git pull")
    assert_equal(sc.mode, 0755)
    assert(sc.links.include? "gitp")
    assert(sc.links.include? "gpull")
    assert_equal(sc.shebang, "#!/bin/sh")
    tf.unlink
  end

  def test_invalid_key
    contents = <<CONT
[fails]
something_random=5

CONT
    tf = tf_contents(contents)
    assert_raise(SystemExit) do
      parse_config(tf.path)
    end
    tf.unlink
  end

  def test_command_not_str
    contents = <<CONT
[fails]
command=5

CONT
    tf = tf_contents(contents)
    assert_raise(SystemExit) do
      parse_config(tf.path)
    end
    tf.unlink
  end

  def test_link_not_str
    contents = <<CONT
[fails]
command="date"
link=5

CONT
    tf = tf_contents(contents)
    assert_raise(SystemExit) do
      parse_config(tf.path)
    end
    tf.unlink
  end

  def test_links_not_arr
    contents = <<CONT
[fails]
command="date"
links="getdate"

CONT
    tf = tf_contents(contents)
    assert_raise(SystemExit) do
      parse_config(tf.path)
    end
    tf.unlink
  end

  def test_links_not_str
    contents = <<CONT
[fails]
command="date"
links = [3, 5]

CONT
    tf = tf_contents(contents)
    assert_raise(SystemExit) do
      parse_config(tf.path)
    end
    tf.unlink
  end

  def test_shebang_not_str
    contents = <<CONT
[fails]
command="date"
shebang=55

CONT
    tf = tf_contents(contents)
    assert_raise(SystemExit) do
      parse_config(tf.path)
    end
    tf.unlink
  end

  def test_shebang_mode_not_str
    contents = <<CONT
[fails]
command="date"
mode=0755

CONT
    tf = tf_contents(contents)
    assert_raise(SystemExit) do
      parse_config(tf.path)
    end
    tf.unlink
  end

  def test_incorrect_global_shebang
    contents = <<CONT
default_shebang=5

[term-htop]
command="termite -e htop"

CONT
    tf = tf_contents(contents)
    assert_raise(SystemExit) do
      parse_config(tf.path)
    end
    tf.unlink
  end

  def test_incorrect_global_mode
    contents = <<CONT
default_mode=0755

[term-htop]
command="termite -e htop"

CONT
    tf = tf_contents(contents)
    assert_raise(SystemExit) do
      parse_config(tf.path)
    end
    tf.unlink
  end

  def test_multiple_commands
    contents = <<CONT
[term-htop]
command = "termite -e htop"

[openlinks]
command='''
import sys
import webbrowser

[webbrowser.open(s.strip()) for s in sys.stdin.splitlines()]
'''
shebang = "#!/usr/bin/python"

CONT
    tf = tf_contents(contents)
    thtop, twebpy = parse_config(tf.path)
    assert_equal(thtop.command, "termite -e htop")
    assert_equal(twebpy.shebang, "#!/usr/bin/python")
    assert_equal(twebpy.command.strip.lines.count, 4)
  end

  def test_modify_defaults
    contents = <<CONT
default_shebang = "#!/usr/bin/python"

[openlinks]
command='''
import sys
import webbrowser

[webbrowser.open(s.strip()) for s in sys.stdin.splitlines()]
''' 
[term-ncdu]
shebang = "#!/bin/sh"
command = "termite -e ncdu"


CONT
    tf = tf_contents(contents)
    twebpy, ncdu = parse_config(tf.path)
    assert_equal(twebpy.shebang, "#!/usr/bin/python")
    assert_equal(twebpy.command.strip.lines.count, 4)
    assert_equal(ncdu.shebang, "#!/bin/sh")
    load "./shortcuts"  # re-load to reset default shebang values
  end
end
