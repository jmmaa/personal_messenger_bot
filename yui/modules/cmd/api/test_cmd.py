from yui.modules.cmd.api import Command
from yui.modules.cmd.api import CommandTree


def test_command_api():
    tree = CommandTree(parent=None, data=Command(name="root", func=lambda: None))

    @tree.command(name="subtreeA")
    def subtreeA():
        return "subtreeA"

    @tree.command(name="subtreeB")
    def subtreeB():
        return "subtreeB"

    assert tree.get_tree(["root", "subtreeA"]).data.func() == "subtreeA"


def test_add_command_tree():
    sub_tree = CommandTree(parent=None, data=Command(name="subroot", func=lambda: None))

    @sub_tree.command(name="subtreeA")
    def subtreeA():
        return "subtreeA"

    @sub_tree.command(name="subtreeB")
    def subtreeB():
        return "subtreeB"

    main_tree = CommandTree(parent=None, data=Command(name="root", func=lambda: None))

    @main_tree.command(name="treeA")
    def treeA():
        return "treeA"

    @main_tree.command(name="treeB")
    def treeB():
        return "treeB"

    main_tree.add_tree(sub_tree)

    assert main_tree.get_tree(["root", "treeA"]).data.func() == "treeA"
    assert main_tree.get_tree(["root", "subroot", "subtreeA"]).data.func() == "subtreeA"
