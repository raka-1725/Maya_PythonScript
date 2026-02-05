import maya.cmds as mc
selection = mc.ls(sl = True)
for item in selection:
    NewController = mc.circle(n = item.replace("jt_drv", "ac"))
    NewGrp = mc.group(NewController, n = item.replace("jt_drv", "ac_drv") + "_grp")
    OffsetGrp = mc.group(NewController, n = NewGrp.replace("grp", "grp_offset"))
    mc.matchTransform(NewGrp, item)
    mc.matchTransform(OffsetGrp, item)
    mc.orientConstraint(NewController, item)
