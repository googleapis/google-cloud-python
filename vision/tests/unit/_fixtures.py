# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


FULL_TEXT_RESPONSE = {
    'responses': [{
        'fullTextAnnotation': {
            'pages': [{
                'height': 1872,
                'property': {
                    'detectedLanguages': [{
                        'languageCode': 'en'
                    }]
                },
                'blocks': [{
                    'blockType': 'TEXT',
                    'property': {
                        'detectedLanguages': [{
                            'languageCode': 'en'
                        }]
                    },
                    'boundingBox': {
                        'vertices': [{
                            'y': 8,
                            'x': 344
                        }, {
                            'y': 8,
                            'x': 434
                        }, {
                            'y': 22,
                            'x': 434
                        }, {
                            'y': 22,
                            'x': 344
                        }]
                    },
                    'paragraphs': [{
                        'property': {
                            'detectedLanguages': [{
                                'languageCode': 'en'
                            }]
                        },
                        'words': [{
                            'symbols': [{
                                'property': {
                                    'detectedLanguages': [{
                                        'languageCode': 'en'
                                    }]
                                },
                                'text': 'T',
                                'boundingBox': {
                                    'vertices': [{
                                        'y': 8,
                                        'x': 344
                                    }, {
                                        'y': 8,
                                        'x': 352
                                    }, {
                                        'y': 22,
                                        'x': 352
                                    }, {
                                        'y': 22,
                                        'x': 344
                                    }]
                                }
                            }],
                            'property': {
                                'detectedLanguages': [{
                                    'languageCode': 'en'
                                }]
                            },
                            'boundingBox': {
                                'vertices': [{
                                    'y': 8,
                                    'x': 377
                                }, {
                                    'y': 8,
                                    'x': 434
                                }, {
                                    'y': 22,
                                    'x': 434
                                }, {
                                    'y': 22,
                                    'x': 377
                                }]
                            }
                        }],
                        'boundingBox': {
                            'vertices': [{
                                'y': 8,
                                'x': 344
                            }, {
                                'y': 8,
                                'x': 434
                            }, {
                                'y': 22,
                                'x': 434
                            }, {
                                'y': 22,
                                'x': 344
                            }]
                        }
                    }]
                }],
                'width': 792
            }],
            'text': 'The Republic\nBy Plato'
        }
    }]
}

CROP_HINTS_RESPONSE = {
    "responses": [{
        "cropHintsAnnotation": {
            "cropHints": [{
                "importanceFraction": 1.22,
                "boundingPoly": {
                    "vertices": [{
                        "x": 77
                    }, {
                        "x": 1821
                    }, {
                        "x": 1821,
                        "y": 1306
                    }, {
                        "x": 77,
                        "y": 1306
                    }]
                },
                "confidence": 0.5
            }, {
                "importanceFraction": 1.2099999,
                "boundingPoly": {
                    "vertices": [{}, {
                        "x": 1959
                    }, {
                        "x": 1959,
                        "y": 1096
                    }, {
                        "y": 1096
                    }]
                },
                "confidence": 0.29999998
            }]
        }
    }]
}


IMAGE_PROPERTIES_RESPONSE = {
    'responses': [
        {
            'imagePropertiesAnnotation': {
                'dominantColors': {
                    'colors': [
                        {
                            'color': {
                                'red': 253,
                                'green': 203,
                                'blue': 65,
                                'alpha': 0.0
                            },
                            'score': 0.42258179,
                            'pixelFraction': 0.025376344
                        },
                        {
                            'color': {
                                'red': 216,
                                'green': 69,
                                'blue': 56
                            },
                            'score': 0.34945792,
                            'pixelFraction': 0.026093191
                        },
                        {
                            'color': {
                                'red': 79,
                                'green': 142,
                                'blue': 245
                            },
                            'score': 0.050921876,
                            'pixelFraction': 0.014193549
                        },
                        {
                            'color': {
                                'red': 249,
                                'green': 246,
                                'blue': 246
                            },
                            'score': 0.0059412993,
                            'pixelFraction': 0.86896056
                        },
                        {
                            'color': {
                                'red': 222,
                                'green': 119,
                                'blue': 51
                            },
                            'score': 0.0043299114,
                            'pixelFraction': 0.00021505376
                        },
                        {
                            'color': {
                                'red': 226,
                                'green': 138,
                                'blue': 130
                            },
                            'score': 0.0038594988,
                            'pixelFraction': 0.00086021505
                        },
                        {
                            'color': {
                                'red': 165,
                                'green': 194,
                                'blue': 243
                            },
                            'score': 0.0029492097,
                            'pixelFraction': 0.0015053763
                        },
                        {
                            'color': {
                                'red': 231,
                                'green': 169,
                                'blue': 164
                            },
                            'score': 0.0017002203,
                            'pixelFraction': 0.00043010752
                        },
                        {
                            'color': {
                                'red': 137,
                                'green': 98,
                                'blue': 142
                            },
                            'score': 0.0013974205,
                            'pixelFraction': 0.00071684585
                        },
                        {
                            'color': {
                                'red': 239,
                                'green': 179,
                                'blue': 56
                            },
                            'score': 0.050473157,
                            'pixelFraction': 0.0022222223
                        }
                    ]
                }
            }
        }
    ]
}

LABEL_DETECTION_RESPONSE = {
    'responses': [
        {
            'labelAnnotations': [
                {
                    'mid': '/m/0k4j',
                    'description': 'automobile',
                    'score': 0.9776855
                },
                {
                    'mid': '/m/07yv9',
                    'description': 'vehicle',
                    'score': 0.947987
                },
                {
                    'mid': '/m/07r04',
                    'description': 'truck',
                    'score': 0.88429511
                }
            ]
        }
    ]
}


LANDMARK_DETECTION_RESPONSE = {
    'responses': [
        {
            'landmarkAnnotations': [
                {
                    'mid': '/m/04gdr',
                    'description': 'Louvre',
                    'score': 0.67257267,
                    'boundingPoly': {
                        'vertices': [
                            {
                                'x': 1075,
                                'y': 49
                            },
                            {
                                'x': 1494,
                                'y': 49
                            },
                            {
                                'x': 1494,
                                'y': 307
                            },
                            {
                                'x': 1075,
                                'y': 307
                            }
                        ]
                    },
                    'locations': [
                        {
                            'latLng': {
                                'latitude': 48.861013,
                                'longitude': 2.335818
                            }
                        }
                    ]
                },
                {
                    'mid': '/m/094llg',
                    'description': 'Louvre Pyramid',
                    'score': 0.53734678,
                    'boundingPoly': {
                        'vertices': [
                            {
                                'x': 227,
                                'y': 274
                            },
                            {
                                'x': 1471,
                                'y': 274
                            },
                            {
                                'x': 1471,
                                'y': 624
                            },
                            {
                                'x': 227,
                                'y': 624
                            }
                        ]
                    },
                    'locations': [
                        {
                            'latLng': {
                                'latitude': 48.860749,
                                'longitude': 2.336312
                            }
                        }
                    ]
                }
            ]
        }
    ]
}

LOGO_DETECTION_RESPONSE = {
    'responses': [
        {
            'logoAnnotations': [
                {
                    'mid': '/m/05b5c',
                    'description': 'Brand1',
                    'score': 0.63192177,
                    'boundingPoly': {
                        'vertices': [
                            {
                                'x': 78,
                                'y': 162
                            },
                            {
                                'x': 282,
                                'y': 162
                            },
                            {
                                'x': 282,
                                'y': 211
                            },
                            {
                                'x': 78,
                                'y': 211
                            }
                        ]
                    }
                },
                {
                    'mid': '/m/0fpzzp',
                    'description': 'Brand2',
                    'score': 0.5492993,
                    'boundingPoly': {
                        'vertices': [
                            {
                                'x': 310,
                                'y': 209
                            },
                            {
                                'x': 477,
                                'y': 209
                            },
                            {
                                'x': 477,
                                'y': 282
                            },
                            {
                                'x': 310,
                                'y': 282
                            }
                        ]
                    }
                }
            ]
        }
    ]
}

FACE_DETECTION_RESPONSE = {
    'responses': [{
        'faceAnnotations': [{
            'headwearLikelihood': 'VERY_UNLIKELY',
            'panAngle': 6.027647,
            'underExposedLikelihood': 'VERY_UNLIKELY',
            'landmarkingConfidence': 0.54453093,
            'detectionConfidence': 0.9863683,
            'joyLikelihood': 'VERY_LIKELY',
            'landmarks': [{
                'position': {
                    'y': 482.69385,
                    'x': 1004.8003,
                    'z': 0.0016593217
                },
                'type': 'LEFT_EYE'
            }, {
                'position': {
                    'y': 470.90149,
                    'x': 1218.9751,
                    'z': 20.597967
                },
                'type': 'RIGHT_EYE'
            }, {
                'position': {
                    'y': 441.46521,
                    'x': 934.25629,
                    'z': -1.1400928
                },
                'type': 'LEFT_OF_LEFT_EYEBROW'
            }, {
                'position': {
                    'y': 449.2872,
                    'x': 1059.306,
                    'z': -47.195843
                },
                'type': 'RIGHT_OF_LEFT_EYEBROW'
            }, {
                'position': {
                    'y': 446.05408,
                    'x': 1163.678,
                    'z': -37.211197
                },
                'type': 'LEFT_OF_RIGHT_EYEBROW'
            }, {
                'position': {
                    'y': 424.18341,
                    'x': 1285.0209,
                    'z': 34.844131
                },
                'type': 'RIGHT_OF_RIGHT_EYEBROW'
            }, {
                'position': {
                    'y': 485.18387,
                    'x': 1113.4325,
                    'z': -32.579361
                },
                'type': 'MIDPOINT_BETWEEN_EYES'
            }, {
                'position': {
                    'y': 620.27032,
                    'x': 1122.5671,
                    'z': -51.019524
                },
                'type': 'NOSE_TIP'
            }, {
                'position': {
                    'y': 674.32526,
                    'x': 1117.0417,
                    'z': 17.330631
                },
                'type': 'UPPER_LIP'
            }, {
                'position': {
                    'y': 737.29736,
                    'x': 1115.7112,
                    'z': 54.076469
                },
                'type': 'LOWER_LIP'
            }, {
                'position': {
                    'y': 680.62927,
                    'x': 1017.0475,
                    'z': 72.948006
                },
                'type': 'MOUTH_LEFT'
            }, {
                'position': {
                    'y': 681.53552,
                    'x': 1191.5186,
                    'z': 87.198334
                },
                'type': 'MOUTH_RIGHT'
            }, {
                'position': {
                    'y': 702.3808,
                    'x': 1115.4193,
                    'z': 42.56889
                },
                'type': 'MOUTH_CENTER'
            }, {
                'position': {
                    'y': 606.68555,
                    'x': 1169.0006,
                    'z': 33.98217
                },
                'type': 'NOSE_BOTTOM_RIGHT'
            }, {
                'position': {
                    'y': 612.71509,
                    'x': 1053.9476,
                    'z': 23.409685
                },
                'type': 'NOSE_BOTTOM_LEFT'
            }, {
                'position': {
                    'y': 634.95532,
                    'x': 1116.6818,
                    'z': 3.386874
                },
                'type': 'NOSE_BOTTOM_CENTER'
            }, {
                'position': {
                    'y': 476.70197,
                    'x': 1009.2689,
                    'z': -16.84004
                },
                'type': 'LEFT_EYE_TOP_BOUNDARY'
            }, {
                'position': {
                    'y': 491.64874,
                    'x': 1049.3926,
                    'z': 7.0493474
                },
                'type': 'LEFT_EYE_RIGHT_CORNER'
            }, {
                'position': {
                    'y': 499.426,
                    'x': 1003.9925,
                    'z': 3.5417991
                },
                'type': 'LEFT_EYE_BOTTOM_BOUNDARY'
            }, {
                'position': {
                    'y': 482.37302,
                    'x': 964.48242,
                    'z': 14.96223
                },
                'type': 'LEFT_EYE_LEFT_CORNER'
            }, {
                'position': {
                    'y': 487.90195,
                    'x': 1005.3607,
                    'z': -4.7375555
                },
                'type': 'LEFT_EYE_PUPIL'
            }, {
                'position': {
                    'y': 468.33276,
                    'x': 1212.7329,
                    'z': 3.5585577
                },
                'type': 'RIGHT_EYE_TOP_BOUNDARY'
            }, {
                'position': {
                    'y': 470.92487,
                    'x': 1251.7043,
                    'z': 43.794273
                },
                'type': 'RIGHT_EYE_RIGHT_CORNER'
            }, {
                'position': {
                    'y': 486.98676,
                    'x': 1217.4629,
                    'z': 23.580008
                },
                'type': 'RIGHT_EYE_BOTTOM_BOUNDARY'
            }, {
                'position': {
                    'y': 482.41071,
                    'x': 1173.4624,
                    'z': 18.852427
                },
                'type': 'RIGHT_EYE_LEFT_CORNER'
            }, {
                'position': {
                    'y': 479.32739,
                    'x': 1213.9757,
                    'z': 16.041821
                },
                'type': 'RIGHT_EYE_PUPIL'
            }, {
                'position': {
                    'y': 424.38797,
                    'x': 1001.2206,
                    'z': -46.463905
                },
                'type': 'LEFT_EYEBROW_UPPER_MIDPOINT'
            }, {
                'position': {
                    'y': 415.33655,
                    'x': 1221.9457,
                    'z': -24.29454
                },
                'type': 'RIGHT_EYEBROW_UPPER_MIDPOINT'
            }, {
                'position': {
                    'y': 506.88251,
                    'x': 851.96124,
                    'z': 257.9054
                },
                'type': 'LEFT_EAR_TRAGION'
            }, {
                'position': {
                    'y': 487.9679,
                    'x': 1313.8328,
                    'z': 304.29816
                },
                'type': 'RIGHT_EAR_TRAGION'
            }, {
                'position': {
                    'y': 447.98254,
                    'x': 1114.1573,
                    'z': -50.620598
                },
                'type': 'FOREHEAD_GLABELLA'
            }, {
                'position': {
                    'y': 815.3302,
                    'x': 1113.27,
                    'z': 109.69422
                },
                'type': 'CHIN_GNATHION'
            }, {
                'position': {
                    'y': 656.20123,
                    'x': 884.34106,
                    'z': 223.19124
                },
                'type': 'CHIN_LEFT_GONION'
            }, {
                'position': {
                    'y': 639.291,
                    'x': 1301.2404,
                    'z': 265.00647
                },
                'type': 'CHIN_RIGHT_GONION'
            }],
            'sorrowLikelihood': 'VERY_UNLIKELY',
            'surpriseLikelihood': 'VERY_UNLIKELY',
            'tiltAngle': -18.412321,
            'angerLikelihood': 'VERY_UNLIKELY',
            'boundingPoly': {
                'vertices': [{
                    'y': 58,
                    'x': 748
                }, {
                    'y': 58,
                    'x': 1430
                }, {
                    'y': 851,
                    'x': 1430
                }, {
                    'y': 851,
                    'x': 748
                }]
            },
            'rollAngle': -0.43419784,
            'blurredLikelihood': 'VERY_UNLIKELY',
            'fdBoundingPoly': {
                'vertices': [{
                    'y': 310,
                    'x': 845
                }, {
                    'y': 310,
                    'x': 1379
                }, {
                    'y': 844,
                    'x': 1379
                }, {
                    'y': 844,
                    'x': 845
                }]
            }
        }, {
            'headwearLikelihood': 'VERY_UNLIKELY',
            'panAngle': -12.609346,
            'underExposedLikelihood': 'VERY_UNLIKELY',
            'landmarkingConfidence': 0.56890666,
            'detectionConfidence': 0.96333671,
            'joyLikelihood': 'VERY_LIKELY',
            'landmarks': [{
                'position': {
                    'y': 604.24847,
                    'x': 1655.8817,
                    'z': -0.0023633335
                },
                'type': 'LEFT_EYE'
            }, {
                'position': {
                    'y': 590.82428,
                    'x': 1797.3677,
                    'z': -30.984835
                },
                'type': 'RIGHT_EYE'
            }, {
                'position': {
                    'y': 574.40173,
                    'x': 1609.9617,
                    'z': 14.634346
                },
                'type': 'LEFT_OF_LEFT_EYEBROW'
            }, {
                'position': {
                    'y': 576.57483,
                    'x': 1682.0824,
                    'z': -41.733879
                },
                'type': 'RIGHT_OF_LEFT_EYEBROW'
            }, {
                'position': {
                    'y': 571.701,
                    'x': 1749.7633,
                    'z': -56.105503
                },
                'type': 'LEFT_OF_RIGHT_EYEBROW'
            }, {
                'position': {
                    'y': 556.67511,
                    'x': 1837.4333,
                    'z': -35.228374
                },
                'type': 'RIGHT_OF_RIGHT_EYEBROW'
            }, {
                'position': {
                    'y': 600.41345,
                    'x': 1720.1719,
                    'z': -44.4393
                },
                'type': 'MIDPOINT_BETWEEN_EYES'
            }, {
                'position': {
                    'y': 691.66907,
                    'x': 1720.0095,
                    'z': -63.878113
                },
                'type': 'NOSE_TIP'
            }, {
                'position': {
                    'y': 731.63239,
                    'x': 1733.2758,
                    'z': -20.964622
                },
                'type': 'UPPER_LIP'
            }, {
                'position': {
                    'y': 774.79138,
                    'x': 1740.1494,
                    'z': -0.038273316
                },
                'type': 'LOWER_LIP'
            }, {
                'position': {
                    'y': 739.80981,
                    'x': 1673.0156,
                    'z': 35.655769
                },
                'type': 'MOUTH_LEFT'
            }, {
                'position': {
                    'y': 728.8186,
                    'x': 1808.8899,
                    'z': 9.5512733
                },
                'type': 'MOUTH_RIGHT'
            }, {
                'position': {
                    'y': 753.71118,
                    'x': 1738.0863,
                    'z': -5.2711153
                },
                'type': 'MOUTH_CENTER'
            }, {
                'position': {
                    'y': 684.97522,
                    'x': 1770.2415,
                    'z': -18.243216
                },
                'type': 'NOSE_BOTTOM_RIGHT'
            }, {
                'position': {
                    'y': 695.69922,
                    'x': 1693.4669,
                    'z': -0.6566487
                },
                'type': 'NOSE_BOTTOM_LEFT'
            }, {
                'position': {
                    'y': 704.46063,
                    'x': 1729.86,
                    'z': -28.144602
                },
                'type': 'NOSE_BOTTOM_CENTER'
            }, {
                'position': {
                    'y': 597.93713,
                    'x': 1654.082,
                    'z': -11.508363
                },
                'type': 'LEFT_EYE_TOP_BOUNDARY'
            }, {
                'position': {
                    'y': 605.889,
                    'x': 1684.0094,
                    'z': -5.0379925
                },
                'type': 'LEFT_EYE_RIGHT_CORNER'
            }, {
                'position': {
                    'y': 614.40448,
                    'x': 1656.4753,
                    'z': 1.001922
                },
                'type': 'LEFT_EYE_BOTTOM_BOUNDARY'
            }, {
                'position': {
                    'y': 604.11292,
                    'x': 1632.2733,
                    'z': 18.163708
                },
                'type': 'LEFT_EYE_LEFT_CORNER'
            }, {
                'position': {
                    'y': 606.02026,
                    'x': 1654.1372,
                    'z': -3.3510325
                },
                'type': 'LEFT_EYE_PUPIL'
            }, {
                'position': {
                    'y': 588.00885,
                    'x': 1790.3329,
                    'z': -41.150127
                },
                'type': 'RIGHT_EYE_TOP_BOUNDARY'
            }, {
                'position': {
                    'y': 590.46307,
                    'x': 1824.5522,
                    'z': -23.20849
                },
                'type': 'RIGHT_EYE_RIGHT_CORNER'
            }, {
                'position': {
                    'y': 601.75946,
                    'x': 1797.9852,
                    'z': -29.095766
                },
                'type': 'RIGHT_EYE_BOTTOM_BOUNDARY'
            }, {
                'position': {
                    'y': 598.66449,
                    'x': 1768.7595,
                    'z': -23.117319
                },
                'type': 'RIGHT_EYE_LEFT_CORNER'
            }, {
                'position': {
                    'y': 595.84918,
                    'x': 1794.0195,
                    'z': -33.897068
                },
                'type': 'RIGHT_EYE_PUPIL'
            }, {
                'position': {
                    'y': 561.08679,
                    'x': 1641.9266,
                    'z': -26.653444
                },
                'type': 'LEFT_EYEBROW_UPPER_MIDPOINT'
            }, {
                'position': {
                    'y': 550.38129,
                    'x': 1789.6267,
                    'z': -58.874447
                },
                'type': 'RIGHT_EYEBROW_UPPER_MIDPOINT'
            }, {
                'position': {
                    'y': 632.54456,
                    'x': 1611.1659,
                    'z': 198.83691
                },
                'type': 'LEFT_EAR_TRAGION'
            }, {
                'position': {
                    'y': 610.1615,
                    'x': 1920.511,
                    'z': 131.28908
                },
                'type': 'RIGHT_EAR_TRAGION'
            }, {
                'position': {
                    'y': 574.28448,
                    'x': 1714.6324,
                    'z': -54.497036
                },
                'type': 'FOREHEAD_GLABELLA'
            }, {
                'position': {
                    'y': 830.93884,
                    'x': 1752.2703,
                    'z': 33.332912
                },
                'type': 'CHIN_GNATHION'
            }, {
                'position': {
                    'y': 732.33936,
                    'x': 1626.519,
                    'z': 162.6319
                },
                'type': 'CHIN_LEFT_GONION'
            }, {
                'position': {
                    'y': 712.21118,
                    'x': 1905.7007,
                    'z': 101.86344
                },
                'type': 'CHIN_RIGHT_GONION'
            }],
            'sorrowLikelihood': 'VERY_UNLIKELY',
            'surpriseLikelihood': 'VERY_UNLIKELY',
            'tiltAngle': -13.636207,
            'angerLikelihood': 'VERY_UNLIKELY',
            'boundingPoly': {
                'vertices': [{
                    'y': 319,
                    'x': 1524
                }, {
                    'y': 319,
                    'x': 1959
                }, {
                    'y': 859,
                    'x': 1959
                }, {
                    'y': 859,
                    'x': 1524
                }]
            },
            'rollAngle': -7.1766233,
            'blurredLikelihood': 'VERY_UNLIKELY',
            'fdBoundingPoly': {
                'vertices': [{
                    'y': 485,
                    'x': 1559
                }, {
                    'y': 485,
                    'x': 1920
                }, {
                    'y': 846,
                    'x': 1920
                }, {
                    'y': 846,
                    'x': 1559
                }]
            }
        }, {
            'headwearLikelihood': 'VERY_UNLIKELY',
            'panAngle': 8.7634687,
            'underExposedLikelihood': 'VERY_UNLIKELY',
            'landmarkingConfidence': 0.45491594,
            'detectionConfidence': 0.98870116,
            'joyLikelihood': 'VERY_LIKELY',
            'landmarks': [{
                'position': {
                    'y': 678.57886,
                    'x': 397.22269,
                    'z': 0.00052442803
                },
                'type': 'LEFT_EYE'
            }, {
                'position': {
                    'y': 671.90381,
                    'x': 515.38159,
                    'z': 17.843918
                },
                'type': 'RIGHT_EYE'
            }, {
                'position': {
                    'y': 657.13904,
                    'x': 361.41068,
                    'z': 6.1270714
                },
                'type': 'LEFT_OF_LEFT_EYEBROW'
            }, {
                'position': {
                    'y': 649.82916,
                    'x': 432.9726,
                    'z': -16.12303
                },
                'type': 'RIGHT_OF_LEFT_EYEBROW'
            }, {
                'position': {
                    'y': 646.04272,
                    'x': 487.78485,
                    'z': -7.638854
                },
                'type': 'LEFT_OF_RIGHT_EYEBROW'
            }, {
                'position': {
                    'y': 642.4032,
                    'x': 549.46954,
                    'z': 35.154259
                },
                'type': 'RIGHT_OF_RIGHT_EYEBROW'
            }, {
                'position': {
                    'y': 672.44031,
                    'x': 462.86993,
                    'z': -14.413016
                },
                'type': 'MIDPOINT_BETWEEN_EYES'
            }, {
                'position': {
                    'y': 736.5896,
                    'x': 474.0661,
                    'z': -50.206612
                },
                'type': 'NOSE_TIP'
            }, {
                'position': {
                    'y': 775.34973,
                    'x': 472.54224,
                    'z': -25.24843
                },
                'type': 'UPPER_LIP'
            }, {
                'position': {
                    'y': 820.41418,
                    'x': 474.41162,
                    'z': -18.226196
                },
                'type': 'LOWER_LIP'
            }, {
                'position': {
                    'y': 797.35547,
                    'x': 415.29095,
                    'z': 0.069621459
                },
                'type': 'MOUTH_LEFT'
            }, {
                'position': {
                    'y': 786.58917,
                    'x': 519.26709,
                    'z': 13.945135
                },
                'type': 'MOUTH_RIGHT'
            }, {
                'position': {
                    'y': 798.462,
                    'x': 472.48071,
                    'z': -17.317541
                },
                'type': 'MOUTH_CENTER'
            }, {
                'position': {
                    'y': 742.13464,
                    'x': 498.90826,
                    'z': -1.8338414
                },
                'type': 'NOSE_BOTTOM_RIGHT'
            }, {
                'position': {
                    'y': 747.218,
                    'x': 438.95078,
                    'z': -11.851667
                },
                'type': 'NOSE_BOTTOM_LEFT'
            }, {
                'position': {
                    'y': 754.20105,
                    'x': 472.47375,
                    'z': -24.760784
                },
                'type': 'NOSE_BOTTOM_CENTER'
            }, {
                'position': {
                    'y': 672.1994,
                    'x': 403.39957,
                    'z': -6.9005938
                },
                'type': 'LEFT_EYE_TOP_BOUNDARY'
            }, {
                'position': {
                    'y': 679.914,
                    'x': 425.36029,
                    'z': 4.3264537
                },
                'type': 'LEFT_EYE_RIGHT_CORNER'
            }, {
                'position': {
                    'y': 687.11792,
                    'x': 401.66464,
                    'z': -0.79697126
                },
                'type': 'LEFT_EYE_BOTTOM_BOUNDARY'
            }, {
                'position': {
                    'y': 682.9585,
                    'x': 378.93005,
                    'z': 7.3909378
                },
                'type': 'LEFT_EYE_LEFT_CORNER'
            }, {
                'position': {
                    'y': 680.40326,
                    'x': 401.7229,
                    'z': -2.7444897
                },
                'type': 'LEFT_EYE_PUPIL'
            }, {
                'position': {
                    'y': 663.39496,
                    'x': 516.03217,
                    'z': 10.454485
                },
                'type': 'RIGHT_EYE_TOP_BOUNDARY'
            }, {
                'position': {
                    'y': 670.74463,
                    'x': 536.45978,
                    'z': 31.652559
                },
                'type': 'RIGHT_EYE_RIGHT_CORNER'
            }, {
                'position': {
                    'y': 679.21289,
                    'x': 517.50879,
                    'z': 16.653259
                },
                'type': 'RIGHT_EYE_BOTTOM_BOUNDARY'
            }, {
                'position': {
                    'y': 676.06976,
                    'x': 495.27335,
                    'z': 14.956539
                },
                'type': 'RIGHT_EYE_LEFT_CORNER'
            }, {
                'position': {
                    'y': 671.41052,
                    'x': 517.3429,
                    'z': 15.007857
                },
                'type': 'RIGHT_EYE_PUPIL'
            }, {
                'position': {
                    'y': 639.23633,
                    'x': 396.8494,
                    'z': -12.132922
                },
                'type': 'LEFT_EYEBROW_UPPER_MIDPOINT'
            }, {
                'position': {
                    'y': 629.66724,
                    'x': 518.96332,
                    'z': 6.7055798
                },
                'type': 'RIGHT_EYEBROW_UPPER_MIDPOINT'
            }, {
                'position': {
                    'y': 750.20837,
                    'x': 313.60855,
                    'z': 127.8474
                },
                'type': 'LEFT_EAR_TRAGION'
            }, {
                'position': {
                    'y': 728.68243,
                    'x': 570.95,
                    'z': 166.43564
                },
                'type': 'RIGHT_EAR_TRAGION'
            }, {
                'position': {
                    'y': 646.05042,
                    'x': 460.94397,
                    'z': -16.196959
                },
                'type': 'FOREHEAD_GLABELLA'
            }, {
                'position': {
                    'y': 869.36255,
                    'x': 476.69009,
                    'z': -4.4716644
                },
                'type': 'CHIN_GNATHION'
            }, {
                'position': {
                    'y': 818.48083,
                    'x': 340.65454,
                    'z': 80.163544
                },
                'type': 'CHIN_LEFT_GONION'
            }, {
                'position': {
                    'y': 800.17029,
                    'x': 571.60297,
                    'z': 115.88489
                },
                'type': 'CHIN_RIGHT_GONION'
            }],
            'sorrowLikelihood': 'VERY_UNLIKELY',
            'surpriseLikelihood': 'VERY_UNLIKELY',
            'tiltAngle': 2.1818738,
            'angerLikelihood': 'VERY_UNLIKELY',
            'boundingPoly': {
                'vertices': [{
                    'y': 481,
                    'x': 257
                }, {
                    'y': 481,
                    'x': 636
                }, {
                    'y': 922,
                    'x': 636
                }, {
                    'y': 922,
                    'x': 257
                }]
            },
            'rollAngle': -4.8415074,
            'blurredLikelihood': 'VERY_UNLIKELY',
            'fdBoundingPoly': {
                'vertices': [{
                    'y': 597,
                    'x': 315
                }, {
                    'y': 597,
                    'x': 593
                }, {
                    'y': 874,
                    'x': 593
                }, {
                    'y': 874,
                    'x': 315
                }]
            }
        }, {
            'headwearLikelihood': 'VERY_UNLIKELY',
            'panAngle': 13.486016,
            'underExposedLikelihood': 'VERY_UNLIKELY',
            'landmarkingConfidence': 0.22890881,
            'detectionConfidence': 0.91653949,
            'joyLikelihood': 'LIKELY',
            'landmarks': [{
                'position': {
                    'y': 549.30334,
                    'x': 9.7225485,
                    'z': 0.0014079071
                },
                'type': 'LEFT_EYE'
            }, {
                'position': {
                    'y': 539.7489,
                    'x': 128.87411,
                    'z': 28.692257
                },
                'type': 'RIGHT_EYE'
            }, {
                'position': {
                    'y': 523.62103,
                    'x': -35.406662,
                    'z': -0.67885911
                },
                'type': 'LEFT_OF_LEFT_EYEBROW'
            }, {
                'position': {
                    'y': 519.99487,
                    'x': 42.973644,
                    'z': -18.105515
                },
                'type': 'RIGHT_OF_LEFT_EYEBROW'
            }, {
                'position': {
                    'y': 514.23407,
                    'x': 103.02193,
                    'z': -4.1667485
                },
                'type': 'LEFT_OF_RIGHT_EYEBROW'
            }, {
                'position': {
                    'y': 505.69614,
                    'x': 165.63609,
                    'z': 47.583176
                },
                'type': 'RIGHT_OF_RIGHT_EYEBROW'
            }, {
                'position': {
                    'y': 540.9787,
                    'x': 76.066139,
                    'z': -11.183347
                },
                'type': 'MIDPOINT_BETWEEN_EYES'
            }, {
                'position': {
                    'y': 615.48669,
                    'x': 89.695564,
                    'z': -41.252846
                },
                'type': 'NOSE_TIP'
            }, {
                'position': {
                    'y': 658.39246,
                    'x': 85.935593,
                    'z': -9.70177
                },
                'type': 'UPPER_LIP'
            }, {
                'position': {
                    'y': 703.04309,
                    'x': 87.266853,
                    'z': 2.6370313
                },
                'type': 'LOWER_LIP'
            }, {
                'position': {
                    'y': 678.54712,
                    'x': 31.584759,
                    'z': 12.874522
                },
                'type': 'MOUTH_LEFT'
            }, {
                'position': {
                    'y': 670.44092,
                    'x': 126.54009,
                    'z': 35.510525
                },
                'type': 'MOUTH_RIGHT'
            }, {
                'position': {
                    'y': 677.92883,
                    'x': 85.152267,
                    'z': 0.89151889
                },
                'type': 'MOUTH_CENTER'
            }, {
                'position': {
                    'y': 618.41052,
                    'x': 112.767,
                    'z': 14.021111
                },
                'type': 'NOSE_BOTTOM_RIGHT'
            }, {
                'position': {
                    'y': 624.28644,
                    'x': 45.776546,
                    'z': -2.0218573
                },
                'type': 'NOSE_BOTTOM_LEFT'
            }, {
                'position': {
                    'y': 632.9657,
                    'x': 84.253586,
                    'z': -12.025499
                },
                'type': 'NOSE_BOTTOM_CENTER'
            }, {
                'position': {
                    'y': 541.79987,
                    'x': 11.081995,
                    'z': -8.7047234
                },
                'type': 'LEFT_EYE_TOP_BOUNDARY'
            }, {
                'position': {
                    'y': 549.57306,
                    'x': 35.396069,
                    'z': 6.4817863
                },
                'type': 'LEFT_EYE_RIGHT_CORNER'
            }, {
                'position': {
                    'y': 557.55121,
                    'x': 10.446005,
                    'z': -0.37798333
                },
                'type': 'LEFT_EYE_BOTTOM_BOUNDARY'
            }, {
                'position': {
                    'y': 551.75134,
                    'x': -16.862394,
                    'z': 5.4017038
                },
                'type': 'LEFT_EYE_LEFT_CORNER'
            }, {
                'position': {
                    'y': 550.14355,
                    'x': 8.5758247,
                    'z': -3.3803346
                },
                'type': 'LEFT_EYE_PUPIL'
            }, {
                'position': {
                    'y': 531.02594,
                    'x': 131.48265,
                    'z': 20.201307
                },
                'type': 'RIGHT_EYE_TOP_BOUNDARY'
            }, {
                'position': {
                    'y': 536.71674,
                    'x': 151.31306,
                    'z': 45.753532
                },
                'type': 'RIGHT_EYE_RIGHT_CORNER'
            }, {
                'position': {
                    'y': 547.00037,
                    'x': 130.27722,
                    'z': 28.447813
                },
                'type': 'RIGHT_EYE_BOTTOM_BOUNDARY'
            }, {
                'position': {
                    'y': 542.38531,
                    'x': 106.59242,
                    'z': 23.77187
                },
                'type': 'RIGHT_EYE_LEFT_CORNER'
            }, {
                'position': {
                    'y': 539.12781,
                    'x': 132.16141,
                    'z': 26.180428
                },
                'type': 'RIGHT_EYE_PUPIL'
            }, {
                'position': {
                    'y': 506.64093,
                    'x': 4.8589344,
                    'z': -18.679537
                },
                'type': 'LEFT_EYEBROW_UPPER_MIDPOINT'
            }, {
                'position': {
                    'y': 494.94244,
                    'x': 135.53185,
                    'z': 12.703153
                },
                'type': 'RIGHT_EYEBROW_UPPER_MIDPOINT'
            }, {
                'position': {
                    'y': 609.03503,
                    'x': -98.89212,
                    'z': 134.96341
                },
                'type': 'LEFT_EAR_TRAGION'
            }, {
                'position': {
                    'y': 584.60681,
                    'x': 174.55208,
                    'z': 200.56409
                },
                'type': 'RIGHT_EAR_TRAGION'
            }, {
                'position': {
                    'y': 514.88513,
                    'x': 74.575394,
                    'z': -15.91002
                },
                'type': 'FOREHEAD_GLABELLA'
            }, {
                'position': {
                    'y': 755.372,
                    'x': 86.603539,
                    'z': 23.596317
                },
                'type': 'CHIN_GNATHION'
            }, {
                'position': {
                    'y': 689.8385,
                    'x': -67.949554,
                    'z': 94.833694
                },
                'type': 'CHIN_LEFT_GONION'
            }, {
                'position': {
                    'y': 667.89325,
                    'x': 179.19363,
                    'z': 154.18192
                },
                'type': 'CHIN_RIGHT_GONION'
            }],
            'sorrowLikelihood': 'VERY_UNLIKELY',
            'surpriseLikelihood': 'VERY_UNLIKELY',
            'tiltAngle': -4.1819687,
            'angerLikelihood': 'VERY_UNLIKELY',
            'boundingPoly': {
                'vertices': [{
                    'y': 322
                }, {
                    'y': 322,
                    'x': 252
                }, {
                    'y': 800,
                    'x': 252
                }, {
                    'y': 800
                }]
            },
            'rollAngle': -4.1248608,
            'blurredLikelihood': 'LIKELY',
            'fdBoundingPoly': {
                'vertices': [{
                    'y': 450
                }, {
                    'y': 450,
                    'x': 235
                }, {
                    'y': 745,
                    'x': 235
                }, {
                    'y': 745
                }]
            }
        }, {
            'headwearLikelihood': 'VERY_UNLIKELY',
            'panAngle': 4.0344138,
            'underExposedLikelihood': 'VERY_UNLIKELY',
            'landmarkingConfidence': 0.16798845,
            'detectionConfidence': 0.7605139,
            'joyLikelihood': 'VERY_LIKELY',
            'landmarks': [{
                'position': {
                    'y': 637.85211,
                    'x': 676.09375,
                    'z': 4.3306696e-05
                },
                'type': 'LEFT_EYE'
            }, {
                'position': {
                    'y': 637.43292,
                    'x': 767.7132,
                    'z': 6.4413033
                },
                'type': 'RIGHT_EYE'
            }, {
                'position': {
                    'y': 614.27075,
                    'x': 642.07782,
                    'z': 3.731837
                },
                'type': 'LEFT_OF_LEFT_EYEBROW'
            }, {
                'position': {
                    'y': 617.27216,
                    'x': 700.90112,
                    'z': -19.774208
                },
                'type': 'RIGHT_OF_LEFT_EYEBROW'
            }, {
                'position': {
                    'y': 617.15649,
                    'x': 747.60974,
                    'z': -16.511871
                },
                'type': 'LEFT_OF_RIGHT_EYEBROW'
            }, {
                'position': {
                    'y': 614.018,
                    'x': 802.60638,
                    'z': 14.954031
                },
                'type': 'RIGHT_OF_RIGHT_EYEBROW'
            }, {
                'position': {
                    'y': 638.11755,
                    'x': 724.42511,
                    'z': -16.930967
                },
                'type': 'MIDPOINT_BETWEEN_EYES'
            }, {
                'position': {
                    'y': 696.08392,
                    'x': 725.82532,
                    'z': -38.252609
                },
                'type': 'NOSE_TIP'
            }, {
                'position': {
                    'y': 727.826,
                    'x': 724.0116,
                    'z': -11.615328
                },
                'type': 'UPPER_LIP'
            }, {
                'position': {
                    'y': 760.22595,
                    'x': 723.30157,
                    'z': -0.454926
                },
                'type': 'LOWER_LIP'
            }, {
                'position': {
                    'y': 738.67548,
                    'x': 684.35724,
                    'z': 13.192401
                },
                'type': 'MOUTH_LEFT'
            }, {
                'position': {
                    'y': 738.53015,
                    'x': 759.91022,
                    'z': 18.485643
                },
                'type': 'MOUTH_RIGHT'
            }, {
                'position': {
                    'y': 742.42737,
                    'x': 723.45239,
                    'z': -2.4991846
                },
                'type': 'MOUTH_CENTER'
            }, {
                'position': {
                    'y': 698.4281,
                    'x': 749.50385,
                    'z': 1.1831931
                },
                'type': 'NOSE_BOTTOM_RIGHT'
            }, {
                'position': {
                    'y': 698.48151,
                    'x': 696.923,
                    'z': -2.4809308
                },
                'type': 'NOSE_BOTTOM_LEFT'
            }, {
                'position': {
                    'y': 708.10651,
                    'x': 724.18506,
                    'z': -14.418536
                },
                'type': 'NOSE_BOTTOM_CENTER'
            }, {
                'position': {
                    'y': 632.12128,
                    'x': 675.22388,
                    'z': -7.2390652
                },
                'type': 'LEFT_EYE_TOP_BOUNDARY'
            }, {
                'position': {
                    'y': 638.59021,
                    'x': 694.03516,
                    'z': 1.7715795
                },
                'type': 'LEFT_EYE_RIGHT_CORNER'
            }, {
                'position': {
                    'y': 644.33356,
                    'x': 674.92206,
                    'z': -0.037067439
                },
                'type': 'LEFT_EYE_BOTTOM_BOUNDARY'
            }, {
                'position': {
                    'y': 637.16479,
                    'x': 655.035,
                    'z': 7.4372306
                },
                'type': 'LEFT_EYE_LEFT_CORNER'
            }, {
                'position': {
                    'y': 638.18683,
                    'x': 673.39447,
                    'z': -2.4558623
                },
                'type': 'LEFT_EYE_PUPIL'
            }, {
                'position': {
                    'y': 631.96063,
                    'x': 771.31744,
                    'z': -0.51439536
                },
                'type': 'RIGHT_EYE_TOP_BOUNDARY'
            }, {
                'position': {
                    'y': 636.94287,
                    'x': 789.29443,
                    'z': 16.814001
                },
                'type': 'RIGHT_EYE_RIGHT_CORNER'
            }, {
                'position': {
                    'y': 644.21619,
                    'x': 770.13458,
                    'z': 6.6525826
                },
                'type': 'RIGHT_EYE_BOTTOM_BOUNDARY'
            }, {
                'position': {
                    'y': 638.75732,
                    'x': 752.51831,
                    'z': 5.8927159
                },
                'type': 'RIGHT_EYE_LEFT_CORNER'
            }, {
                'position': {
                    'y': 638.06738,
                    'x': 772.04718,
                    'z': 4.350193
                },
                'type': 'RIGHT_EYE_PUPIL'
            }, {
                'position': {
                    'y': 604.87769,
                    'x': 671.68707,
                    'z': -15.778968
                },
                'type': 'LEFT_EYEBROW_UPPER_MIDPOINT'
            }, {
                'position': {
                    'y': 604.71191,
                    'x': 775.98663,
                    'z': -8.4828024
                },
                'type': 'RIGHT_EYEBROW_UPPER_MIDPOINT'
            }, {
                'position': {
                    'y': 670.40063,
                    'x': 605.07721,
                    'z': 119.27386
                },
                'type': 'LEFT_EAR_TRAGION'
            }, {
                'position': {
                    'y': 669.99823,
                    'x': 823.42841,
                    'z': 134.54482
                },
                'type': 'RIGHT_EAR_TRAGION'
            }, {
                'position': {
                    'y': 616.47058,
                    'x': 724.54547,
                    'z': -21.861612
                },
                'type': 'FOREHEAD_GLABELLA'
            }, {
                'position': {
                    'y': 801.31934,
                    'x': 722.071,
                    'z': 18.37034
                },
                'type': 'CHIN_GNATHION'
            }, {
                'position': {
                    'y': 736.57159,
                    'x': 617.91388,
                    'z': 88.713562
                },
                'type': 'CHIN_LEFT_GONION'
            }, {
                'position': {
                    'y': 736.21118,
                    'x': 815.234,
                    'z': 102.52047
                },
                'type': 'CHIN_RIGHT_GONION'
            }],
            'sorrowLikelihood': 'VERY_UNLIKELY',
            'surpriseLikelihood': 'VERY_UNLIKELY',
            'tiltAngle': -7.0173812,
            'angerLikelihood': 'VERY_UNLIKELY',
            'boundingPoly': {
                'vertices': [{
                    'y': 459,
                    'x': 557
                }, {
                    'y': 459,
                    'x': 875
                }, {
                    'y': 829,
                    'x': 875
                }, {
                    'y': 829,
                    'x': 557
                }]
            },
            'rollAngle': 0.38634345,
            'blurredLikelihood': 'LIKELY',
            'fdBoundingPoly': {
                'vertices': [{
                    'y': 570,
                    'x': 612
                }, {
                    'y': 570,
                    'x': 837
                }, {
                    'y': 795,
                    'x': 837
                }, {
                    'y': 795,
                    'x': 612
                }]
            }
        }]
    }]
}


MULTIPLE_RESPONSE = {
    'responses': [
        {
            'labelAnnotations': [
                {
                    'mid': '/m/0k4j',
                    'description': 'automobile',
                    'score': 0.9776855
                },
                {
                    'mid': '/m/07yv9',
                    'description': 'vehicle',
                    'score': 0.947987
                },
                {
                    'mid': '/m/07r04',
                    'description': 'truck',
                    'score': 0.88429511
                },
            ],
        },
        {
            'safeSearchAnnotation': {
                'adult': 'VERY_UNLIKELY',
                'spoof': 'UNLIKELY',
                'medical': 'POSSIBLE',
                'violence': 'VERY_UNLIKELY'
            },
        },
    ],
}


SAFE_SEARCH_DETECTION_RESPONSE = {
    'responses': [
        {
            'safeSearchAnnotation': {
                'adult': 'VERY_UNLIKELY',
                'spoof': 'UNLIKELY',
                'medical': 'POSSIBLE',
                'violence': 'VERY_UNLIKELY'
            }
        }
    ]
}


TEXT_DETECTION_RESPONSE = {
    'responses': [
        {
            'textAnnotations': [
                {
                    'locale': 'en',
                    'description': 'Google CloudPlatform\n',
                    'boundingPoly': {
                        'vertices': [
                            {
                                'x': 129,
                                'y': 694
                            },
                            {
                                'x': 1375,
                                'y': 694
                            },
                            {
                                'x': 1375,
                                'y': 835
                            },
                            {
                                'x': 129,
                                'y': 835
                            }
                        ]
                    }
                },
                {
                    'description': 'Google',
                    'boundingPoly': {
                        'vertices': [
                            {
                                'x': 129,
                                'y': 694
                            },
                            {
                                'x': 535,
                                'y': 694
                            },
                            {
                                'x': 535,
                                'y': 835
                            },
                            {
                                'x': 129,
                                'y': 835
                            }
                        ]
                    }
                },
                {
                    'description': 'CloudPlatform',
                    'boundingPoly': {
                        'vertices': [
                            {
                                'x': 567,
                                'y': 694
                            },
                            {
                                'x': 1375,
                                'y': 694
                            },
                            {
                                'x': 1375,
                                'y': 835
                            },
                            {
                                'x': 567,
                                'y': 835
                            }
                        ]
                    }
                }
            ]
        }
    ]
}


WEB_DETECTION_RESPONSE = {
    'responses': [
        {
            'webDetection': {
                'partialMatchingImages': [{
                    'score': 0.9216,
                    'url': 'https://cloud.google.com/vision'
                }, {
                    'score': 0.55520177,
                    'url': 'https://cloud.google.com/vision'
                }],
                'fullMatchingImages': [{
                    'score': 0.09591467,
                    'url': 'https://cloud.google.com/vision'
                }, {
                    'score': 0.09591467,
                    'url': 'https://cloud.google.com/vision'
                }],
                'webEntities': [{
                    'entityId': '/m/019dvv',
                    'score': 1470.4435,
                    'description': 'Mount Rushmore National Memorial'
                }, {
                    'entityId': '/m/05_5t0l',
                    'score': 0.9468027,
                    'description': 'Landmark'
                }],
                'pagesWithMatchingImages': [{
                    'score': 2.9996617,
                    'url': 'https://cloud.google.com/vision'
                }, {
                    'score': 1.1980441,
                    'url': 'https://cloud.google.com/vision'
                }]
            }
        }
    ]
}
