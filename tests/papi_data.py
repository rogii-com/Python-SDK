from uuid import uuid4

METER_PROJECT_NAME = 'Global project'
METER_PROJECT_ID = uuid4()

FOOT_PROJECT_NAME = 'Global project (ft)'
FOOT_PROJECT_ID = uuid4()

FOOT_METER_PROJECT_NAME = 'Global project (ft-m)'
FOOT_METER_PROJECT_ID = uuid4()

WELL_NAME = 'Lateral'
WELL_XSRF = 1000000.0
WELL_YSRF = 2000000.0
WELL_KB = 100.0
WELL_AZIMUTH = 5.672320068981945
WELL_CONVERGENCE = 0.17453292519944444

ENDLESS_INTERPRETATION_NAME = 'Endless Interpretation'
ENDLESS_INTERPRETATION_ID = uuid4()

TRACE_NAME = 'Bit depth'
START_DATETIME = '2020-09-06 10:00:00.0'
END_DATETIME = '2020-09-06 10:00:10.0'

INTERPRETATION_NAME = 'Interpretation'

STARRED_INTERPRETATION_NAME = 'Starred Interpretation'
STARRED_INTERPRETATION_ID = uuid4()

HORIZON_NAME = 'Horizon'
HORIZON_ID = uuid4()

TARGET_LINE_NAME = 'Target Line'
STARRED_TARGET_LINE_ID = uuid4()
STARRED_TARGET_LINE_NAME = 'Starred Target Line'

STARRED_HORIZON_TOP_NAME = 'Horizon 2'
STARRED_HORIZON_CENTER_NAME = 'Horizon'
STARRED_HORIZON_BOTTOM_NAME = 'Horizon 3'

NESTED_WELL_NAME = 'Nested Well'
STARRED_NESTED_WELL_NAME = 'Starred Nested Well'
STARRED_NESTED_WELL_ID = uuid4()

LOG_NAME = 'GR'

TYPEWELL_NAME = 'Typewell'
TYPEWELL_XSRF = 500000.0
TYPEWELL_YSRF = 600000.0
TYPEWELL_KB = 100.0
TYPEWELL_CONVERGENCE = 0.17453292519944444

STARRED_TOPSET_NAME = 'Starred Topset'
STARRED_TOPSET_ID = uuid4()

STARRED_TOP_TOP_NAME = 'Top'
STARRED_TOP_CENTER_NAME = 'Top 2'
STARRED_TOP_BOTTOM_NAME = 'Top 3'

MUDLOG_NAME = 'Mudlog'

PROJECTS_DATA_RESPONSE = {
    'content': [
        {
            'uuid': METER_PROJECT_ID,
            'name': METER_PROJECT_NAME,
            'measure_unit': 'METER',
            'role': 'MANAGER',
            'accessed_on': '2022-06-30T08:26:30Z',
            'modified_on': '2022-06-24T13:30:32Z'
        },
        {
            'uuid': FOOT_PROJECT_ID,
            'name': FOOT_PROJECT_NAME,
            'measure_unit': 'FOOT',
            'role': 'MANAGER',
            'accessed_on': '2022-05-20T19:56:52Z',
            'modified_on': '2022-05-20T18:17:35Z'
        },
        {
            'uuid': FOOT_METER_PROJECT_ID,
            'name': FOOT_METER_PROJECT_NAME,
            'measure_unit': 'METER_FOOT',
            'role': 'MANAGER',
            'accessed_on': '2022-05-20T19:56:52Z',
            'modified_on': '2022-05-20T18:17:35Z'
        }
    ],
    'offset': 0,
    'limit': 100,
    'total': 3,
    'first': True,
    'last': True
}

VIRTUAL_PROJECTS_DATA_RESPONSE = {
    'content': [
        {
            'uuid': '4e684dbc-37ed-4827-b677-dc0e3febc432',
            'name': 'Virtual project',
            'measure_unit': 'FOOT',
            'role': 'MANAGER',
            'geo_crs': {
                'code': 2194,
                'authority': 'EPSG',
                'name': 'American Samoa 1962 / American Samoa Lambert',
                'measure_unit': 'FOOT_US'
            },
            'parent_uuid': METER_PROJECT_ID,
            'parent_name': METER_PROJECT_NAME,
            'virtual': True,
            'modified_on': '2022-06-24T13:30:32Z'
        },
        {
            'uuid': 'b721009f-f71a-4c35-b6ad-084ca1cd624f',
            'name': 'Virtual project 2',
            'measure_unit': 'METER',
            'role': 'MANAGER',
            'geo_crs': {
                'code': 2194,
                'authority': 'EPSG',
                'name': 'American Samoa 1962 / American Samoa Lambert',
                'measure_unit': 'FOOT_US'
            },
            'parent_uuid': METER_PROJECT_ID,
            'parent_name': METER_PROJECT_NAME,
            'virtual': True,
            'modified_on': '2022-05-20T18:17:35Z'
        }
    ],
    'offset': 0,
    'limit': 100,
    'total': 2,
    'first': True,
    'last': True
}

WELLS_DATA_RESPONSE = {
    'content': [
        {
            'uuid': '85fa6e44-3507-40b6-a7e2-ee07be241ac7',
            'name': WELL_NAME,
            'api': 'Lateral API',
            'operator': 'Lateral Operator',
            'xsrf': {
                'val': WELL_XSRF
            },
            'ysrf': {
                'val': WELL_YSRF
            },
            'xsrf_real': {
                'val': WELL_XSRF
            },
            'ysrf_real': {
                'val': WELL_YSRF
            },
            'kb': {
                'val': WELL_KB
            },
            'convergence': {
                'val': WELL_CONVERGENCE
            },
            'tie_in_tvd': {
                'val': 0.0
            },
            'tie_in_ns': {
                'val': 49.0
            },
            'tie_in_ew': {
                'val': 69.0
            },
            'azimuth': {
                'val': WELL_AZIMUTH
            },
            'starred': {
                'target_line': STARRED_TARGET_LINE_ID,
                'nested_well': STARRED_NESTED_WELL_ID,
                'interpretation': STARRED_INTERPRETATION_ID,
                'topset': STARRED_TOPSET_ID
            }
        },
        {
            'uuid': '95fa6e44-3507-40b6-a7e2-ee07be241ac7',
            'name': 'Lateral 2',
            'api': 'Lateral 2 API',
            'operator': 'Lateral 2 Operator',
            'xsrf': {
                'val': WELL_XSRF
            },
            'ysrf': {
                'val': WELL_YSRF
            },
            'xsrf_real': {
                'val': 3000000.0
            },
            'ysrf_real': {
                'val': 4000000.0
            },
            'kb': {
                'val': 494.0
            },
            'convergence': {
                'val': 0.027453292519944444
            },
            'tie_in_tvd': {
                'val': 125.0
            },
            'tie_in_ns': {
                'val': 150.5
            },
            'tie_in_ew': {
                'val': 250.5
            },
            'azimuth': {
                'val': 5.372320068981945
            },
            'starred': {
                'target_line': STARRED_TARGET_LINE_ID,
                'nested_well': STARRED_NESTED_WELL_ID,
                'interpretation': STARRED_INTERPRETATION_ID
            }
        }
    ],
    'offset': 0,
    'limit': 100,
    'total': 3,
    'first': True,
    'last': True
}

TRAJECTORY_DATA_RESPONSE = {
    'content': [
        {
            'azim': {
                'val': 0
            },
            'incl': {
                'val': 0
            },
            'md': {
                'val': 0
            }
        },
        {
            'azim': {
                'val': 4.324925886442234
            },
            'incl': {
                'val': 0.006981317007977778
            },
            'md': {
                'val': 447.99999999999994
            }
        },
        {
            'azim': {
                'val': 0
            },
            'incl': {
                'val': 0.0017453292519944445
            },
            'md': {
                'val': 500
            }
        },
        {
            'azim': {
                'val': 4.569271981721456
            },
            'incl': {
                'val': 0.005235987755983333
            },
            'md': {
                'val': 601
            }
        },
        {
            'azim': {
                'val': 5.180137219919511
            },
            'incl': {
                'val': 0.010471975511966667
            },
            'md': {
                'val': 847.0000000000001
            }
        },
        {
            'azim': {
                'val': 5.791002458117567
            },
            'incl': {
                'val': 0.003490658503988889
            },
            'md': {
                'val': 1035
            }
        },
        {
            'azim': {
                'val': 0.6597344572538999
            },
            'incl': {
                'val': 0.005235987755983333
            },
            'md': {
                'val': 1224
            }
        },
        {
            'azim': {
                'val': 0.8866272600131777
            },
            'incl': {
                'val': 0.003490658503988889
            },
            'md': {
                'val': 1413
            }
        },
        {
            'azim': {
                'val': 1.0437068926926778
            },
            'incl': {
                'val': 0.005235987755983333
            },
            'md': {
                'val': 1601
            }
        },
        {
            'azim': {
                'val': 2.247984076568844
            },
            'incl': {
                'val': 0.003490658503988889
            },
            'md': {
                'val': 1789.0000000000002
            }
        },
        {
            'azim': {
                'val': 2.300343954128678
            },
            'incl': {
                'val': 0
            },
            'md': {
                'val': 1977
            }
        },
        {
            'azim': {
                'val': 3.1031954100461223
            },
            'incl': {
                'val': 0.005235987755983333
            },
            'md': {
                'val': 2166
            }
        },
        {
            'azim': {
                'val': 3.3475415053253434
            },
            'incl': {
                'val': 0.005235987755983333
            },
            'md': {
                'val': 2354
            }
        },
        {
            'azim': {
                'val': 2.9810223624065113
            },
            'incl': {
                'val': 0.003490658503988889
            },
            'md': {
                'val': 2543
            }
        },
        {
            'azim': {
                'val': 1.3927727430915666
            },
            'incl': {
                'val': 0
            },
            'md': {
                'val': 2732
            }
        },
        {
            'azim': {
                'val': 0.1884955592154
            },
            'incl': {
                'val': 0.0017453292519944445
            },
            'md': {
                'val': 2921
            }
        },
        {
            'azim': {
                'val': 6.27969464867601
            },
            'incl': {
                'val': 0.01221730476396111
            },
            'md': {
                'val': 3108
            }
        },
        {
            'azim': {
                'val': 0.0314159265359
            },
            'incl': {
                'val': 0.008726646259972222
            },
            'md': {
                'val': 3297.0000000000005
            }
        },
        {
            'azim': {
                'val': 5.599016240398178
            },
            'incl': {
                'val': 0.01570796326795
            },
            'md': {
                'val': 3483
            }
        },
        {
            'azim': {
                'val': 5.407030022678789
            },
            'incl': {
                'val': 0.013962634015955556
            },
            'md': {
                'val': 3671
            }
        },
        {
            'azim': {
                'val': 5.249950389999289
            },
            'incl': {
                'val': 0.017453292519944444
            },
            'md': {
                'val': 3858
            }
        },
        {
            'azim': {
                'val': 5.075417464799845
            },
            'incl': {
                'val': 0.017453292519944444
            },
            'md': {
                'val': 4047.0000000000005
            }
        },
        {
            'azim': {
                'val': 5.075417464799845
            },
            'incl': {
                'val': 0.01919862177193889
            },
            'md': {
                'val': 4236
            }
        },
        {
            'azim': {
                'val': 5.1103240498397335
            },
            'incl': {
                'val': 0.017453292519944444
            },
            'md': {
                'val': 4424
            }
        },
        {
            'azim': {
                'val': 5.197590512439454
            },
            'incl': {
                'val': 0.020943951023933333
            },
            'md': {
                'val': 4611
            }
        },
        {
            'azim': {
                'val': 5.180137219919511
            },
            'incl': {
                'val': 0.01919862177193889
            },
            'md': {
                'val': 4799
            }
        },
        {
            'azim': {
                'val': 5.424483315198733
            },
            'incl': {
                'val': 0.013962634015955556
            },
            'md': {
                'val': 4987
            }
        },
        {
            'azim': {
                'val': 5.249950389999289
            },
            'incl': {
                'val': 0.008726646259972222
            },
            'md': {
                'val': 5176
            }
        },
        {
            'azim': {
                'val': 6.017895260876845
            },
            'incl': {
                'val': 0.013962634015955556
            },
            'md': {
                'val': 5364
            }
        },
        {
            'azim': {
                'val': 5.633922825438066
            },
            'incl': {
                'val': 0.01570796326795
            },
            'md': {
                'val': 5550.000000000001
            }
        },
        {
            'azim': {
                'val': 5.337216852599012
            },
            'incl': {
                'val': 0.01919862177193889
            },
            'md': {
                'val': 5739
            }
        },
        {
            'azim': {
                'val': 5.204571829447433
            },
            'incl': {
                'val': 0.022689280275927773
            },
            'md': {
                'val': 5949
            }
        },
        {
            'azim': {
                'val': 2.4644049038161553
            },
            'incl': {
                'val': 0.026179938779916666
            },
            'md': {
                'val': 6044
            }
        },
        {
            'azim': {
                'val': 2.349213173184522
            },
            'incl': {
                'val': 0.03839724354387778
            },
            'md': {
                'val': 6137.000000000001
            }
        },
        {
            'azim': {
                'val': 2.412045026256322
            },
            'incl': {
                'val': 0.033161255787894445
            },
            'md': {
                'val': 6232
            }
        },
        {
            'azim': {
                'val': 2.2514747350728332
            },
            'incl': {
                'val': 0.02443460952792222
            },
            'md': {
                'val': 6326
            }
        },
        {
            'azim': {
                'val': 2.2200588085369333
            },
            'incl': {
                'val': 0.020943951023933333
            },
            'md': {
                'val': 6418
            }
        },
        {
            'azim': {
                'val': 1.8378317023501496
            },
            'incl': {
                'val': 0.01221730476396111
            },
            'md': {
                'val': 6513
            }
        },
        {
            'azim': {
                'val': 2.6232298657476503
            },
            'incl': {
                'val': 0.03839724354387778
            },
            'md': {
                'val': 6607
            }
        },
        {
            'azim': {
                'val': 2.6738444140554884
            },
            'incl': {
                'val': 0.03839724354387778
            },
            'md': {
                'val': 6702
            }
        },
        {
            'azim': {
                'val': 2.576105975943799
            },
            'incl': {
                'val': 0.033161255787894445
            },
            'md': {
                'val': 6797
            }
        },
        {
            'azim': {
                'val': 2.598795256219727
            },
            'incl': {
                'val': 0.029670597283905555
            },
            'md': {
                'val': 6891
            }
        },
        {
            'azim': {
                'val': 2.49756615960405
            },
            'incl': {
                'val': 0.02443460952792222
            },
            'md': {
                'val': 6985.000000000001
            }
        },
        {
            'azim': {
                'val': 2.375393111964439
            },
            'incl': {
                'val': 0.017453292519944444
            },
            'md': {
                'val': 7078
            }
        },
        {
            'azim': {
                'val': 2.427752989524272
            },
            'incl': {
                'val': 0.005235987755983333
            },
            'md': {
                'val': 7171.999999999999
            }
        },
        {
            'azim': {
                'val': 0.6667157742618778
            },
            'incl': {
                'val': 0.013962634015955556
            },
            'md': {
                'val': 7264
            }
        },
        {
            'azim': {
                'val': 1.4782938764392946
            },
            'incl': {
                'val': 0.005235987755983333
            },
            'md': {
                'val': 7357.000000000001
            }
        },
        {
            'azim': {
                'val': 2.52898208613995
            },
            'incl': {
                'val': 0.033161255787894445
            },
            'md': {
                'val': 7452
            }
        },
        {
            'azim': {
                'val': 2.598795256219727
            },
            'incl': {
                'val': 0.04014257279587222
            },
            'md': {
                'val': 7546.000000000001
            }
        },
        {
            'azim': {
                'val': 2.7157323161033555
            },
            'incl': {
                'val': 0.033161255787894445
            },
            'md': {
                'val': 7640
            }
        },
        {
            'azim': {
                'val': 2.7488935718912493
            },
            'incl': {
                'val': 0.026179938779916666
            },
            'md': {
                'val': 7735
            }
        },
        {
            'azim': {
                'val': 2.3544491609405056
            },
            'incl': {
                'val': 0.01570796326795
            },
            'md': {
                'val': 7830.000000000001
            }
        },
        {
            'azim': {
                'val': 1.5463617172670776
            },
            'incl': {
                'val': 0.008726646259972222
            },
            'md': {
                'val': 7925
            }
        },
        {
            'azim': {
                'val': 1.8692476288860498
            },
            'incl': {
                'val': 0.005235987755983333
            },
            'md': {
                'val': 8020
            }
        },
        {
            'azim': {
                'val': 2.3911010752323887
            },
            'incl': {
                'val': 0.005235987755983333
            },
            'md': {
                'val': 8115.000000000001
            }
        },
        {
            'azim': {
                'val': 3.558726344816672
            },
            'incl': {
                'val': 0.013962634015955556
            },
            'md': {
                'val': 8209
            }
        },
        {
            'azim': {
                'val': 3.6442474781644
            },
            'incl': {
                'val': 0.020943951023933333
            },
            'md': {
                'val': 8304
            }
        },
        {
            'azim': {
                'val': 3.5325464060367557
            },
            'incl': {
                'val': 0.013962634015955556
            },
            'md': {
                'val': 8399
            }
        },
        {
            'azim': {
                'val': 1.8133970928222278
            },
            'incl': {
                'val': 0.01221730476396111
            },
            'md': {
                'val': 8494
            }
        },
        {
            'azim': {
                'val': 0.5829399701661444
            },
            'incl': {
                'val': 0.013962634015955556
            },
            'md': {
                'val': 8589
            }
        },
        {
            'azim': {
                'val': 0.10995574287564999
            },
            'incl': {
                'val': 0.013962634015955556
            },
            'md': {
                'val': 8683.000000000002
            }
        },
        {
            'azim': {
                'val': 6.113888369736537
            },
            'incl': {
                'val': 0.013962634015955556
            },
            'md': {
                'val': 8776
            }
        },
        {
            'azim': {
                'val': 5.173155902911533
            },
            'incl': {
                'val': 0.013962634015955556
            },
            'md': {
                'val': 8871
            }
        },
        {
            'azim': {
                'val': 4.694935687865056
            },
            'incl': {
                'val': 0.005235987755983333
            },
            'md': {
                'val': 8964
            }
        },
        {
            'azim': {
                'val': 4.696681017117049
            },
            'incl': {
                'val': 0.01919862177193889
            },
            'md': {
                'val': 9058
            }
        },
        {
            'azim': {
                'val': 5.885250237725266
            },
            'incl': {
                'val': 0.033161255787894445
            },
            'md': {
                'val': 9152.000000000002
            }
        },
        {
            'azim': {
                'val': 0.6771877497738442
            },
            'incl': {
                'val': 0.045378560551855546
            },
            'md': {
                'val': 9247
            }
        },
        {
            'azim': {
                'val': 0.5742133239061722
            },
            'incl': {
                'val': 0.04188790204786667
            },
            'md': {
                'val': 9341
            }
        },
        {
            'azim': {
                'val': 0.4468042885105778
            },
            'incl': {
                'val': 0.03839724354387778
            },
            'md': {
                'val': 9436
            }
        },
        {
            'azim': {
                'val': 1.1938052083642001
            },
            'incl': {
                'val': 0.017453292519944444
            },
            'md': {
                'val': 9530
            }
        },
        {
            'azim': {
                'val': 1.6912240451826168
            },
            'incl': {
                'val': 0.013962634015955556
            },
            'md': {
                'val': 9624
            }
        },
        {
            'azim': {
                'val': 1.5777776438029778
            },
            'incl': {
                'val': 0.006981317007977778
            },
            'md': {
                'val': 9719
            }
        },
        {
            'azim': {
                'val': 5.3354715233470165
            },
            'incl': {
                'val': 0.006981317007977778
            },
            'md': {
                'val': 9813
            }
        },
        {
            'azim': {
                'val': 5.225515780471366
            },
            'incl': {
                'val': 0.008726646259972222
            },
            'md': {
                'val': 9907
            }
        },
        {
            'azim': {
                'val': 5.337216852599012
            },
            'incl': {
                'val': 0.01570796326795
            },
            'md': {
                'val': 10000
            }
        },
        {
            'azim': {
                'val': 5.064945489287878
            },
            'incl': {
                'val': 0.017453292519944444
            },
            'md': {
                'val': 10094.000000000002
            }
        },
        {
            'azim': {
                'val': 5.270894341023222
            },
            'incl': {
                'val': 0.01570796326795
            },
            'md': {
                'val': 10188
            }
        },
        {
            'azim': {
                'val': 0.4625122517785278
            },
            'incl': {
                'val': 0.0314159265359
            },
            'md': {
                'val': 10283
            }
        },
        {
            'azim': {
                'val': 0.6789330790258389
            },
            'incl': {
                'val': 0.03839724354387778
            },
            'md': {
                'val': 10376
            }
        },
        {
            'azim': {
                'val': 0.4537856055185554
            },
            'incl': {
                'val': 0.036651914291883324
            },
            'md': {
                'val': 10470
            }
        },
        {
            'azim': {
                'val': 0.2391101075232388
            },
            'incl': {
                'val': 0.01919862177193889
            },
            'md': {
                'val': 10564
            }
        },
        {
            'azim': {
                'val': 0.010471975511966667
            },
            'incl': {
                'val': 0.01570796326795
            },
            'md': {
                'val': 10662
            }
        },
        {
            'azim': {
                'val': 5.895722213237233
            },
            'incl': {
                'val': 0.017453292519944444
            },
            'md': {
                'val': 10756
            }
        },
        {
            'azim': {
                'val': 5.818927726149477
            },
            'incl': {
                'val': 0.017453292519944444
            },
            'md': {
                'val': 10850
            }
        },
        {
            'azim': {
                'val': 5.7072266540218335
            },
            'incl': {
                'val': 0.022689280275927773
            },
            'md': {
                'val': 10881
            }
        },
        {
            'azim': {
                'val': 5.7613318608336614
            },
            'incl': {
                'val': 0.05410520681182776
            },
            'md': {
                'val': 10913
            }
        },
        {
            'azim': {
                'val': 5.708971983273828
            },
            'incl': {
                'val': 0.11519173063163332
            },
            'md': {
                'val': 10944
            }
        },
        {
            'azim': {
                'val': 5.619960191422111
            },
            'incl': {
                'val': 0.1797689129554278
            },
            'md': {
                'val': 10976
            }
        },
        {
            'azim': {
                'val': 5.5292030703184
            },
            'incl': {
                'val': 0.23736477827124444
            },
            'md': {
                'val': 11007
            }
        },
        {
            'azim': {
                'val': 5.585053606382222
            },
            'incl': {
                'val': 0.2827433388231
            },
            'md': {
                'val': 11039
            }
        },
        {
            'azim': {
                'val': 5.6793013859899215
            },
            'incl': {
                'val': 0.31939525311498335
            },
            'md': {
                'val': 11070
            }
        },
        {
            'azim': {
                'val': 5.703735995517844
            },
            'incl': {
                'val': 0.3508111796508832
            },
            'md': {
                'val': 11101
            }
        },
        {
            'azim': {
                'val': 5.70199066626585
            },
            'incl': {
                'val': 0.3804817769347889
            },
            'md': {
                'val': 11133
            }
        },
        {
            'azim': {
                'val': 5.677556056737928
            },
            'incl': {
                'val': 0.41887902047866665
            },
            'md': {
                'val': 11164.000000000002
            }
        },
        {
            'azim': {
                'val': 5.628686837682083
            },
            'incl': {
                'val': 0.4782202150464776
            },
            'md': {
                'val': 11195
            }
        },
        {
            'azim': {
                'val': 5.597270911146183
            },
            'incl': {
                'val': 0.5375614096142889
            },
            'md': {
                'val': 11226
            }
        },
        {
            'azim': {
                'val': 5.5798176186262385
            },
            'incl': {
                'val': 0.609119908946061
            },
            'md': {
                'val': 11257
            }
        },
        {
            'azim': {
                'val': 5.602506898902167
            },
            'incl': {
                'val': 0.6806784082778333
            },
            'md': {
                'val': 11288
            }
        },
        {
            'azim': {
                'val': 5.640904142446044
            },
            'incl': {
                'val': 0.7365289443416556
            },
            'md': {
                'val': 11319
            }
        },
        {
            'azim': {
                'val': 5.6793013859899215
            },
            'incl': {
                'val': 0.7958701389094667
            },
            'md': {
                'val': 11351
            }
        },
        {
            'azim': {
                'val': 5.689773361501889
            },
            'incl': {
                'val': 0.8429940287133166
            },
            'md': {
                'val': 11383
            }
        },
        {
            'azim': {
                'val': 5.695009349257872
            },
            'incl': {
                'val': 0.8953539062731499
            },
            'md': {
                'val': 11414
            }
        },
        {
            'azim': {
                'val': 5.71420797102981
            },
            'incl': {
                'val': 0.9407324668250056
            },
            'md': {
                'val': 11445
            }
        },
        {
            'azim': {
                'val': 5.7159533002818055
            },
            'incl': {
                'val': 0.9599310885969444
            },
            'md': {
                'val': 11476
            }
        },
        {
            'azim': {
                'val': 5.69850000776186
            },
            'incl': {
                'val': 0.9721483933609053
            },
            'md': {
                'val': 11506
            }
        },
        {
            'azim': {
                'val': 5.677556056737928
            },
            'incl': {
                'val': 1.0053096491488
            },
            'md': {
                'val': 11537.000000000002
            }
        },
        {
            'azim': {
                'val': 5.656612105713995
            },
            'incl': {
                'val': 1.05243353895265
            },
            'md': {
                'val': 11568
            }
        },
        {
            'azim': {
                'val': 5.656612105713995
            },
            'incl': {
                'val': 1.111774733520461
            },
            'md': {
                'val': 11599
            }
        },
        {
            'azim': {
                'val': 5.644394800950033
            },
            'incl': {
                'val': 1.1955505376161943
            },
            'md': {
                'val': 11631
            }
        },
        {
            'azim': {
                'val': 5.635668154690061
            },
            'incl': {
                'val': 1.2880529879718996
            },
            'md': {
                'val': 11662
            }
        },
        {
            'azim': {
                'val': 5.632177496186072
            },
            'incl': {
                'val': 1.3770647798236164
            },
            'md': {
                'val': 11694
            }
        },
        {
            'azim': {
                'val': 5.633922825438066
            },
            'incl': {
                'val': 1.4748032179353054
            },
            'md': {
                'val': 11725.000000000002
            }
        },
        {
            'azim': {
                'val': 5.644394800950033
            },
            'incl': {
                'val': 1.5376350710071054
            },
            'md': {
                'val': 11756
            }
        },
        {
            'azim': {
                'val': 5.644394800950033
            },
            'incl': {
                'val': 1.5515977050230612
            },
            'md': {
                'val': 11787
            }
        },
        {
            'azim': {
                'val': 5.646140130202028
            },
            'incl': {
                'val': 1.570796326795
            },
            'md': {
                'val': 11881
            }
        },
        {
            'azim': {
                'val': 5.651376117958011
            },
            'incl': {
                'val': 1.5952309363229222
            },
            'md': {
                'val': 11976
            }
        },
        {
            'azim': {
                'val': 5.656612105713995
            },
            'incl': {
                'val': 1.5969762655749167
            },
            'md': {
                'val': 12070.000000000002
            }
        },
        {
            'azim': {
                'val': 5.647885459454023
            },
            'incl': {
                'val': 1.5690509975430056
            },
            'md': {
                'val': 12105
            }
        },
        {
            'azim': {
                'val': 5.674065398233939
            },
            'incl': {
                'val': 1.542871058763089
            },
            'md': {
                'val': 12167
            }
        },
        {
            'azim': {
                'val': 5.710717312525822
            },
            'incl': {
                'val': 1.574286985298989
            },
            'md': {
                'val': 12262.000000000002
            }
        },
        {
            'azim': {
                'val': 5.717698629533801
            },
            'incl': {
                'val': 1.6091935703388778
            },
            'md': {
                'val': 12356
            }
        },
        {
            'azim': {
                'val': 5.726425275793773
            },
            'incl': {
                'val': 1.6039575825828944
            },
            'md': {
                'val': 12451
            }
        },
        {
            'azim': {
                'val': 5.729915934297761
            },
            'incl': {
                'val': 1.6022122533309
            },
            'md': {
                'val': 12545
            }
        },
        {
            'azim': {
                'val': 5.719443958785794
            },
            'incl': {
                'val': 1.607448241086883
            },
            'md': {
                'val': 12639.000000000002
            }
        },
        {
            'azim': {
                'val': 5.681046715241917
            },
            'incl': {
                'val': 1.6109388995908722
            },
            'md': {
                'val': 12734
            }
        },
        {
            'azim': {
                'val': 5.674065398233939
            },
            'incl': {
                'val': 1.6022122533309
            },
            'md': {
                'val': 12828
            }
        },
        {
            'azim': {
                'val': 5.6618480934699775
            },
            'incl': {
                'val': 1.5830136315589611
            },
            'md': {
                'val': 12922
            }
        },
        {
            'azim': {
                'val': 5.665338751973967
            },
            'incl': {
                'val': 1.574286985298989
            },
            'md': {
                'val': 13016.000000000002
            }
        },
        {
            'azim': {
                'val': 5.649630788706016
            },
            'incl': {
                'val': 1.5830136315589611
            },
            'md': {
                'val': 13110
            }
        },
        {
            'azim': {
                'val': 5.644394800950033
            },
            'incl': {
                'val': 1.5812683023069665
            },
            'md': {
                'val': 13204.000000000002
            }
        },
        {
            'azim': {
                'val': 5.665338751973967
            },
            'incl': {
                'val': 1.5812683023069665
            },
            'md': {
                'val': 13299
            }
        },
        {
            'azim': {
                'val': 5.653121447210004
            },
            'incl': {
                'val': 1.576032314550983
            },
            'md': {
                'val': 13393
            }
        },
        {
            'azim': {
                'val': 5.642649471698039
            },
            'incl': {
                'val': 1.5795229730549722
            },
            'md': {
                'val': 13487.000000000002
            }
        },
        {
            'azim': {
                'val': 5.656612105713995
            },
            'incl': {
                'val': 1.5690509975430056
            },
            'md': {
                'val': 13581
            }
        },
        {
            'azim': {
                'val': 5.654866776462
            },
            'incl': {
                'val': 1.576032314550983
            },
            'md': {
                'val': 13676
            }
        },
        {
            'azim': {
                'val': 5.668829410477955
            },
            'incl': {
                'val': 1.5725416560469943
            },
            'md': {
                'val': 13770
            }
        },
        {
            'azim': {
                'val': 5.656612105713995
            },
            'incl': {
                'val': 1.5655603390390167
            },
            'md': {
                'val': 13864.000000000002
            }
        },
        {
            'azim': {
                'val': 5.653121447210004
            },
            'incl': {
                'val': 1.5393804002591
            },
            'md': {
                'val': 13958.999999999998
            }
        },
        {
            'azim': {
                'val': 5.665338751973967
            },
            'incl': {
                'val': 1.5236724369911498
            },
            'md': {
                'val': 14051
            }
        },
        {
            'azim': {
                'val': 5.674065398233939
            },
            'incl': {
                'val': 1.5132004614791834
            },
            'md': {
                'val': 14146.000000000002
            }
        },
        {
            'azim': {
                'val': 5.675810727485933
            },
            'incl': {
                'val': 1.520181778487161
            },
            'md': {
                'val': 14241.000000000002
            }
        },
        {
            'azim': {
                'val': 5.672320068981945
            },
            'incl': {
                'val': 1.5254177662431445
            },
            'md': {
                'val': 14335.999999999998
            }
        },
        {
            'azim': {
                'val': 5.695009349257872
            },
            'incl': {
                'val': 1.520181778487161
            },
            'md': {
                'val': 14430
            }
        },
        {
            'azim': {
                'val': 5.681046715241917
            },
            'incl': {
                'val': 1.520181778487161
            },
            'md': {
                'val': 14524
            }
        },
        {
            'azim': {
                'val': 5.646140130202028
            },
            'incl': {
                'val': 1.542871058763089
            },
            'md': {
                'val': 14618.000000000002
            }
        },
        {
            'azim': {
                'val': 5.642649471698039
            },
            'incl': {
                'val': 1.5498523757710663
            },
            'md': {
                'val': 14712
            }
        },
        {
            'azim': {
                'val': 5.6705747397299495
            },
            'incl': {
                'val': 1.576032314550983
            },
            'md': {
                'val': 14806
            }
        },
        {
            'azim': {
                'val': 5.6862827029979
            },
            'incl': {
                'val': 1.5952309363229222
            },
            'md': {
                'val': 14900
            }
        },
        {
            'azim': {
                'val': 5.695009349257872
            },
            'incl': {
                'val': 1.5934856070709271
            },
            'md': {
                'val': 14994.000000000002
            }
        },
        {
            'azim': {
                'val': 5.80845575063751
            },
            'incl': {
                'val': 1.6196655458508444
            },
            'md': {
                'val': 15088
            }
        },
        {
            'azim': {
                'val': 5.770058507093633
            },
            'incl': {
                'val': 1.58650429006295
            },
            'md': {
                'val': 15183
            }
        },
        {
            'azim': {
                'val': 5.792747787369558
            },
            'incl': {
                'val': 1.6109388995908722
            },
            'md': {
                'val': 15276.000000000002
            }
        },
        {
            'azim': {
                'val': 5.782275811857595
            },
            'incl': {
                'val': 1.5952309363229222
            },
            'md': {
                'val': 15369.999999999998
            }
        },
        {
            'azim': {
                'val': 5.717698629533801
            },
            'incl': {
                'val': 1.5777776438029778
            },
            'md': {
                'val': 15463
            }
        },
        {
            'azim': {
                'val': 5.691518690753884
            },
            'incl': {
                'val': 1.5690509975430056
            },
            'md': {
                'val': 15558
            }
        },
        {
            'azim': {
                'val': 5.667084081225961
            },
            'incl': {
                'val': 1.5673056682910107
            },
            'md': {
                'val': 15653.000000000002
            }
        },
        {
            'azim': {
                'val': 5.660102764217983
            },
            'incl': {
                'val': 1.5585790220310385
            },
            'md': {
                'val': 15748.000000000002
            }
        },
        {
            'azim': {
                'val': 5.6618480934699775
            },
            'incl': {
                'val': 1.5446163880150834
            },
            'md': {
                'val': 15843.000000000002
            }
        },
        {
            'azim': {
                'val': 5.6705747397299495
            },
            'incl': {
                'val': 1.5515977050230612
            },
            'md': {
                'val': 15938
            }
        },
        {
            'azim': {
                'val': 5.656612105713995
            },
            'incl': {
                'val': 1.5673056682910107
            },
            'md': {
                'val': 16032
            }
        },
        {
            'azim': {
                'val': 5.660102764217983
            },
            'incl': {
                'val': 1.5812683023069665
            },
            'md': {
                'val': 16126.000000000002
            }
        },
        {
            'azim': {
                'val': 5.623450849926099
            },
            'incl': {
                'val': 1.5812683023069665
            },
            'md': {
                'val': 16220.000000000002
            }
        },
        {
            'azim': {
                'val': 5.619960191422111
            },
            'incl': {
                'val': 1.576032314550983
            },
            'md': {
                'val': 16314
            }
        },
        {
            'azim': {
                'val': 5.619960191422111
            },
            'incl': {
                'val': 1.5830136315589611
            },
            'md': {
                'val': 16409
            }
        },
        {
            'azim': {
                'val': 5.5885442648862105
            },
            'incl': {
                'val': 1.574286985298989
            },
            'md': {
                'val': 16504
            }
        },
        {
            'azim': {
                'val': 5.607742886658148
            },
            'incl': {
                'val': 1.5725416560469943
            },
            'md': {
                'val': 16598
            }
        },
        {
            'azim': {
                'val': 5.614724203666127
            },
            'incl': {
                'val': 1.5620696805350278
            },
            'md': {
                'val': 16692
            }
        },
        {
            'azim': {
                'val': 5.619960191422111
            },
            'incl': {
                'val': 1.5515977050230612
            },
            'md': {
                'val': 16787
            }
        },
        {
            'azim': {
                'val': 5.619960191422111
            },
            'incl': {
                'val': 1.5515977050230612
            },
            'md': {
                'val': 16854
            }
        }
    ]
}

INTERPRETATIONS_DATA_RESPONSE = {
    'content': [
        {
            'uuid': STARRED_INTERPRETATION_ID,
            'name': STARRED_INTERPRETATION_NAME,
            'properties': {
                'cutoff': {
                    'val': 0
                },
                'palette': 10,
                'lightness': 0,
                'transparency': 0,
                'typelogFillUuid': '39980ce2-2961-4a35-8baf-8941e9b0169a',
                'extensionGridUuid': '00000000-0000-0000-0000-000000000000',
                'faultLabelVisible': True,
                'reverse_extension': False,
                'zero_horizon_uuid': '00000000-0000-0000-0000-000000000000',
                'coloredLogsVisible': True,
                'boundaryPointsColor': '#ffa5a5a5',
                'interpretationExtend': {
                    'val': 0
                },
                'boundaryPointsVisible': True,
                'display_hidden_segment': True
            },
            'owner': 3,
            'mode': 'PUBLIC',
            'format': None
        },
        {
            'uuid': 'a4811211-cf40-4b2a-9536-aa7f41b56b08',
            'name': INTERPRETATION_NAME,
            'properties': {
                'cutoff': {
                    'val': 0
                },
                'palette': 10,
                'lightness': 0,
                'transparency': 0,
                'typelogFillUuid': '39980ce2-2961-4a35-8baf-8941e9b0169a',
                'extensionGridUuid': '00000000-0000-0000-0000-000000000000',
                'faultLabelVisible': True,
                'reverse_extension': False,
                'zero_horizon_uuid': '00000000-0000-0000-0000-000000000000',
                'coloredLogsVisible': True,
                'boundaryPointsColor': '#ffa5a5a5',
                'interpretationExtend': {
                    'val': 0
                },
                'boundaryPointsVisible': True,
                'display_hidden_segment': True
            },
            'owner': 1,
            'mode': 'PUBLIC',
            'format': None
        },
        {
            'uuid': '1e78d781-4804-42b6-974f-6f53830d9fb7',
            'name': 'Interpretation 2',
            'properties': {
                'cutoff': {
                    'val': 0
                },
                'palette': 10,
                'lightness': 0,
                'transparency': 0,
                'typelogFillUuid': '39980ce2-2961-4a35-8baf-8941e9b0169a',
                'extensionGridUuid': '00000000-0000-0000-0000-000000000000',
                'faultLabelVisible': True,
                'reverse_extension': False,
                'zero_horizon_uuid': '00000000-0000-0000-0000-000000000000',
                'coloredLogsVisible': True,
                'boundaryPointsColor': '#ffa5a5a5',
                'interpretationExtend': {
                    'val': 0
                },
                'boundaryPointsVisible': True,
                'display_hidden_segment': True
            },
            'owner': 2,
            'mode': 'PUBLIC',
            'format': None
        },
        {
            'uuid': ENDLESS_INTERPRETATION_ID,
            'name': ENDLESS_INTERPRETATION_NAME,
            'properties': {
                'cutoff': {
                    'val': 0
                },
                'palette': 10,
                'lightness': 0,
                'transparency': 0,
                'typelogFillUuid': '39980ce2-2961-4a35-8baf-8941e9b0169a',
                'extensionGridUuid': '00000000-0000-0000-0000-000000000000',
                'faultLabelVisible': True,
                'reverse_extension': False,
                'zero_horizon_uuid': '00000000-0000-0000-0000-000000000000',
                'coloredLogsVisible': True,
                'boundaryPointsColor': '#ffa5a5a5',
                'interpretationExtend': {
                    'val': 0
                },
                'boundaryPointsVisible': True,
                'display_hidden_segment': True
            },
            'owner': 4,
            'mode': 'PUBLIC',
            'format': 'v2',
        },
    ],
    'offset': 0,
    'limit': 100,
    'total': 4,
    'first': True,
    'last': True
}

HORIZONS_DATA_RESPONSE = {
    'content': [
        {
            'uuid': HORIZON_ID,
            'name': HORIZON_NAME
        },
        {
            'uuid': '586a5e44-2a1c-402d-88bf-e82304e8fa2e',
            'name': 'Horizon 2'
        },
        {
            'uuid': '86831e2a-3a0b-4085-9e63-90500a8b47ac',
            'name': 'Horizon 3'
        },
    ],
    'offset': 0,
    'limit': 100,
    'total': 3,
    'first': True,
    'last': True
}

ASSEMBLED_SEGMENTS_DATA_RESPONSE = {
    'assembled_segments': {
        'horizons': {
            '586a5e44-2a1c-402d-88bf-e82304e8fa2e': {
                'tvd': {
                    'val': 11517.84276413585
                },
                'uuid': '586a5e44-2a1c-402d-88bf-e82304e8fa2e'
            },
            HORIZON_ID: {
                'tvd': {
                    'val': 11517.84276413585
                },
                'uuid': HORIZON_ID
            },
            '86831e2a-3a0b-4085-9e63-90500a8b47ac': {
                'tvd': {
                    'val': 11519.84276413585
                },
                'uuid': '86831e2a-3a0b-4085-9e63-90500a8b47ac'
            }
        },
        'segments': [
            {
                'boundary_type': 1,
                'end': {
                    'val': -6.5656962603957885
                },
                'horizon_shifts': {
                    '586a5e44-2a1c-402d-88bf-e82304e8fa2e': {
                        'end': {
                            'val': -6.5656962603957885
                        },
                        'start': {
                            'val': 0
                        },
                        'uuid': '586a5e44-2a1c-402d-88bf-e82304e8fa2e'
                    },
                    HORIZON_ID: {
                        'end': {
                            'val': -6.5656962603957885
                        },
                        'start': {
                            'val': 0
                        },
                        'uuid': HORIZON_ID
                    },
                    '86831e2a-3a0b-4085-9e63-90500a8b47ac': {
                        'end': {
                            'val': -6.5656962603957885
                        },
                        'start': {
                            'val': 0
                        },
                        'uuid': '86831e2a-3a0b-4085-9e63-90500a8b47ac'
                    }
                },
                'md': {
                    'val': 11284.942670449882
                },
                'start': {
                    'val': 0
                },
                'uuid': '17d78c2b-1544-42f9-9ffb-7aa07de5a90c'
            },
            {
                'boundary_type': 1,
                'end': {
                    'val': -18.912379033568882
                },
                'horizon_shifts': {
                    '586a5e44-2a1c-402d-88bf-e82304e8fa2e': {
                        'end': {
                            'val': -18.912379033568882
                        },
                        'start': {
                            'val': -6.565715689306932
                        },
                        'uuid': '586a5e44-2a1c-402d-88bf-e82304e8fa2e'
                    },
                    HORIZON_ID: {
                        'end': {
                            'val': -18.912379033568882
                        },
                        'start': {
                            'val': -6.565715689306932
                        },
                        'uuid': HORIZON_ID
                    },
                    '86831e2a-3a0b-4085-9e63-90500a8b47ac': {
                        'end': {
                            'val': -18.912379033568882
                        },
                        'start': {
                            'val': -6.565715689306932
                        },
                        'uuid': '86831e2a-3a0b-4085-9e63-90500a8b47ac'
                    }
                },
                'md': {
                    'val': 11511
                },
                'start': {
                    'val': -6.565715689306932
                },
                'uuid': 'b8e4b757-3612-4fe0-8fb3-82f3f7a3bcd4'
            },
            {
                'boundary_type': 1,
                'end': {
                    'val': -33.516118275710916
                },
                'horizon_shifts': {
                    '586a5e44-2a1c-402d-88bf-e82304e8fa2e': {
                        'end': {
                            'val': -33.516118275710916
                        },
                        'start': {
                            'val': -18.91237067033499
                        },
                        'uuid': '586a5e44-2a1c-402d-88bf-e82304e8fa2e'
                    },
                    HORIZON_ID: {
                        'end': {
                            'val': -33.516118275710916
                        },
                        'start': {
                            'val': -18.91237067033499
                        },
                        'uuid': HORIZON_ID
                    },
                    '86831e2a-3a0b-4085-9e63-90500a8b47ac': {
                        'end': {
                            'val': -33.516118275710916
                        },
                        'start': {
                            'val': -18.91237067033499
                        },
                        'uuid': '86831e2a-3a0b-4085-9e63-90500a8b47ac'
                    }
                },
                'md': {
                    'val': 11606
                },
                'start': {
                    'val': -18.91237067033499
                },
                'uuid': 'b7b5e05a-f6dd-4a7f-a84c-a44aca48e0ab'
            },
            {
                'boundary_type': 1,
                'end': {
                    'val': -62.39180676689853
                },
                'horizon_shifts': {
                    '586a5e44-2a1c-402d-88bf-e82304e8fa2e': {
                        'end': {
                            'val': -58.95023687660797
                        },
                        'start': {
                            'val': -33.516119686481034
                        },
                        'uuid': '586a5e44-2a1c-402d-88bf-e82304e8fa2e'
                    },
                    HORIZON_ID: {
                        'end': {
                            'val': -58.95023687660797
                        },
                        'start': {
                            'val': -33.516119686481034
                        },
                        'uuid': HORIZON_ID
                    },
                    '86831e2a-3a0b-4085-9e63-90500a8b47ac': {
                        'end': {
                            'val': -58.95023687660797
                        },
                        'start': {
                            'val': -33.516119686481034
                        },
                        'uuid': '86831e2a-3a0b-4085-9e63-90500a8b47ac'
                    }
                },
                'md': {
                    'val': 12186.000000000002
                },
                'start': {
                    'val': -33.5161196864814
                },
                'uuid': 'a482bf78-0224-42fa-808a-5f847ea93b7d'
            },
            {
                'boundary_type': 1,
                'end': {
                    'val': 0
                },
                'horizon_shifts': {
                    '586a5e44-2a1c-402d-88bf-e82304e8fa2e': {
                        'end': {
                            'val': -59.10163924450717
                        },
                        'start': {
                            'val': -58.95023687660797
                        },
                        'uuid': '586a5e44-2a1c-402d-88bf-e82304e8fa2e'
                    },
                    HORIZON_ID: {
                        'end': {
                            'val': -59.10163924450717
                        },
                        'start': {
                            'val': -58.95023687660797
                        },
                        'uuid': HORIZON_ID
                    },
                    '86831e2a-3a0b-4085-9e63-90500a8b47ac': {
                        'end': {
                            'val': -59.10163924450717
                        },
                        'start': {
                            'val': -58.95023687660797
                        },
                        'uuid': '86831e2a-3a0b-4085-9e63-90500a8b47ac'
                    }
                },
                'md': {
                    'val': 13056.70686045735
                },
                'start': {
                    'val': 0
                },
                'uuid': 'c7d83962-def5-4c76-90c0-2477886d45b5'
            },
            {
                'boundary_type': 0,
                'end': {
                    'val': -59.393141961814116
                },
                'horizon_shifts': {
                    '586a5e44-2a1c-402d-88bf-e82304e8fa2e': {
                        'end': {
                            'val': -56.70307051967029
                        },
                        'start': {
                            'val': -51.812185591572415
                        },
                        'uuid': '586a5e44-2a1c-402d-88bf-e82304e8fa2e'
                    },
                    HORIZON_ID: {
                        'end': {
                            'val': -56.70307051967029
                        },
                        'start': {
                            'val': -51.812185591572415
                        },
                        'uuid': HORIZON_ID
                    },
                    '86831e2a-3a0b-4085-9e63-90500a8b47ac': {
                        'end': {
                            'val': -56.70307051967029
                        },
                        'start': {
                            'val': -51.812185591572415
                        },
                        'uuid': '86831e2a-3a0b-4085-9e63-90500a8b47ac'
                    }
                },
                'md': {
                    'val': 13400.753488110999
                },
                'start': {
                    'val': -49.79941990825468
                },
                'uuid': 'd432f117-01bc-4b3b-9dcc-18f0276b74cd'
            },
            {
                'boundary_type': 1,
                'end': {
                    'val': 0
                },
                'horizon_shifts': {
                    '586a5e44-2a1c-402d-88bf-e82304e8fa2e': {
                        'end': {
                            'val': -60.56338690861413
                        },
                        'start': {
                            'val': -56.70307051967029
                        },
                        'uuid': '586a5e44-2a1c-402d-88bf-e82304e8fa2e'
                    },
                    HORIZON_ID: {
                        'end': {
                            'val': -60.56338690861413
                        },
                        'start': {
                            'val': -56.70307051967029
                        },
                        'uuid': HORIZON_ID
                    },
                    '86831e2a-3a0b-4085-9e63-90500a8b47ac': {
                        'end': {
                            'val': -60.56338690861413
                        },
                        'start': {
                            'val': -56.70307051967029
                        },
                        'uuid': '86831e2a-3a0b-4085-9e63-90500a8b47ac'
                    }
                },
                'md': {
                    'val': 13849.900000000045
                },
                'start': {
                    'val': 0
                },
                'uuid': '78f86c64-73e3-4daf-a861-fd7039a4d82a'
            },
            {
                'boundary_type': 0,
                'end': {
                    'val': -110.61396071446408
                },
                'horizon_shifts': {
                    '586a5e44-2a1c-402d-88bf-e82304e8fa2e': {
                        'end': {
                            'val': -103.06310344580925
                        },
                        'start': {
                            'val': -99.99209841093398
                        },
                        'uuid': '586a5e44-2a1c-402d-88bf-e82304e8fa2e'
                    },
                    HORIZON_ID: {
                        'end': {
                            'val': -103.06310344580925
                        },
                        'start': {
                            'val': -99.99209841093398
                        },
                        'uuid': HORIZON_ID
                    },
                    '86831e2a-3a0b-4085-9e63-90500a8b47ac': {
                        'end': {
                            'val': -103.06310344580925
                        },
                        'start': {
                            'val': -99.99209841093398
                        },
                        'uuid': '86831e2a-3a0b-4085-9e63-90500a8b47ac'
                    }
                },
                'md': {
                    'val': 13990.412233060615
                },
                'start': {
                    'val': -103.33964736322979
                },
                'uuid': 'aef9b467-8759-447a-bd83-4eebbd8ec403'
            },
            {
                'boundary_type': 1,
                'end': {
                    'val': 0
                },
                'horizon_shifts': {
                    '586a5e44-2a1c-402d-88bf-e82304e8fa2e': {
                        'end': {
                            'val': -110.61396071446325
                        },
                        'start': {
                            'val': -103.06310344580925
                        },
                        'uuid': '586a5e44-2a1c-402d-88bf-e82304e8fa2e'
                    },
                    HORIZON_ID: {
                        'end': {
                            'val': -110.61396071446325
                        },
                        'start': {
                            'val': -103.06310344580925
                        },
                        'uuid': HORIZON_ID
                    },
                    '86831e2a-3a0b-4085-9e63-90500a8b47ac': {
                        'end': {
                            'val': -110.61396071446325
                        },
                        'start': {
                            'val': -103.06310344580925
                        },
                        'uuid': '86831e2a-3a0b-4085-9e63-90500a8b47ac'
                    }
                },
                'md': {
                    'val': 14151.700000000004
                },
                'start': {
                    'val': 0
                },
                'uuid': '212c1744-1fce-414a-a569-15be33a2e863'
            },
            {
                'boundary_type': 1,
                'end': {
                    'val': -118.64063807436037
                },
                'horizon_shifts': {
                    '586a5e44-2a1c-402d-88bf-e82304e8fa2e': {
                        'end': {
                            'val': -118.64063807436037
                        },
                        'start': {
                            'val': -110.61403385396254
                        },
                        'uuid': '586a5e44-2a1c-402d-88bf-e82304e8fa2e'
                    },
                    HORIZON_ID: {
                        'end': {
                            'val': -118.64063807436037
                        },
                        'start': {
                            'val': -110.61403385396254
                        },
                        'uuid': HORIZON_ID
                    },
                    '86831e2a-3a0b-4085-9e63-90500a8b47ac': {
                        'end': {
                            'val': -118.64063807436037
                        },
                        'start': {
                            'val': -110.61403385396254
                        },
                        'uuid': '86831e2a-3a0b-4085-9e63-90500a8b47ac'
                    }
                },
                'md': {
                    'val': 14240.500000000002
                },
                'start': {
                    'val': -110.61403385396254
                },
                'uuid': '17cb4109-690e-4f45-a39a-a64532e25eb9'
            },
            {
                'boundary_type': 1,
                'end': {
                    'val': -141.0744362926588
                },
                'horizon_shifts': {
                    '586a5e44-2a1c-402d-88bf-e82304e8fa2e': {
                        'end': {
                            'val': -135.60868693330121
                        },
                        'start': {
                            'val': -118.6403753720424
                        },
                        'uuid': '586a5e44-2a1c-402d-88bf-e82304e8fa2e'
                    },
                    HORIZON_ID: {
                        'end': {
                            'val': -135.60868693330121
                        },
                        'start': {
                            'val': -118.6403753720424
                        },
                        'uuid': HORIZON_ID
                    },
                    '86831e2a-3a0b-4085-9e63-90500a8b47ac': {
                        'end': {
                            'val': -135.60868693330121
                        },
                        'start': {
                            'val': -118.6403753720424
                        },
                        'uuid': '86831e2a-3a0b-4085-9e63-90500a8b47ac'
                    }
                },
                'md': {
                    'val': 14466.000000000002
                },
                'start': {
                    'val': -118.6403753720431
                },
                'uuid': '200b0a28-ffc6-483e-99c7-2168ac7119b4'
            },
            {
                'boundary_type': 1,
                'end': {
                    'val': 0
                },
                'horizon_shifts': {
                    '586a5e44-2a1c-402d-88bf-e82304e8fa2e': {
                        'end': {
                            'val': -154.195111448762
                        },
                        'start': {
                            'val': -135.60868693330121
                        },
                        'uuid': '586a5e44-2a1c-402d-88bf-e82304e8fa2e'
                    },
                    HORIZON_ID: {
                        'end': {
                            'val': -154.195111448762
                        },
                        'start': {
                            'val': -135.60868693330121
                        },
                        'uuid': HORIZON_ID
                    },
                    '86831e2a-3a0b-4085-9e63-90500a8b47ac': {
                        'end': {
                            'val': -154.195111448762
                        },
                        'start': {
                            'val': -135.60868693330121
                        },
                        'uuid': '86831e2a-3a0b-4085-9e63-90500a8b47ac'
                    }
                },
                'md': {
                    'val': 14565.360000000022
                },
                'start': {
                    'val': 0
                },
                'uuid': 'faa9cc04-7841-4b0a-989d-da0d25be8a7d'
            },
            {
                'boundary_type': 0,
                'end': {
                    'val': -210.65888770893307
                },
                'horizon_shifts': {
                    '586a5e44-2a1c-402d-88bf-e82304e8fa2e': {
                        'end': {
                            'val': -211.69246022414336
                        },
                        'start': {
                            'val': -213.8141818373515
                        },
                        'uuid': '586a5e44-2a1c-402d-88bf-e82304e8fa2e'
                    },
                    HORIZON_ID: {
                        'end': {
                            'val': -211.69246022414336
                        },
                        'start': {
                            'val': -213.8141818373515
                        },
                        'uuid': HORIZON_ID
                    },
                    '86831e2a-3a0b-4085-9e63-90500a8b47ac': {
                        'end': {
                            'val': -211.69246022414336
                        },
                        'start': {
                            'val': -213.8141818373515
                        },
                        'uuid': '86831e2a-3a0b-4085-9e63-90500a8b47ac'
                    }
                },
                'md': {
                    'val': 14605.513625420313
                },
                'start': {
                    'val': -214.98207144576187
                },
                'uuid': 'c957b420-5c52-414e-902f-77005c3d12ea'
            },
            {
                'boundary_type': 1,
                'end': {
                    'val': 0
                },
                'horizon_shifts': {
                    '586a5e44-2a1c-402d-88bf-e82304e8fa2e': {
                        'end': {
                            'val': -215.79805967196262
                        },
                        'start': {
                            'val': -211.69246022414336
                        },
                        'uuid': '586a5e44-2a1c-402d-88bf-e82304e8fa2e'
                    },
                    HORIZON_ID: {
                        'end': {
                            'val': -215.79805967196262
                        },
                        'start': {
                            'val': -211.69246022414336
                        },
                        'uuid': HORIZON_ID
                    },
                    '86831e2a-3a0b-4085-9e63-90500a8b47ac': {
                        'end': {
                            'val': -215.79805967196262
                        },
                        'start': {
                            'val': -211.69246022414336
                        },
                        'uuid': '86831e2a-3a0b-4085-9e63-90500a8b47ac'
                    }
                },
                'md': {
                    'val': 14795.660000000045
                },
                'start': {
                    'val': 0
                },
                'uuid': '393d4368-b131-47a3-b9cc-019e548cf126'
            },
            {
                'boundary_type': 1,
                'end': {
                    'val': 0
                },
                'horizon_shifts': {
                    '586a5e44-2a1c-402d-88bf-e82304e8fa2e': {
                        'end': {
                            'val': -221.2564026611872
                        },
                        'start': {
                            'val': -215.79805967196262
                        },
                        'uuid': '586a5e44-2a1c-402d-88bf-e82304e8fa2e'
                    },
                    HORIZON_ID: {
                        'end': {
                            'val': -221.2564026611872
                        },
                        'start': {
                            'val': -215.79805967196262
                        },
                        'uuid': HORIZON_ID
                    },
                    '86831e2a-3a0b-4085-9e63-90500a8b47ac': {
                        'end': {
                            'val': -221.2564026611872
                        },
                        'start': {
                            'val': -215.79805967196262
                        },
                        'uuid': '86831e2a-3a0b-4085-9e63-90500a8b47ac'
                    }
                },
                'md': {
                    'val': 14976.140000000043
                },
                'start': {
                    'val': 0
                },
                'uuid': 'ff743f11-6101-42a8-8870-724189962750'
            },
            {
                'boundary_type': 1,
                'end': {
                    'val': 0
                },
                'horizon_shifts': {
                    '586a5e44-2a1c-402d-88bf-e82304e8fa2e': {
                        'end': {
                            'val': -229.80925200626916
                        },
                        'start': {
                            'val': -221.2564026611872
                        },
                        'uuid': '586a5e44-2a1c-402d-88bf-e82304e8fa2e'
                    },
                    HORIZON_ID: {
                        'end': {
                            'val': -229.80925200626916
                        },
                        'start': {
                            'val': -221.2564026611872
                        },
                        'uuid': HORIZON_ID
                    },
                    '86831e2a-3a0b-4085-9e63-90500a8b47ac': {
                        'end': {
                            'val': -229.80925200626916
                        },
                        'start': {
                            'val': -221.2564026611872
                        },
                        'uuid': '86831e2a-3a0b-4085-9e63-90500a8b47ac'
                    }
                },
                'md': {
                    'val': 15243.45000000002
                },
                'start': {
                    'val': 0
                },
                'uuid': 'f4178ffa-f443-4a0b-bee0-33925e0458ff'
            },
            {
                'boundary_type': 1,
                'end': {
                    'val': 0
                },
                'horizon_shifts': {
                    '586a5e44-2a1c-402d-88bf-e82304e8fa2e': {
                        'end': {
                            'val': -230.16893424342015
                        },
                        'start': {
                            'val': -229.80925200626916
                        },
                        'uuid': '586a5e44-2a1c-402d-88bf-e82304e8fa2e'
                    },
                    HORIZON_ID: {
                        'end': {
                            'val': -230.16893424342015
                        },
                        'start': {
                            'val': -229.80925200626916
                        },
                        'uuid': HORIZON_ID
                    },
                    '86831e2a-3a0b-4085-9e63-90500a8b47ac': {
                        'end': {
                            'val': -230.16893424342015
                        },
                        'start': {
                            'val': -229.80925200626916
                        },
                        'uuid': '86831e2a-3a0b-4085-9e63-90500a8b47ac'
                    }
                },
                'md': {
                    'val': 15501.950000000032
                },
                'start': {
                    'val': 0
                },
                'uuid': '01dda0be-8d5f-4d00-aba8-8bb9cc39a50a'
            },
            {
                'boundary_type': 1,
                'end': {
                    'val': -235.85437670843604
                },
                'horizon_shifts': {
                    '586a5e44-2a1c-402d-88bf-e82304e8fa2e': {
                        'end': {
                            'val': -235.85437670843567
                        },
                        'start': {
                            'val': -230.16893424342015
                        },
                        'uuid': '586a5e44-2a1c-402d-88bf-e82304e8fa2e'
                    },
                    HORIZON_ID: {
                        'end': {
                            'val': -235.85437670843567
                        },
                        'start': {
                            'val': -230.16893424342015
                        },
                        'uuid': HORIZON_ID
                    },
                    '86831e2a-3a0b-4085-9e63-90500a8b47ac': {
                        'end': {
                            'val': -235.85437670843567
                        },
                        'start': {
                            'val': -230.16893424342015
                        },
                        'uuid': '86831e2a-3a0b-4085-9e63-90500a8b47ac'
                    }
                },
                'md': {
                    'val': 15613.183002760585
                },
                'start': {
                    'val': -229.73977518065405
                },
                'uuid': 'a5e7554a-fd09-483b-92eb-ad029771996a'
            },
            {
                'boundary_type': 1,
                'end': {
                    'val': -254.64365643654796
                },
                'horizon_shifts': {
                    '586a5e44-2a1c-402d-88bf-e82304e8fa2e': {
                        'end': {
                            'val': -254.64365643654796
                        },
                        'start': {
                            'val': -235.8287914731423
                        },
                        'uuid': '586a5e44-2a1c-402d-88bf-e82304e8fa2e'
                    },
                    HORIZON_ID: {
                        'end': {
                            'val': -254.64365643654796
                        },
                        'start': {
                            'val': -235.8287914731423
                        },
                        'uuid': HORIZON_ID
                    },
                    '86831e2a-3a0b-4085-9e63-90500a8b47ac': {
                        'end': {
                            'val': -254.64365643654796
                        },
                        'start': {
                            'val': -235.8287914731423
                        },
                        'uuid': '86831e2a-3a0b-4085-9e63-90500a8b47ac'
                    }
                },
                'md': {
                    'val': 15967.5
                },
                'start': {
                    'val': -235.8287914731423
                },
                'uuid': '7bfea2b5-fbe4-42f7-ae83-41316f79e1d9'
            }
        ]
    }
}

TARGET_LINES_DATA_RESPONSE = {
    'content': [
        {
            'uuid': STARRED_TARGET_LINE_ID,
            'name': STARRED_TARGET_LINE_NAME,
            'azimuth': {
                'val': 324.9999999999999
            },
            'delta_tvd': {
                'val': 19.46959181839702
            },
            'delta_vs': {
                'val': 3377.727551431245
            },
            'inclination': {
                'val': 89.66974450459126
            },
            'length': {
                'val': 3377.783663395759
            },
            'origin_base_corridor_tvd': {
                'undefined': True
            },
            'origin_md': {
                'undefined': True
            },
            'origin_top_corridor_tvd': {
                'undefined': True
            },
            'origin_tvd': {
                'val': 11488.203352355784
            },
            'origin_vs': {
                'val': 6044.52554257121
            },
            'origin_x': {
                'val': 496536.37744074466
            },
            'origin_y': {
                'val': 604953.7485579867
            },
            'origin_z': {
                'val': -11094.203352355784
            },
            'target_base_corridor_tvd': {
                'undefined': True
            },
            'target_md': {
                'undefined': True
            },
            'target_top_corridor_tvd': {
                'undefined': True
            },
            'target_tvd': {
                'val': 11507.67294417418
            },
            'target_vs': {
                'val': 9422.253094002455
            },
            'target_x': {
                'val': 494598.99250883
            },
            'target_y': {
                'val': 607720.6209867928
            },
            'target_z': {
                'val': -11113.67294417418
            },
            'tvd_vs': {
                'val': 11453.362044625126
            }
        },
        {
            'uuid': 'ace335a9-bb9e-4f7a-b33d-a625b71e764e',
            'name': TARGET_LINE_NAME,
            'azimuth': {
                'val': 324.9999999999999
            },
            'delta_tvd': {
                'val': 19.46959181839702
            },
            'delta_vs': {
                'val': 3377.727551431245
            },
            'inclination': {
                'val': 89.66974450459126
            },
            'length': {
                'val': 3377.783663395759
            },
            'origin_base_corridor_tvd': {
                'undefined': True
            },
            'origin_md': {
                'undefined': True
            },
            'origin_top_corridor_tvd': {
                'undefined': True
            },
            'origin_tvd': {
                'val': 11488.203352355784
            },
            'origin_vs': {
                'val': 6044.52554257121
            },
            'origin_x': {
                'val': 496536.37744074466
            },
            'origin_y': {
                'val': 604953.7485579867
            },
            'origin_z': {
                'val': -11094.203352355784
            },
            'target_base_corridor_tvd': {
                'undefined': True
            },
            'target_md': {
                'undefined': True
            },
            'target_top_corridor_tvd': {
                'undefined': True
            },
            'target_tvd': {
                'val': 11507.67294417418
            },
            'target_vs': {
                'val': 9422.253094002455
            },
            'target_x': {
                'val': 494598.99250883
            },
            'target_y': {
                'val': 607720.6209867928
            },
            'target_z': {
                'val': -11113.67294417418
            },
            'tvd_vs': {
                'val': 11453.362044625126
            }
        },
        {
            'uuid': 'b8a72c7a-94c7-4f25-9f72-12f8013d06a5',
            'name': 'Target Line 2',
            'azimuth': {
                'val': 324.9999999999999
            },
            'delta_tvd': {
                'val': 19.46959181839702
            },
            'delta_vs': {
                'val': 3377.727551431245
            },
            'inclination': {
                'val': 89.66974450459126
            },
            'length': {
                'val': 3377.783663395759
            },
            'origin_base_corridor_tvd': {
                'undefined': True
            },
            'origin_md': {
                'undefined': True
            },
            'origin_top_corridor_tvd': {
                'undefined': True
            },
            'origin_tvd': {
                'val': 11488.203352355784
            },
            'origin_vs': {
                'val': 6044.52554257121
            },
            'origin_x': {
                'val': 496536.37744074466
            },
            'origin_y': {
                'val': 604953.7485579867
            },
            'origin_z': {
                'val': -11094.203352355784
            },
            'target_base_corridor_tvd': {
                'undefined': True
            },
            'target_md': {
                'undefined': True
            },
            'target_top_corridor_tvd': {
                'undefined': True
            },
            'target_tvd': {
                'val': 11507.67294417418
            },
            'target_vs': {
                'val': 9422.253094002455
            },
            'target_x': {
                'val': 494598.99250883
            },
            'target_y': {
                'val': 607720.6209867928
            },
            'target_z': {
                'val': -11113.67294417418
            },
            'tvd_vs': {
                'val': 11453.362044625126
            }
        }
    ],
    'offset': 0,
    'limit': 100,
    'total': 3,
    'first': True,
    'last': True
}

NESTED_WELLS_DATA_RESPONSE = {
    'content': [
        {
            'uuid': STARRED_NESTED_WELL_ID,
            'name': STARRED_NESTED_WELL_NAME,
            'api': 'Starred Nested Well API',
            'operator': 'Operator',
            'xsrf': {
                'val': WELL_XSRF
            },
            'ysrf': {
                'val': WELL_YSRF
            },
            'xsrf_real': {
                'val': 3000000.0
            },
            'ysrf_real': {
                'val': 4000000.0
            },
            'kb': {
                'val': WELL_KB
            },
            'convergence': {
                'val': WELL_CONVERGENCE
            },
            'tie_in_tvd': {
                'val': 125.0
            },
            'tie_in_ns': {
                'val': 150.5
            },
            'tie_in_ew': {
                'val': 250.5
            },
            'azimuth': {
                'val': WELL_AZIMUTH
            }
        },
        {
            'uuid': 'afbbe18b-511d-4ef2-b65c-b70eddc49731',
            'name': NESTED_WELL_NAME,
            'api': 'Nested Well API',
            'operator': 'Nested Well Operator',
            'xsrf': {
                'val': WELL_XSRF
            },
            'ysrf': {
                'val': WELL_YSRF
            },
            'xsrf_real': {
                'val': 3000000.0
            },
            'ysrf_real': {
                'val': 4000000.0
            },
            'kb': {
                'undefined': True
            },
            'convergence': {
                'val': 0.017453292519944444
            },
            'tie_in_tvd': {
                'val': 125.0
            },
            'tie_in_ns': {
                'val': 150.5
            },
            'tie_in_ew': {
                'val': 250.5
            },
            'azimuth': {
                'val': 5.672320068981945
            }
        },
        {
            'uuid': 'bfbbe18b-511d-4ef2-b65c-b70eddc49731',
            'name': 'Nested Well 2',
            'api': 'Nested Well 2 API',
            'operator': 'Nested Well 2 Operator',
            'xsrf': {
                'val': WELL_XSRF
            },
            'ysrf': {
                'val': WELL_YSRF
            },
            'xsrf_real': {
                'val': 3000000.0
            },
            'ysrf_real': {
                'val': 4000000.0
            },
            'kb': {
                'undefined': True
            },
            'convergence': {
                'val': 0.027453292519944444
            },
            'tie_in_tvd': {
                'undefined': True
            },
            'tie_in_ns': {
                'undefined': True
            },
            'tie_in_ew': {
                'undefined': True
            },
            'azimuth': {
                'val': 4.672320068981945
            }
        }
    ],
    'offset': 0,
    'limit': 100,
    'total': 3,
    'first': True,
    'last': True
}

LOGS_DATA_RESPONSE = {
    'content': [
        {
            'name': LOG_NAME,
            'uuid': '1b6424cf-1af1-4bdc-a371-561063689b94'
        },
        {
            'name': 'Gamma Ray',
            'uuid': '1070fbaf-25e2-4ede-807a-98a1c2e0f763'
        }
    ],
    'offset': 0,
    'limit': 10,
    'total': 2,
    'first': True,
    'last': True
}

LOG_POINTS_DATA_RESPONSE = {
    'log_points': [
        {
            'data': {
                'val': -3688.6927
            },
            'md': {
                'val': 744.6263999999999
            }
        },
        {
            'data': {
                'val': 16.581
            },
            'md': {
                'val': 744.7787999999999
            }
        },
        {
            'data': {
                'val': -11.85
            },
            'md': {
                'val': 744.9311999999999
            }
        },
        {
            'data': {
                'val': 15.187
            },
            'md': {
                'val': 745.0835999999999
            }
        },
        {
            'data': {
                'val': -4.363
            },
            'md': {
                'val': 745.2359999999999
            }
        },
        {
            'data': {
                'val': -40.475
            },
            'md': {
                'val': 745.3883999999999
            }
        },
        {
            'data': {
                'val': 61.463
            },
            'md': {
                'val': 745.5407999999999
            }
        },
        {
            'data': {
                'val': 82.305
            },
            'md': {
                'val': 745.6931999999999
            }
        },
        {
            'data': {
                'val': 114.139
            },
            'md': {
                'val': 745.8455999999999
            }
        },
        {
            'data': {
                'val': 144.503
            },
            'md': {
                'val': 745.9979999999999
            }
        }
    ]
}


HORIZONS_TVT_DATA_RESPONSE = {
    'content': [
        {
            'azimuth': {
                'val': 71.543
            },
            'horizons': [
                {
                    'name': HORIZON_NAME,
                    'tvdss': {
                        'val': 22.965879265091868
                    },
                    'uuid': HORIZON_ID
                }, {
                    'name': 'Horizon 2',
                    'tvdss': {
                        'val': -3257.8740157480324
                    },
                    'uuid': '586a5e44-2a1c-402d-88bf-e82304e8fa2e'
                }
            ],
            'inclination': {
                'val': 0
            },
            'kb': {
                'val': 22.965879265091868
            },
            'md': {
                'val': 0
            },
            'tvt': {
                'val': 0
            },
            'vs_azim': {
                'azimuth': {
                    'val': 0
                },
                'vs': {
                    'val': 3.280839895013124
                }
            },
            'well_name': WELL_NAME,
            'x': {
                'val': 19.68503937007874
            },
            'y': {
                'val': 36.08923884514436
            },
            'z': {
                'val': 22.965879265091868
            }
        }, {
            'azimuth': {
                'val': 149.253
            },
            'horizons': [
                {
                    'name': HORIZON_NAME,
                    'tvdss': {
                        'val': 22.965879265091868
                    },
                    'uuid': HORIZON_ID
                }, {
                    'name': 'Horizon 2',
                    'tvdss': {
                        'val': -3257.8740157480324
                    },
                    'uuid': '586a5e44-2a1c-402d-88bf-e82304e8fa2e'
                }
            ],
            'inclination': {
                'val': 1.33
            },
            'kb': {
                'val': 22.965879265091868
            },
            'md': {
                'val': 3280.839895013124
            },
            'tvt': {
                'val': 3280.0196063852154
            },
            'vs_azim': {
                'azimuth': {
                    'val': 0
                },
                'vs': {
                    'val': -60.07861128428071
                }
            },
            'well_name': WELL_NAME,
            'x': {
                'val': 53.715600823725445
            },
            'y': {
                'val': -27.270212334149477
            },
            'z': {
                'val': -3257.0537271201238
            }
        }
    ]
}


TYPEWELLS_DATA_RESPONSE = {
    'content': [
        {
            'uuid': 'fc1e3e0c-12ed-4cc6-adcf-6a14dc3db7ae',
            'name': TYPEWELL_NAME,
            'api': 'Typewell API',
            'xsrf': {
                'val': TYPEWELL_XSRF
            },
            'ysrf': {
                'val': TYPEWELL_YSRF
            },
            'xsrf_real': {
                'val': 500000.0
            },
            'ysrf_real': {
                'val': 600000.0
            },
            'kb': {
                'val': TYPEWELL_KB
            },
            'convergence': {
                'val': TYPEWELL_CONVERGENCE
            },
            'tie_in_tvd': {
                'val': 125.0
            },
            'tie_in_ns': {
                'val': 150.5
            },
            'tie_in_ew': {
                'val': 250.5
            }
        },
        {
            'name': 'Typewell 2',
            'uuid': '66a1dd35-6bc2-4d01-a550-c5054d956146',
            'api': 'Typewell 2 API',
            'xsrf': {
                'val': TYPEWELL_XSRF
            },
            'ysrf': {
                'val': TYPEWELL_YSRF
            },
            'xsrf_real': {
                'val': 500000.0
            },
            'ysrf_real': {
                'val': 600000.0
            },
            'kb': {
                'val': TYPEWELL_KB
            },
            'convergence': {
                'val': TYPEWELL_CONVERGENCE
            },
            'tie_in_tvd': {
                'val': 125.0
            },
            'tie_in_ns': {
                'val': 150.5
            },
            'tie_in_ew': {
                'val': 250.5
            }
        }
    ],
    'offset': 0,
    'limit': 100,
    'total': 2,
    'first': True,
    'last': True
}

TOPSETS_DATA_RESPONSE = {
    'content': [
        {
            'name': STARRED_TOPSET_NAME,
            'uuid': STARRED_TOPSET_ID
        },
        {
            'name': 'Topset 2',
            'uuid': 'fb20162a-0c47-4eea-8bc5-a56b1bd856dc'
        },
        {
            'name': 'Topset 3',
            'uuid': '7e86bd40-124d-466a-9592-24811963fa12'
        },
        {
            'name': 'Topset 4',
            'uuid': '95c15955-af34-4b41-ba6a-c1abb979ea68'
        }
    ],
    'offset': 0,
    'limit': 10,
    'total': 4,
    'first': True,
    'last': True
}

TOPS_DATA_RESPONSE = {
    'content': [
        {
            'md': {
                'val': 9.842519685039372
            },
            'name': STARRED_TOP_TOP_NAME,
            'topset_name': 'Topset',
            'uuid': 'c0332dab-9468-4b27-b1f6-3d4d7c875ecf'
        },
        {
            'md': {
                'val': 13.123359580052496
            },
            'name': STARRED_TOP_CENTER_NAME,
            'topset_name': 'Topset',
            'uuid': '3e5f09a8-0a0a-4722-ab1a-c52c769fc72b'
        },
        {
            'md': {
                'val': 15.443359580052496
            },
            'name': STARRED_TOP_BOTTOM_NAME,
            'topset_name': 'Topset',
            'uuid': '77b3db2b-83f0-4122-8068-647ce432d221'
        }
    ],
    'offset': 0,
    'limit': 20,
    'total': 3,
    'first': True,
    'last': True
}

STARRED_HORIZONS_DATA_RESPONSE = {
    'top': '586a5e44-2a1c-402d-88bf-e82304e8fa2e',
    'center': HORIZON_ID,
    'bottom': '86831e2a-3a0b-4085-9e63-90500a8b47ac',
}

STARRED_TOPS_DATA_RESPONSE = {
    'top': 'c0332dab-9468-4b27-b1f6-3d4d7c875ecf',
    'center': '3e5f09a8-0a0a-4722-ab1a-c52c769fc72b',
    'bottom': '77b3db2b-83f0-4122-8068-647ce432d221',
}

MUDLOGS_DATA_RESPONSE = {
    'content': [
        {
            'name': MUDLOG_NAME,
            'uuid': 'fc927f99-aae2-4ac5-b16e-676c4d70d8b7'
        }
    ],
    'offset': 0,
    'limit': 10,
    'total': 1,
    'first': True,
    'last': True
}

MUDLOG_DATA_RESPONSE = {
    'logs': [
        {
            'uuid': '0a157968-8265-44c7-99a4-a18d17baa71a',
            'name': 'GRMA',
            'log_points': [
                {
                    'md': {
                        'val': 9465.499999999998
                    },
                    'data': {
                        'val': 16.917995
                    }
                }, {
                    'md': {
                        'val': 9465.999999999998
                    },
                    'data': {
                        'val': 17.194681
                    }
                }, {
                    'md': {
                        'val': 9466.499999999998
                    },
                    'data': {
                        'val': 18.103792
                    }
                }
            ]
        }, {
            'uuid': 'f2f36585-2036-4d90-a291-1da771c2b04d',
            'name': 'RHOB',
            'log_points': [
                {
                    'md': {
                        'val': 9465.499999999998
                    },
                    'data': {
                        'val': 2.241943
                    }
                }, {
                    'md': {
                        'val': 9465.999999999998
                    },
                    'data': {
                        'val': 2.269067
                    }
                }, {
                    'md': {
                        'val': 9466.499999999998
                    },
                    'data': {
                        'val': 2.287254
                    }
                }
            ]
        }
    ]
}


TRACES_DATA_RESPONSE = {
    'content': [
        {
            'uuid': '793b06f6-d494-45e0-9ed8-b5e8e916a2a8',
            'name': 'Bit depth'
        },
        {
            'uuid': '11b379f9-184b-465a-beb8-7307c7b4b1d9',
            'name': 'Hole Depth'
        },
        {
            'uuid': '491c2160-c65b-4ca0-afa9-7514fc6f7c56',
            'name': 'Block position'
        },
        {
            'uuid': '8752123d-d270-4eb6-b132-ba0f3e0d83b8',
            'name': 'Hookload'
        },
        {
            'uuid': 'c908bc68-0e9b-4368-a2be-97b48cbd5440',
            'name': 'Surface RPM'
        },
        {
            'uuid': 'a07b5bc6-a36f-4b8c-a3bb-4ce426eac7c0',
            'name': 'Surface Torque'
        },
        {
            'uuid': '2b2ad244-f208-4bb9-9b7c-6bbde9483635',
            'name': 'Standpipe Pressure'
        },
        {
            'uuid': '77c1bd4d-0fc1-470f-a24c-e28a5dd4c5fc',
            'name': 'Mud Weight IN'
        },
        {
            'uuid': '0a745541-0a23-45be-870d-9fdd8a1849c6',
            'name': 'Downhole WOB'
        },
        {
            'uuid': '9f7ed05c-66cd-441c-855d-a4aec51b33e2',
            'name': 'SPM1'
        },
        {
            'uuid': 'e0a2398e-21ad-4410-9cdd-e212c516061a',
            'name': 'SPM2'
        },
        {
            'uuid': '98bce1cd-fda0-41dd-8d04-e6020dd6e3e1',
            'name': 'SPM3'
        },
        {
            'uuid': '14b6654f-ba57-4bc5-8374-e219fc491e75',
            'name': 'Surface Torque Max'
        },
        {
            'uuid': '24624b80-b34c-4062-98c8-d42dea5fa125',
            'name': 'Block Velocity'
        },
        {
            'uuid': '6f83f7e7-40ac-448c-a2ce-e3c72d828735',
            'name': 'Gas'
        },
        {
            'uuid': '66d264d4-d935-49c8-bf17-c15c88d1f082',
            'name': 'Total Tank Volume'
        },
        {
            'uuid': 'b72b91cd-9482-47a7-8914-fe4c17b7aa02',
            'name': 'Trip Tank Volume'
        },
        {
            'uuid': 'accde91d-d6a3-4bc1-9986-f117a59f17e9',
            'name': 'Mud Weight Out'
        },
        {
            'uuid': '2c32a691-8787-49a6-83a1-c54d859a43ff',
            'name': 'Survey MD'
        },
        {
            'uuid': '16968239-944d-480e-ba34-195d4ba12927',
            'name': 'Inclination'
        },
        {
            'uuid': 'fa3a2cfb-c858-4c4f-8776-4130c475e594',
            'name': 'Cont Inclination'
        },
        {
            'uuid': '01da81cf-b8c7-4a3b-b561-3fdaf2f61dd4',
            'name': 'Azimuth'
        },
        {
            'uuid': 'ea9f7ad6-0880-4a5a-bddc-79e7c79d26bc',
            'name': 'Cont Azimuth'
        },
        {
            'uuid': '4022fb41-6279-4a5a-bec0-e8e0563119cc',
            'name': 'Gamma Ray'
        },
        {
            'uuid': '02f37da6-ced8-4b57-8a7d-0a583615a196',
            'name': 'Resistivity'
        },
        {
            'uuid': '865ba522-5800-40df-9271-5b8d8efece5c',
            'name': 'Density'
        },
        {
            'uuid': 'e58a09e4-9036-4bf4-b645-b1ef1984b867',
            'name': 'Caliper'
        },
        {
            'uuid': '83a18db4-e419-4671-8191-2d67149ac67e',
            'name': 'ECD'
        },
        {
            'uuid': '7572a7e5-8d99-444f-9be6-3de328354274',
            'name': 'StickSlip'
        },
        {
            'uuid': '061a437d-74de-41d0-b21d-c5858293d3e5',
            'name': 'Shock Levels'
        },
        {
            'uuid': '88d7ccaf-dafe-495f-934f-ad56e2e16c42',
            'name': 'On bottom hours'
        },
        {
            'uuid': 'd30498b6-6e8a-41b0-a6a4-9be5be5319e5',
            'name': 'Circulation hours'
        },
        {
            'uuid': '9fc059d1-85c6-429a-b03e-d92fb466b168',
            'name': 'User Defined 1'
        },
        {
            'uuid': '9e26b22f-b4ef-4284-80a9-f2716aac718c',
            'name': 'User Defined 2'
        },
        {
            'uuid': 'dbcf25d9-f808-4877-b3ca-90accf3d784b',
            'name': 'User Defined 3'
        },
        {
            'uuid': '908905a3-0269-4711-8007-1b7755471528',
            'name': 'User Defined 4'
        },
        {
            'uuid': '4be6e7f7-1eae-4f4e-ac6a-350327e59a39',
            'name': 'User Defined 5'
        },
        {
            'uuid': '54cd355d-8acf-4442-b62f-a50c78c189f8',
            'name': 'User Defined 6'
        },
        {
            'uuid': '6f304e26-802b-4118-a9ec-189b0d08d58f',
            'name': 'User Defined 7'
        },
        {
            'uuid': 'aaddd315-5693-4aac-ba31-4b5fd592923c',
            'name': 'User Defined 8'
        },
        {
            'uuid': '45369f92-7074-431f-8e9a-c47a0c64afff',
            'name': 'User Defined 9'
        },
        {
            'uuid': '435990bc-ead8-4268-8821-a8aea9e93944',
            'name': 'User Defined 10'
        },
        {
            'uuid': '074cb1e6-2bec-4b61-9e76-f48ebecf5ddd',
            'name': 'Mud Flow In'
        },
        {
            'uuid': 'ff172791-85e2-43cc-95f9-1fbb719abc6c',
            'name': 'SMP Total'
        },
        {
            'uuid': '227f118f-7845-49b2-9896-55dc5222519d',
            'name': 'WOB'
        },
        {
            'uuid': '9cb51894-17ff-4928-b8b4-4919f492c5c9',
            'name': 'In Slips'
        },
        {
            'uuid': '1b2beeff-a4a1-4e13-a25a-feabdc593da7',
            'name': 'GTF'
        },
        {
            'uuid': '0abaf4b2-6a97-4b0b-8609-f7ac37136a3b',
            'name': 'MTF'
        },
        {
            'uuid': '30146cef-6942-4247-bc75-521d76b85127',
            'name': 'ROP'
        },
        {
            'uuid': '7e01b567-d5f6-4912-bfe0-2ba189db6b2f',
            'name': 'Downhole TQ'
        },
        {
            'uuid': '9f0cb268-e4b7-425e-a191-596489da81d2',
            'name': 'Temperature In'
        },
        {
            'uuid': '009f1d02-b17a-41cf-9166-d02c37bcd834',
            'name': 'Temperature Out'
        },
        {
            'uuid': '36c53c74-8836-4a91-b95b-d5c3785c1f27',
            'name': 'Bit Depth Vertical'
        },
        {
            'uuid': '81a04429-a30f-4f13-ba33-138ab0981183',
            'name': 'Total RPM'
        },
        {
            'uuid': '7b021e39-f422-462c-87ac-d7e1105ac188',
            'name': 'WOB Max'
        },
        {
            'uuid': 'a8bfeb47-37f3-4bf8-b256-2f773307ee5b',
            'name': 'Mud Flow Out'
        },
        {
            'uuid': '82db3825-d6eb-4925-a73d-f5af1d1d6743',
            'name': 'Pump Stroke Count'
        },
        {
            'uuid': 'fe637ea0-4ae2-48d3-8c1d-2a4a84f8e06f',
            'name': 'Hole Depth Vertical'
        },
        {
            'uuid': '6eecd916-a7d2-47de-a72c-8afe5dd36373',
            'name': 'Flow'
        },
        {
            'uuid': '8eb6a4af-9453-44e7-ade3-aace18e0024a',
            'name': 'Casing Pressure'
        },
        {
            'uuid': 'c3b19920-8f01-47cb-acd9-0da8843e3ce7',
            'name': 'KPI: Slip to slip'
        },
        {
            'uuid': 'a0448fd5-d2d5-435f-9f57-dc23bafec82d',
            'name': 'Rig Activity'
        },
        {
            'uuid': '3fe5ea4a-e7d4-4679-aa10-0eba283a1e7d',
            'name': 'KPI: Trip In: Connection'
        },
        {
            'uuid': 'c0e7707d-24df-44c8-bd71-24aee1a5abe6',
            'name': 'KPI: Trip Out: Running'
        },
        {
            'uuid': 'a6f3ad7b-5363-427c-98ec-8bfee338cdd8',
            'name': 'KPI: Trip In: Running'
        },
        {
            'uuid': '6455f4ed-2ee7-4b1a-8535-d8df017e4b83',
            'name': 'KPI: Weight to Weight'
        },
        {
            'uuid': 'b35c6e45-45b1-46ea-8463-21237bf53353',
            'name': 'KPI: Trip Out: Connection'
        }
    ]
}


MAPPED_TRACES_DATA_RESPONSE = {
    'content': [
        {
            'uuid': '793b06f6-d494-45e0-9ed8-b5e8e916a2a8',
            'hash': 'bd9863171705c3a0bf3e334cdcfcb85d',
            'unit': ''
        },
        {
            'uuid': '11b379f9-184b-465a-beb8-7307c7b4b1d9',
            'hash': 'bdf8d4fbfc4a9238a0a77077fc8c7e89',
            'unit': 'm'
        },
        {
            'uuid': '491c2160-c65b-4ca0-afa9-7514fc6f7c56',
            'hash': '1afd16706047b52fae650a4c90c5e212',
            'unit': 'm'
        },
        {
            'uuid': '8752123d-d270-4eb6-b132-ba0f3e0d83b8',
            'hash': '68e05d9c28dc1440d606cd2ea421e822',
            'unit': ''
        },
        {
            'uuid': '8752123d-d270-4eb6-b132-ba0f3e0d83b8',
            'hash': 'f057732b91f6c397cfe98f4233f882fd',
            'unit': ''
        },
        {
            'uuid': 'c908bc68-0e9b-4368-a2be-97b48cbd5440',
            'hash': '62c94c73d18fa1dab139a63fadd6cda2',
            'unit': ''
        },
        {
            'uuid': '2b2ad244-f208-4bb9-9b7c-6bbde9483635',
            'hash': '9ffabe39ac818d9a5452710039cd0044',
            'unit': ''
        },
        {
            'uuid': '77c1bd4d-0fc1-470f-a24c-e28a5dd4c5fc',
            'hash': '10d2ef4b350e8321309310af6aaab08c',
            'unit': ''
        },
        {
            'uuid': '0a745541-0a23-45be-870d-9fdd8a1849c6',
            'hash': '8046e97e52a04a93f3401c5afcd06340',
            'unit': ''
        },
        {
            'uuid': '9f7ed05c-66cd-441c-855d-a4aec51b33e2',
            'hash': 'd0419aeed61716dda7a784e237fa0323',
            'unit': ''
        },
        {
            'uuid': '98bce1cd-fda0-41dd-8d04-e6020dd6e3e1',
            'hash': '7fd89649a07b54b842712965799b7d99',
            'unit': ''
        }
    ]
}

ENDLESS_INTERPRETATION_ASSEMBLED_SEGMENTS_DATA_RESPONSE = {
    'assembled_segments': {
        'horizons': {
            '586a5e44-2a1c-402d-88bf-e82304e8fa2e': {
                'tvd': {
                    'val': 11517.84276413585
                },
                'uuid': '586a5e44-2a1c-402d-88bf-e82304e8fa2e'
            },
            HORIZON_ID: {
                'tvd': {
                    'val': 11517.84276413585
                },
                'uuid': HORIZON_ID
            },
            '86831e2a-3a0b-4085-9e63-90500a8b47ac': {
                'tvd': {
                    'val': 11519.84276413585
                },
                'uuid': '86831e2a-3a0b-4085-9e63-90500a8b47ac'
            }
        },
        'segments': [
            {
                'boundary_type': 1,
                'end': {
                    'val': -6.5656962603957885
                },
                'horizon_shifts': {
                    '586a5e44-2a1c-402d-88bf-e82304e8fa2e': {
                        'end': {
                            'val': -6.5656962603957885
                        },
                        'start': {
                            'val': 0
                        },
                        'uuid': '586a5e44-2a1c-402d-88bf-e82304e8fa2e'
                    },
                    HORIZON_ID: {
                        'end': {
                            'val': -6.5656962603957885
                        },
                        'start': {
                            'val': 0
                        },
                        'uuid': HORIZON_ID
                    },
                    '86831e2a-3a0b-4085-9e63-90500a8b47ac': {
                        'end': {
                            'val': -6.5656962603957885
                        },
                        'start': {
                            'val': 0
                        },
                        'uuid': '86831e2a-3a0b-4085-9e63-90500a8b47ac'
                    }
                },
                'md': {
                    'val': 11284.942670449882
                },
                'start': {
                    'val': 0
                },
                'uuid': '17d78c2b-1544-42f9-9ffb-7aa07de5a90c'
            },
            {
                'boundary_type': 1,
                'end': {
                    'val': -18.912379033568882
                },
                'horizon_shifts': {
                    '586a5e44-2a1c-402d-88bf-e82304e8fa2e': {
                        'end': {
                            'val': -18.912379033568882
                        },
                        'start': {
                            'val': -6.565715689306932
                        },
                        'uuid': '586a5e44-2a1c-402d-88bf-e82304e8fa2e'
                    },
                    HORIZON_ID: {
                        'end': {
                            'val': -18.912379033568882
                        },
                        'start': {
                            'val': -6.565715689306932
                        },
                        'uuid': HORIZON_ID
                    },
                    '86831e2a-3a0b-4085-9e63-90500a8b47ac': {
                        'end': {
                            'val': -18.912379033568882
                        },
                        'start': {
                            'val': -6.565715689306932
                        },
                        'uuid': '86831e2a-3a0b-4085-9e63-90500a8b47ac'
                    }
                },
                'md': {
                    'val': 11511
                },
                'start': {
                    'val': -6.565715689306932
                },
                'uuid': 'b8e4b757-3612-4fe0-8fb3-82f3f7a3bcd4'
            },
            {
                'boundary_type': 1,
                'end': {
                    'val': -33.516118275710916
                },
                'horizon_shifts': {
                    '586a5e44-2a1c-402d-88bf-e82304e8fa2e': {
                        'end': {
                            'val': -33.516118275710916
                        },
                        'start': {
                            'val': -18.91237067033499
                        },
                        'uuid': '586a5e44-2a1c-402d-88bf-e82304e8fa2e'
                    },
                    HORIZON_ID: {
                        'end': {
                            'val': -33.516118275710916
                        },
                        'start': {
                            'val': -18.91237067033499
                        },
                        'uuid': HORIZON_ID
                    },
                    '86831e2a-3a0b-4085-9e63-90500a8b47ac': {
                        'end': {
                            'val': -33.516118275710916
                        },
                        'start': {
                            'val': -18.91237067033499
                        },
                        'uuid': '86831e2a-3a0b-4085-9e63-90500a8b47ac'
                    }
                },
                'md': {
                    'val': 11606
                },
                'start': {
                    'val': -18.91237067033499
                },
                'uuid': 'b7b5e05a-f6dd-4a7f-a84c-a44aca48e0ab'
            },
            {
                'boundary_type': 1,
                'end': {
                    'val': -62.39180676689853
                },
                'horizon_shifts': {
                    '586a5e44-2a1c-402d-88bf-e82304e8fa2e': {
                        'end': {
                            'val': -58.95023687660797
                        },
                        'start': {
                            'val': -33.516119686481034
                        },
                        'uuid': '586a5e44-2a1c-402d-88bf-e82304e8fa2e'
                    },
                    HORIZON_ID: {
                        'end': {
                            'val': -58.95023687660797
                        },
                        'start': {
                            'val': -33.516119686481034
                        },
                        'uuid': HORIZON_ID
                    },
                    '86831e2a-3a0b-4085-9e63-90500a8b47ac': {
                        'end': {
                            'val': -58.95023687660797
                        },
                        'start': {
                            'val': -33.516119686481034
                        },
                        'uuid': '86831e2a-3a0b-4085-9e63-90500a8b47ac'
                    }
                },
                'md': {
                    'val': 12186.000000000002
                },
                'start': {
                    'val': -33.5161196864814
                },
                'uuid': 'a482bf78-0224-42fa-808a-5f847ea93b7d'
            },
            {
                'boundary_type': 1,
                'end': {
                    'val': 0
                },
                'horizon_shifts': {
                    '586a5e44-2a1c-402d-88bf-e82304e8fa2e': {
                        'end': {
                            'val': -59.10163924450717
                        },
                        'start': {
                            'val': -58.95023687660797
                        },
                        'uuid': '586a5e44-2a1c-402d-88bf-e82304e8fa2e'
                    },
                    HORIZON_ID: {
                        'end': {
                            'val': -59.10163924450717
                        },
                        'start': {
                            'val': -58.95023687660797
                        },
                        'uuid': HORIZON_ID
                    },
                    '86831e2a-3a0b-4085-9e63-90500a8b47ac': {
                        'end': {
                            'val': -59.10163924450717
                        },
                        'start': {
                            'val': -58.95023687660797
                        },
                        'uuid': '86831e2a-3a0b-4085-9e63-90500a8b47ac'
                    }
                },
                'md': {
                    'val': 13056.70686045735
                },
                'start': {
                    'val': 0
                },
                'uuid': 'c7d83962-def5-4c76-90c0-2477886d45b5'
            },
            {
                'boundary_type': 0,
                'end': {
                    'val': -59.393141961814116
                },
                'horizon_shifts': {
                    '586a5e44-2a1c-402d-88bf-e82304e8fa2e': {
                        'end': {
                            'val': -56.70307051967029
                        },
                        'start': {
                            'val': -51.812185591572415
                        },
                        'uuid': '586a5e44-2a1c-402d-88bf-e82304e8fa2e'
                    },
                    HORIZON_ID: {
                        'end': {
                            'val': -56.70307051967029
                        },
                        'start': {
                            'val': -51.812185591572415
                        },
                        'uuid': HORIZON_ID
                    },
                    '86831e2a-3a0b-4085-9e63-90500a8b47ac': {
                        'end': {
                            'val': -56.70307051967029
                        },
                        'start': {
                            'val': -51.812185591572415
                        },
                        'uuid': '86831e2a-3a0b-4085-9e63-90500a8b47ac'
                    }
                },
                'md': {
                    'val': 13400.753488110999
                },
                'start': {
                    'val': -49.79941990825468
                },
                'uuid': 'd432f117-01bc-4b3b-9dcc-18f0276b74cd'
            },
            {
                'boundary_type': 1,
                'end': {
                    'val': 0
                },
                'horizon_shifts': {
                    '586a5e44-2a1c-402d-88bf-e82304e8fa2e': {
                        'end': {
                            'val': -60.56338690861413
                        },
                        'start': {
                            'val': -56.70307051967029
                        },
                        'uuid': '586a5e44-2a1c-402d-88bf-e82304e8fa2e'
                    },
                    HORIZON_ID: {
                        'end': {
                            'val': -60.56338690861413
                        },
                        'start': {
                            'val': -56.70307051967029
                        },
                        'uuid': HORIZON_ID
                    },
                    '86831e2a-3a0b-4085-9e63-90500a8b47ac': {
                        'end': {
                            'val': -60.56338690861413
                        },
                        'start': {
                            'val': -56.70307051967029
                        },
                        'uuid': '86831e2a-3a0b-4085-9e63-90500a8b47ac'
                    }
                },
                'md': {
                    'val': 13849.900000000045
                },
                'start': {
                    'val': 0
                },
                'uuid': '78f86c64-73e3-4daf-a861-fd7039a4d82a'
            },
            {
                'boundary_type': 0,
                'end': {
                    'val': -110.61396071446408
                },
                'horizon_shifts': {
                    '586a5e44-2a1c-402d-88bf-e82304e8fa2e': {
                        'end': {
                            'val': -103.06310344580925
                        },
                        'start': {
                            'val': -99.99209841093398
                        },
                        'uuid': '586a5e44-2a1c-402d-88bf-e82304e8fa2e'
                    },
                    HORIZON_ID: {
                        'end': {
                            'val': -103.06310344580925
                        },
                        'start': {
                            'val': -99.99209841093398
                        },
                        'uuid': HORIZON_ID
                    },
                    '86831e2a-3a0b-4085-9e63-90500a8b47ac': {
                        'end': {
                            'val': -103.06310344580925
                        },
                        'start': {
                            'val': -99.99209841093398
                        },
                        'uuid': '86831e2a-3a0b-4085-9e63-90500a8b47ac'
                    }
                },
                'md': {
                    'val': 13990.412233060615
                },
                'start': {
                    'val': -103.33964736322979
                },
                'uuid': 'aef9b467-8759-447a-bd83-4eebbd8ec403'
            },
            {
                'boundary_type': 1,
                'end': {
                    'val': 0
                },
                'horizon_shifts': {
                    '586a5e44-2a1c-402d-88bf-e82304e8fa2e': {
                        'end': {
                            'val': -110.61396071446325
                        },
                        'start': {
                            'val': -103.06310344580925
                        },
                        'uuid': '586a5e44-2a1c-402d-88bf-e82304e8fa2e'
                    },
                    HORIZON_ID: {
                        'end': {
                            'val': -110.61396071446325
                        },
                        'start': {
                            'val': -103.06310344580925
                        },
                        'uuid': HORIZON_ID
                    },
                    '86831e2a-3a0b-4085-9e63-90500a8b47ac': {
                        'end': {
                            'val': -110.61396071446325
                        },
                        'start': {
                            'val': -103.06310344580925
                        },
                        'uuid': '86831e2a-3a0b-4085-9e63-90500a8b47ac'
                    }
                },
                'md': {
                    'val': 14151.700000000004
                },
                'start': {
                    'val': 0
                },
                'uuid': '212c1744-1fce-414a-a569-15be33a2e863'
            },
            {
                'boundary_type': 1,
                'end': {
                    'val': -118.64063807436037
                },
                'horizon_shifts': {
                    '586a5e44-2a1c-402d-88bf-e82304e8fa2e': {
                        'end': {
                            'val': -118.64063807436037
                        },
                        'start': {
                            'val': -110.61403385396254
                        },
                        'uuid': '586a5e44-2a1c-402d-88bf-e82304e8fa2e'
                    },
                    HORIZON_ID: {
                        'end': {
                            'val': -118.64063807436037
                        },
                        'start': {
                            'val': -110.61403385396254
                        },
                        'uuid': HORIZON_ID
                    },
                    '86831e2a-3a0b-4085-9e63-90500a8b47ac': {
                        'end': {
                            'val': -118.64063807436037
                        },
                        'start': {
                            'val': -110.61403385396254
                        },
                        'uuid': '86831e2a-3a0b-4085-9e63-90500a8b47ac'
                    }
                },
                'md': {
                    'val': 14240.500000000002
                },
                'start': {
                    'val': -110.61403385396254
                },
                'uuid': '17cb4109-690e-4f45-a39a-a64532e25eb9'
            },
            {
                'boundary_type': 1,
                'end': {
                    'val': -141.0744362926588
                },
                'horizon_shifts': {
                    '586a5e44-2a1c-402d-88bf-e82304e8fa2e': {
                        'end': {
                            'val': -135.60868693330121
                        },
                        'start': {
                            'val': -118.6403753720424
                        },
                        'uuid': '586a5e44-2a1c-402d-88bf-e82304e8fa2e'
                    },
                    HORIZON_ID: {
                        'end': {
                            'val': -135.60868693330121
                        },
                        'start': {
                            'val': -118.6403753720424
                        },
                        'uuid': HORIZON_ID
                    },
                    '86831e2a-3a0b-4085-9e63-90500a8b47ac': {
                        'end': {
                            'val': -135.60868693330121
                        },
                        'start': {
                            'val': -118.6403753720424
                        },
                        'uuid': '86831e2a-3a0b-4085-9e63-90500a8b47ac'
                    }
                },
                'md': {
                    'val': 14466.000000000002
                },
                'start': {
                    'val': -118.6403753720431
                },
                'uuid': '200b0a28-ffc6-483e-99c7-2168ac7119b4'
            },
            {
                'boundary_type': 1,
                'end': {
                    'val': 0
                },
                'horizon_shifts': {
                    '586a5e44-2a1c-402d-88bf-e82304e8fa2e': {
                        'end': {
                            'val': -154.195111448762
                        },
                        'start': {
                            'val': -135.60868693330121
                        },
                        'uuid': '586a5e44-2a1c-402d-88bf-e82304e8fa2e'
                    },
                    HORIZON_ID: {
                        'end': {
                            'val': -154.195111448762
                        },
                        'start': {
                            'val': -135.60868693330121
                        },
                        'uuid': HORIZON_ID
                    },
                    '86831e2a-3a0b-4085-9e63-90500a8b47ac': {
                        'end': {
                            'val': -154.195111448762
                        },
                        'start': {
                            'val': -135.60868693330121
                        },
                        'uuid': '86831e2a-3a0b-4085-9e63-90500a8b47ac'
                    }
                },
                'md': {
                    'val': 14565.360000000022
                },
                'start': {
                    'val': 0
                },
                'uuid': 'faa9cc04-7841-4b0a-989d-da0d25be8a7d'
            },
            {
                'boundary_type': 0,
                'end': {
                    'val': -210.65888770893307
                },
                'horizon_shifts': {
                    '586a5e44-2a1c-402d-88bf-e82304e8fa2e': {
                        'end': {
                            'val': -211.69246022414336
                        },
                        'start': {
                            'val': -213.8141818373515
                        },
                        'uuid': '586a5e44-2a1c-402d-88bf-e82304e8fa2e'
                    },
                    HORIZON_ID: {
                        'end': {
                            'val': -211.69246022414336
                        },
                        'start': {
                            'val': -213.8141818373515
                        },
                        'uuid': HORIZON_ID
                    },
                    '86831e2a-3a0b-4085-9e63-90500a8b47ac': {
                        'end': {
                            'val': -211.69246022414336
                        },
                        'start': {
                            'val': -213.8141818373515
                        },
                        'uuid': '86831e2a-3a0b-4085-9e63-90500a8b47ac'
                    }
                },
                'md': {
                    'val': 14605.513625420313
                },
                'start': {
                    'val': -214.98207144576187
                },
                'uuid': 'c957b420-5c52-414e-902f-77005c3d12ea'
            },
            {
                'boundary_type': 1,
                'end': {
                    'val': 0
                },
                'horizon_shifts': {
                    '586a5e44-2a1c-402d-88bf-e82304e8fa2e': {
                        'end': {
                            'val': -215.79805967196262
                        },
                        'start': {
                            'val': -211.69246022414336
                        },
                        'uuid': '586a5e44-2a1c-402d-88bf-e82304e8fa2e'
                    },
                    HORIZON_ID: {
                        'end': {
                            'val': -215.79805967196262
                        },
                        'start': {
                            'val': -211.69246022414336
                        },
                        'uuid': HORIZON_ID
                    },
                    '86831e2a-3a0b-4085-9e63-90500a8b47ac': {
                        'end': {
                            'val': -215.79805967196262
                        },
                        'start': {
                            'val': -211.69246022414336
                        },
                        'uuid': '86831e2a-3a0b-4085-9e63-90500a8b47ac'
                    }
                },
                'md': {
                    'val': 14795.660000000045
                },
                'start': {
                    'val': 0
                },
                'uuid': '393d4368-b131-47a3-b9cc-019e548cf126'
            },
            {
                'boundary_type': 1,
                'end': {
                    'val': 0
                },
                'horizon_shifts': {
                    '586a5e44-2a1c-402d-88bf-e82304e8fa2e': {
                        'end': {
                            'val': -221.2564026611872
                        },
                        'start': {
                            'val': -215.79805967196262
                        },
                        'uuid': '586a5e44-2a1c-402d-88bf-e82304e8fa2e'
                    },
                    HORIZON_ID: {
                        'end': {
                            'val': -221.2564026611872
                        },
                        'start': {
                            'val': -215.79805967196262
                        },
                        'uuid': HORIZON_ID
                    },
                    '86831e2a-3a0b-4085-9e63-90500a8b47ac': {
                        'end': {
                            'val': -221.2564026611872
                        },
                        'start': {
                            'val': -215.79805967196262
                        },
                        'uuid': '86831e2a-3a0b-4085-9e63-90500a8b47ac'
                    }
                },
                'md': {
                    'val': 14976.140000000043
                },
                'start': {
                    'val': 0
                },
                'uuid': 'ff743f11-6101-42a8-8870-724189962750'
            },
            {
                'boundary_type': 1,
                'end': {
                    'val': 0
                },
                'horizon_shifts': {
                    '586a5e44-2a1c-402d-88bf-e82304e8fa2e': {
                        'end': {
                            'val': -229.80925200626916
                        },
                        'start': {
                            'val': -221.2564026611872
                        },
                        'uuid': '586a5e44-2a1c-402d-88bf-e82304e8fa2e'
                    },
                    HORIZON_ID: {
                        'end': {
                            'val': -229.80925200626916
                        },
                        'start': {
                            'val': -221.2564026611872
                        },
                        'uuid': HORIZON_ID
                    },
                    '86831e2a-3a0b-4085-9e63-90500a8b47ac': {
                        'end': {
                            'val': -229.80925200626916
                        },
                        'start': {
                            'val': -221.2564026611872
                        },
                        'uuid': '86831e2a-3a0b-4085-9e63-90500a8b47ac'
                    }
                },
                'md': {
                    'val': 15243.45000000002
                },
                'start': {
                    'val': 0
                },
                'uuid': 'f4178ffa-f443-4a0b-bee0-33925e0458ff'
            },
            {
                'boundary_type': 1,
                'end': {
                    'val': 0
                },
                'horizon_shifts': {
                    '586a5e44-2a1c-402d-88bf-e82304e8fa2e': {
                        'end': {
                            'val': -230.16893424342015
                        },
                        'start': {
                            'val': -229.80925200626916
                        },
                        'uuid': '586a5e44-2a1c-402d-88bf-e82304e8fa2e'
                    },
                    HORIZON_ID: {
                        'end': {
                            'val': -230.16893424342015
                        },
                        'start': {
                            'val': -229.80925200626916
                        },
                        'uuid': HORIZON_ID
                    },
                    '86831e2a-3a0b-4085-9e63-90500a8b47ac': {
                        'end': {
                            'val': -230.16893424342015
                        },
                        'start': {
                            'val': -229.80925200626916
                        },
                        'uuid': '86831e2a-3a0b-4085-9e63-90500a8b47ac'
                    }
                },
                'md': {
                    'val': 15501.950000000032
                },
                'start': {
                    'val': 0
                },
                'uuid': '01dda0be-8d5f-4d00-aba8-8bb9cc39a50a'
            },
            {
                'boundary_type': 1,
                'end': {
                    'val': -235.85437670843604
                },
                'horizon_shifts': {
                    '586a5e44-2a1c-402d-88bf-e82304e8fa2e': {
                        'end': {
                            'val': -235.85437670843567
                        },
                        'start': {
                            'val': -230.16893424342015
                        },
                        'uuid': '586a5e44-2a1c-402d-88bf-e82304e8fa2e'
                    },
                    HORIZON_ID: {
                        'end': {
                            'val': -235.85437670843567
                        },
                        'start': {
                            'val': -230.16893424342015
                        },
                        'uuid': HORIZON_ID
                    },
                    '86831e2a-3a0b-4085-9e63-90500a8b47ac': {
                        'end': {
                            'val': -235.85437670843567
                        },
                        'start': {
                            'val': -230.16893424342015
                        },
                        'uuid': '86831e2a-3a0b-4085-9e63-90500a8b47ac'
                    }
                },
                'md': {
                    'val': 15613.183002760585
                },
                'start': {
                    'val': -229.73977518065405
                },
                'uuid': 'a5e7554a-fd09-483b-92eb-ad029771996a'
            },
            {
                'boundary_type': 1,
                'end': {
                    'val': -254.64365643654796
                },
                'horizon_shifts': {
                    '586a5e44-2a1c-402d-88bf-e82304e8fa2e': {
                        'end': {
                            'val': -256.70260195632545
                        },
                        'start': {
                            'val': -235.8287914731427
                        },
                        'uuid': '586a5e44-2a1c-402d-88bf-e82304e8fa2e'
                    },
                    HORIZON_ID: {
                        'end': {
                            'val': -256.70260195632545
                        },
                        'start': {
                            'val': -235.8287914731427
                        },
                        'uuid': HORIZON_ID
                    },
                    '86831e2a-3a0b-4085-9e63-90500a8b47ac': {
                        'end': {
                            'val': -256.70260195632545
                        },
                        'start': {
                            'val': -235.8287914731427
                        },
                        'uuid': '86831e2a-3a0b-4085-9e63-90500a8b47ac'
                    }
                },
                'md': {
                    'val': 15967.5
                },
                'start': {
                    'val': -235.8287914731423
                },
                'uuid': '7bfea2b5-fbe4-42f7-ae83-41316f79e1d9',
                'x': -3225.8079920962136,
                'y': 3284.1141864352785,
            },
            {
                'boundary_type': 1,
                'end': {
                    'val': 0
                },
                'horizon_shifts': {
                    '586a5e44-2a1c-402d-88bf-e82304e8fa2e': {
                        'end': {
                            'val': -225.49538329945972
                        },
                        'start': {
                            'val': -256.70260195632545
                        },
                        'uuid': '586a5e44-2a1c-402d-88bf-e82304e8fa2e'
                    },
                    HORIZON_ID: {
                        'end': {
                            'val': -225.49538329945972
                        },
                        'start': {
                            'val': -256.70260195632545
                        },
                        'uuid': HORIZON_ID
                    },
                    '86831e2a-3a0b-4085-9e63-90500a8b47ac': {
                        'end': {
                            'val': -225.49538329945972
                        },
                        'start': {
                            'val': -256.70260195632545
                        },
                        'uuid': '86831e2a-3a0b-4085-9e63-90500a8b47ac'
                    }
                },
                'md': {
                    'val': 16951.101163762378,
                },
                'start': {
                    'val': 0
                },
                'uuid': '7bfea2b5-fbe4-42f7-ae83-41316f79e1d9',
                'x': -3953.9766627137483,
                'y': 3944.985613623949
            },
            {
                'boundary_type': 1,
                'end': {
                    'val': 0
                },
                'fake': {
                    'val': True
                },
                'horizon_shifts': {
                    '9e26d2ea-7291-4f29-8ebf-bcc47efbdcf2': {
                        'end': {
                            'val': -225.49538329945972
                        },
                        'start': {
                            'val': -225.49538329945972
                        },
                        'uuid': '9e26d2ea-7291-4f29-8ebf-bcc47efbdcf2'
                    },
                    HORIZON_ID: {
                        'end': {
                            'val': -225.49538329945972
                        },
                        'start': {
                            'val': -225.49538329945972
                        },
                        'uuid': HORIZON_ID
                    },
                    'f58e6db4-9525-4a16-b0bf-2f1971594e86': {
                        'end': {
                            'val': -225.49538329945972
                        },
                        'start': {
                            'val': -225.49538329945972
                        },
                        'uuid': 'f58e6db4-9525-4a16-b0bf-2f1971594e86'
                    }
                },
                'md': {
                    'val': 17411.271089701007,
                },
                'start': {
                    'val': 0
                },
                'uuid': '7bfea2b5-fbe4-42f7-ae83-41316f79e1d9',
                'x': -4295.88654055529,
                'y': 4252.842650417853,
            }
        ]
    }
}

TIME_TRACE_DATA_RESPONSE = {
    'content': [
        {
            'index': '2020-09-06T10:00:00.000Z',
            'value': '661.08'
        },
        {
            'index': '2020-09-06T10:00:01.000Z',
            'value': '661.16'
        },
        {
            'index': '2020-09-06T10:00:02.000Z',
            'value': '661.24'
        },
        {
            'index': '2020-09-06T10:00:03.000Z',
            'value': '661.32'
        },
        {
            'index': '2020-09-06T10:00:04.000Z',
            'value': '661.41'
        },
        {
            'index': '2020-09-06T10:00:05.000Z',
            'value': '661.49'
        },
        {
            'index': '2020-09-06T10:00:06.000Z',
            'value': '661.57'
        },
        {
            'index': '2020-09-06T10:00:07.000Z',
            'value': '661.66'
        },
        {
            'index': '2020-09-06T10:00:08.000Z',
            'value': '661.74'
        },
        {
            'index': '2020-09-06T10:00:09.000Z',
            'value': '661.82'
        },
        {
            'index': '2020-09-06T10:00:10.000Z',
            'value': '661.91'
        }
    ]
}
