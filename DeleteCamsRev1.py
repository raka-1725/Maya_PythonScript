import maya.cmds as cmds

def cleanup_cameras_pro():
    
    #merging this into one undo command
    cmds.undoInfo(openChunk = True)

    try:


        default_cameras = ['persp', 'top', 'front', 'side', 'back', 'bottom', 'left', 'right']
        #render_cams = ['render', 'rendering', 'shot', 'cam']
        
        
        deleteAll = False


        all_camera_shapes = cmds.ls(type='camera')
        
        #Lists to avoid overlap
        cameras_to_check = []
        for shape in all_camera_shapes:
            parent = cmds.listRelatives(shape, parent=True, fullPath=True)[0]
            if parent not in cameras_to_check:
                cameras_to_check.append(parent)

        for cam_transform in cameras_to_check:
            short_name = cam_transform.split('|')[-1]
            
            # skip maya default cameras
            if cmds.camera(cam_transform, query=True, startupCamera=True):
                continue

            # skip default cameras above
            if short_name.lower() in [n.lower() for n in default_cameras]:
                continue
                
            # skip referenced cameras
            if cmds.referenceQuery(cam_transform, isNodeReferenced=True):
                print(f"Skipping referenced camera: {short_name}")
                continue

            # Detecting render camera
            #is_render_cam = any(key.lower() in short_name.lower() for key in render_cams)
            
            
            if not deleteAll:
                msg = f"Delete Camera '{short_name}' ?"
                buttons = ['Yes', 'Yes to All', 'No', 'Cancel']
                
                #if is_render_cam:
                #    msg = f"WARNING: Potential render camera detected: '{short_name}' ,  Delete Camera '{short_name}' ?"
                

                result = cmds.confirmDialog(
                    title='Delete Camera?',
                    message=msg,
                    button=buttons,
                    defaultButton='No',
                    cancelButton='Cancel',
                    dismissString='Cancel'
                )

                if result == 'Yes to All':
                    deleteAll = True
                elif result == 'No':
                    continue
                elif result == 'Cancel':
                    print("Operation cancelled by user.")
                    break
            
            #Execute
            
            try:
                # check lock
                if cmds.lockNode(cam_transform, query=True, lock=True)[0]:
                    cmds.lockNode(cam_transform, lock=False)
                
                # unlock shape node
                shapes = cmds.listRelatives(cam_transform, shapes=True, fullPath=True) or []
                for s in shapes:
                    if cmds.lockNode(s, query=True, lock=True)[0]:
                        cmds.lockNode(s, lock=False)

                # deleting
                cmds.delete(cam_transform)
                print(f"Deleted: {short_name}")

            except Exception as e:
                print(f"Failed to delete {short_name}: {e}")


    #closing undo block
    finally:
        cmds.undoInfo(closeChunk=True)

cleanup_cameras_pro()