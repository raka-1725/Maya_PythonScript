import maya.cmds as mc
selection = mc.ls(sl= True)
for item in selection:
    NewController = mc.circle(n=item.replace("jt", "ac"))
    NewGrp = mc.group(NewController, n = item.replace("jt","ac") + "_grp")
    mc.matchTransform(NewGrp, item)
    mc.parentConstraint(NewController, item)
