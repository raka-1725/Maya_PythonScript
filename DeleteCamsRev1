import maya.cmds as cmds

# Default cameras(4 cams)
default_cameras = ['persp', 'top', 'front', 'side' , 'back' , 'bottom' , 'left' , 'right' ]
# Add camera name to protect them from deleting

# PopUp
def show_popup(camera_name):
    result = cmds.confirmDialog(
        title= 'Delete Camera?',
        message=f"Are you sure you want to delete '{camera_name}'?",
        button=['Yes', 'No'],
        defaultButton= 'No',
        cancelButton= 'No',
        dismissString= 'No'
    )
    return result == 'Yes'


# Get all cams
all_cameras = cmds.ls(type= 'camera')

#deleteting extra cams
for cam_shape in all_cameras:
    cam_transform = cmds.listRelatives(cam_shape, parent=True, fullPath=False)[0]

    if cam_transform in default_cameras:
        continue

    has_number = any(char.isdigit() for char in cam_transform)

    if not has_number and not any(cam_transform.startswith(name) for name in default_cameras):
        if not show_popup(cam_transform):
            continue
    try:
        if cmds.lockNode(cam_transform, query=True, lock=True)[0]:
            cmds.lockNode(cam_transform, lock=False)
        
        if cmds.lockNode(cam_shape, query=True, lock=True)[0]:
            cmds.lockNode(cam_shape, lock=False)

        #Executing Delete
        cmds.delete(cam_transform)
        print(f"Deleted camera: {cam_transform}")

    except Exception as e:
        print(f"Could not delete {cam_transform}: {e}")

