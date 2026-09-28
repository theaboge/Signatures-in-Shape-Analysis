#NEWFIX
# Defines which animations (by database id) are compared, and any per-animation
# frame-cropping. Updated to match our own rebuilt database (subject 16, ids 1-18).
import so3.helpers as hp

def crop_curve_based_on_id(curve, id):
    # Forward jump trials (11-15) each contain a standstill lead-in and a
    # settling lead-out around the actual jump, of inconsistent length
    # between trials. Left uncropped, this confuses the DP time-alignment
    # for this category specifically (verified: it visibly hurt within-
    # category clustering vs walk/run). A first pass only trimmed the
    # lead-in, and only for 3 of the 5 trials, using a crude "is anything
    # moving at all" threshold on full-body rotation - that under-detected
    # the real jump window, since incidental arm/weight-shift motion during
    # standstill triggered it early.
    #
    # These values instead come from the root joint's vertical translation
    # (frame['root'][1] in the raw .amc data - confirmed empirically to be
    # the height axis, showing a clean crouch/launch/peak/land/settle
    # shape unique to the jump action itself), thresholded at 8% of that
    # trial's peak height deviation from its own baseline, with a 10-frame
    # margin on each side. Resulting window sizes (183-287 frames) land in
    # the same range as the original repo's own crop for its forward-jump
    # ids (start=140, stop=400 - a 260-frame window), which is a good
    # sanity check that this is the right kind of window.
    #
    # Database ids below refer to the rebuilt database holding the exact
    # 27 animations used in the thesis (Fig. 6.2): subjects 16, 13, 35, 02.
    #
    # forward jump
    if id == 18:    # 16_09
        return hp.crop_curve(curve, start=182, stop=448)
    if id == 20:    # 16_05
        return hp.crop_curve(curve, start=59, stop=241)
    if id == 21:    # 16_07
        return hp.crop_curve(curve, start=117, stop=355)
    if id == 22:    # 16_06
        return hp.crop_curve(curve, start=160, stop=346)
    if id == 26:    # 13_13
        return hp.crop_curve(curve, start=73, stop=348)
    if id == 27:    # 13_11
        return hp.crop_curve(curve, start=115, stop=389)
    if id == 28:    # 13_32
        return hp.crop_curve(curve, start=57, stop=302)
    if id == 29:    # 13_19
        return hp.crop_curve(curve, start=101, stop=387)
    # walk with a standstill at the start (65 frames of no travel, measured
    # from root speed) - the thesis notes such pauses were roughly cropped
    if id == 12:    # 16_31
        return hp.crop_curve(curve, start=55)

    return curve



def get_id_set():
    # The exact 27 animations from the thesis (Fig. 6.2):
    #   forward jump (8): 16_05 16_06 16_07 16_09 13_11 13_13 13_19 13_32
    #   run/jog      (9): 16_35 16_36 16_45 16_46 16_56 35_18 35_22 35_26 02_03
    #   walk        (10): 16_15 16_16 16_21 16_22 16_31 16_47 16_58 35_11 35_12 35_32
    return [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 17, 18,
            20, 21, 22, 23, 24, 25, 26, 27, 28, 29]

#OLDCODE:
"""
import so3.helpers as hp

def crop_curve_based_on_id(curve, id):
    #forward jump
    if id == 1503:
        return hp.crop_curve(curve, start=140, stop=400)
    if id == 1497:
        return hp.crop_curve(curve, start=140, stop=400)
    if id == 1638:
        return hp.crop_curve(curve, start=60)
    if id == 1649:
        return hp.crop_curve(curve, start=120)
    if id == 1627:
        return hp.crop_curve(curve, start=70, stop=330)
    if id == 1616:
        return hp.crop_curve(curve, start=70, stop=380)
    if id == 1489:
        return hp.crop_curve(curve, start=100)
    if id == 1493:
        return hp.crop_curve(curve, start=100)

    return curve



#print("fetch animation id set")
#id_set = [2019, 2034, 2041, 2035, 2038,1497]
#id_set = fetch_animation_id_set(count = 100, subject_fkey=70) + id_set
def get_id_set():
    return [1491, 1493, 1497, 1500, 1501, 1502, 1503, 1516, 1521, 1523, 1525, 1528, 1529, 1534, 1537, 1542, 2019, 2034, 2041, 2035, 2038, 1638,1649,1627,1616, 427, 2012]
"""