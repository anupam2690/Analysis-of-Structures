'''
 Testing environment for the twa-class-library
'''
#    |module           |class
from ProfileDB import ProfileDB
from CombinedProfile import CombinedProfile

CHECK_ProfileDB_Combined = True

if CHECK_ProfileDB_Combined:

    # create Profile database
    db = ProfileDB()

    # create first instance of a Combined Profile
    #                           |name         |k    |b  |z   |d  |Tt
    profile_1 = CombinedProfile("Combined_1", 100., 50., 6., 60.3, 2.3)

    # save the instance into Profile database
    db.setdefault("Combined_1", profile_1)

    # create second instance of a Combined Profile
    #                           |name         |k    |b  |z   |d  |Tt
    # profile_2 = CombinedProfile("Combined_2", 100., 75., 10., 60.3, 2.3)

    # save the instance into Profile database
    # db.setdefault("Combined_2", profile_2)

    # create third instance of a Combined Profile
    #                           |name         |k    |b  |z   |d  |Tt
    # profile_3 = CombinedProfile("Combined_3", 120., 80., 8., 60.3, 2.3)

    # save the instance into Profile database
    # db.setdefault("Combined_3", profile_3)

    # print profile instance data
    db.list()

    # profile plotting
    db.plot()







