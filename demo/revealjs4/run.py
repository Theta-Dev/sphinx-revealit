import sphinx.cmd.build

if __name__ == '__main__':
    sphinx.cmd.build.main(['-M', 'revealjs', '.', '_build', '-a', '-E'])
    # sphinx.cmd.build.main(['-M', 'singlehtml', '.', '_build', '-a', '-E'])
