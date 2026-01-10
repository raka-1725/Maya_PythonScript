import maya.cmds as cmds

class CameraCleanupUI:
    def __init__(self):
        self.window_id = "cameraCleanupWindow"
        self.title = "Camera Cleanup Tool"
        self.size = (300, 150)
        
        if cmds.window(self.window_id, exists=True):
            cmds.deleteUI(self.window_id)
            
        # Generate Window
        self.window = cmds.window(self.window_id, title=self.title, widthHeight=self.size, sizeable=False)
        
        # Layouts
        cmds.columnLayout(adjustableColumn=True, rowSpacing=10, columnOffset=['both', 10])
        
        cmds.separator(height=10, style='none')
        cmds.text(label="Unused Camera Cleaner", font="boldLabelFont", align="center")
        cmds.text(label="Delete all unnecessary cameras in this scene", align="center")
        cmds.separator(height=5)
        
        # CheckBox
        self.skip_render_cams = cmds.checkBox(label=" Protect cameras with specific words", annotation = "Exclude cameras has : render, rendering, shot, cam, from deleting", value=True)
        
        cmds.separator(height=5)
        
        # Execution Button
        cmds.button(label="Clean Up Cameras", height=40, backgroundColor=[0.4, 0.5, 0.4], command=self.execute_cleanup)
        
        cmds.separator(height=10, style='none')
        
        # Show window
        cmds.showWindow(self.window)

    def execute_cleanup(self, *args):
        # Get checkbox flag
        protect_render = cmds.checkBox(self.skip_render_cams, query=True, value=True)
        
        default_cameras = ['persp', 'top', 'front', 'side', 'back', 'bottom', 'left', 'right']
        render_keywords = ['render', 'rendering', 'shot', 'cam']
        
        # Undo Chunk
        cmds.undoInfo(openChunk=True)
        
        try:
            all_camera_shapes = cmds.ls(type='camera')
            cameras_to_check = []

            #avoid overlap
            for shape in all_camera_shapes:
                parent = cmds.listRelatives(shape, parent=True, fullPath=True)[0]
                if parent not in cameras_to_check:
                    cameras_to_check.append(parent)
            
            deleted_count = 0
            
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


                # Rendering cam protection
                is_render_cam = any(key.lower() in short_name.lower() for key in render_keywords)
                if protect_render and is_render_cam:
                    print(f"Protected render camera: {short_name}")
                    continue

                # Execute delete
                try:
                    if cmds.lockNode(cam_transform, query=True, lock=True)[0]:
                        cmds.lockNode(cam_transform, lock=False)
                    cmds.delete(cam_transform)
                    deleted_count += 1
                except Exception as e:
                    print(f"Failed to delete {short_name}: {e}")
            
            # Result
            cmds.confirmDialog(title="Complete", message=f"{deleted_count} cameras deleted.")
            print(f"Cleanup finished. Total deleted: {deleted_count}")

        finally:
            cmds.undoInfo(closeChunk=True)


CameraCleanupUI()