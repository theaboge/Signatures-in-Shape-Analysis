#NEWFIX
import so3.helpers as hp

def crop_curve_based_on_id(curve, id):
    # No per-id crop rules yet for this database (subject 16, animation_id 1-18).
    # The original crop rules were tuned to a different set of recordings and
    # don't correspond to these animations.
    return curve



def get_id_set():
    return [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]

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