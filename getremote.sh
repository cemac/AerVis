git remote add upstream https://github.com/wolfiex/AerVis

# Fetch all the branches of that remote into remote-tracking branches,
# such as upstream/main or upstream/master:

git fetch upstream

# Make sure that you're on your main branch:

git checkout master

# Rewrite your main branch so that any commits of yours that
# aren't already in upstream/master are replayed on top of that
# other branch:

git rebase upstream/main
