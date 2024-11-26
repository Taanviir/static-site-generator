from textwrap import dedent
from markdown_parser import markdown_to_blocks, block_to_block_type


def main():
    markdown = dedent(
        """\
    # This is heading 1

    ## This is heading 2

    ### This is heading 3

    #### This is heading 4

    ##### This is heading 5

    ###### This is heading 6

    ##This is heading 6

    This is a paragraph of text. It has some **bold** and *italic* words inside of it.

    * This is the first list item in a list block
    * This is a list item
    * This is another list item
    """
    )

    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        print(f"type: {block_type}, {block}")


if __name__ == "__main__":
    main()
