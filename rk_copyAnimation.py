# ___________________________________________________________________
# -------------------------------------------------------------------
#                 COPY ANIMATION V02
# -----------------Pieter Vandenhouwe------------------
# ___________________________________________________________________
# -------------------------------------------------------------------


# source
# target
#
# sourceChannel

import maya.cmds as cmds


class CopyAnimation:
    def __init__(self):
        self.source = []
        self.target = []
        self.selectedTargets = []
        self.sourceChannel = None

    # PROCEDURE - storeSource

    def store_source(self, source_name=None):
        sel = cmds.ls(sl=True)

        if source_name: self.source.append(source_name)

    # PROCEDURE - storeTarget

    def store_target(self, target_name=None):
        # sel = cmds.ls(sl=True)
        self.target.clear()
        if target_name: self.target.append(target_name)

    def clear_source(self):
        self.source.clear()

    def clear_target(self):
        self.target.clear()

    def clear_target_channels(self):
        self.selectedTargets.clear()

    def clear_all(self):
        self.source.clear()
        self.target.clear()

    def set_source_channel(self, source_channel):
        self.sourceChannel = source_channel

    def set_target_channel(self, target_channels):
        self.selectedTargets.clear()
        self.selectedTargets.append(target_channels)

    # --------------------------------------------------------------------------------
    # This procedure reverses the selected animation
    # --------------------------------------------------------------------------------

    def invert_keys(self, firstkey, lastkey):

        mediankey = (firstkey + lastkey) / 2
        # calculates the pivotpoint of the keys to be scaled

        res = cmds.scaleKey(f"{self.target[0]}.{self.selectedTargets[0]}", valueScale=-1, timePivot=mediankey)


    # --------------------------------------------------------------------------------
    # This procedure copies all the animation from the source to the selected targets
    # --------------------------------------------------------------------------------

    def copyAnimation(self, all=False, invert=False):
        # If the allState chackbox is ticked, copy all the animation
        if all:
            for i in range(0, len(self.target)):
                cmds.copyKey(self.source[0])
                cmds.pasteKey(self.target[i], option="replaceCompletely")


        # Display a warning if no target channels have been selected
        elif len(self.selectedTargets) is 0:
            print("ERROR// Select at least 1 target channel!")

        # if an individual channel is selected AND if invert is off, copy that animation to the selected curves
        elif len(self.selectedTargets) > 0:

            for i in range(0, len(self.target)):

                cmds.copyKey(self.source[0], at=self.sourceChannel)
                for att in range(0, len(self.selectedTargets)):
                    try:
                        cmds.pasteKey(self.target[i], at=self.selectedTargets[att], option="replaceCompletely")
                    except RuntimeError:
                        pass

        # INVERT THE ANIMATON
        if invert:
            # find the first and last keyframes of the selected channel
            numKeys = cmds.keyframe(f"{self.target[0]}.{self.selectedTargets[0]}", query=True, keyframeCount=True)

            # numKeys = cmds.keyframe(f"{self.source[0]}.{self.sourceChannel}", query=True, keyframeCount=True)
            # self.source[0]
            last = cmds.keyframe(f"{self.target[0]}.{self.selectedTargets[0]}", index=(numKeys - 1, numKeys - 1),
                                 q=True, tc=True)
            # self.source[0]
            first = cmds.keyframe(f"{self.target[0]}.{self.selectedTargets[0]}", index=(0, 0), q=True, tc=True)

            # invert all keys for each object
            for each in self.target:
                #  run invertKeys Procedure
                print(first[0], last[0])
                self.invert_keys(first[0], last[0])