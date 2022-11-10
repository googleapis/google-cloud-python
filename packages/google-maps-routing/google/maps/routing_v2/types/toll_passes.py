# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from typing import MutableMapping, MutableSequence

import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.maps.routing.v2",
    manifest={
        "TollPass",
    },
)


class TollPass(proto.Enum):
    r"""List of toll passes around the world that we support."""
    TOLL_PASS_UNSPECIFIED = 0
    AU_ETOLL_TAG = 82
    AU_EWAY_TAG = 83
    AU_LINKT = 2
    AR_TELEPASE = 3
    BR_AUTO_EXPRESO = 81
    BR_CONECTCAR = 7
    BR_MOVE_MAIS = 8
    BR_PASSA_RAPIDO = 88
    BR_SEM_PARAR = 9
    BR_TAGGY = 10
    BR_VELOE = 11
    CA_US_AKWASASNE_SEAWAY_CORPORATE_CARD = 84
    CA_US_AKWASASNE_SEAWAY_TRANSIT_CARD = 85
    CA_US_BLUE_WATER_EDGE_PASS = 18
    CA_US_CONNEXION = 19
    CA_US_NEXUS_CARD = 20
    ID_E_TOLL = 16
    IN_FASTAG = 78
    IN_LOCAL_HP_PLATE_EXEMPT = 79
    MX_IAVE = 90
    MX_PASE = 91
    MX_QUICKPASS = 93
    MX_SISTEMA_TELEPEAJE_CHIHUAHUA = 89
    MX_TAG_IAVE = 12
    MX_TAG_TELEVIA = 13
    MX_TELEVIA = 92
    MX_VIAPASS = 14
    US_AL_FREEDOM_PASS = 21
    US_AK_ANTON_ANDERSON_TUNNEL_BOOK_OF_10_TICKETS = 22
    US_CA_FASTRAK = 4
    US_CA_FASTRAK_CAV_STICKER = 86
    US_CO_EXPRESSTOLL = 23
    US_CO_GO_PASS = 24
    US_DE_EZPASSDE = 25
    US_FL_BOB_SIKES_TOLL_BRIDGE_PASS = 65
    US_FL_DUNES_COMMUNITY_DEVELOPMENT_DISTRICT_EXPRESSCARD = 66
    US_FL_EPASS = 67
    US_FL_GIBA_TOLL_PASS = 68
    US_FL_LEEWAY = 69
    US_FL_SUNPASS = 70
    US_FL_SUNPASS_PRO = 71
    US_IL_EZPASSIL = 73
    US_IL_IPASS = 72
    US_IN_EZPASSIN = 26
    US_KS_BESTPASS_HORIZON = 27
    US_KS_KTAG = 28
    US_KS_NATIONALPASS = 29
    US_KS_PREPASS_ELITEPASS = 30
    US_KY_RIVERLINK = 31
    US_LA_GEAUXPASS = 32
    US_LA_TOLL_TAG = 33
    US_MA_EZPASSMA = 6
    US_MD_EZPASSMD = 34
    US_ME_EZPASSME = 35
    US_MI_AMBASSADOR_BRIDGE_PREMIER_COMMUTER_CARD = 36
    US_MI_GROSSE_ILE_TOLL_BRIDGE_PASS_TAG = 37
    US_MI_IQ_PROX_CARD = 38
    US_MI_MACKINAC_BRIDGE_MAC_PASS = 39
    US_MI_NEXPRESS_TOLL = 40
    US_MN_EZPASSMN = 41
    US_NC_EZPASSNC = 42
    US_NC_PEACH_PASS = 87
    US_NC_QUICK_PASS = 43
    US_NH_EZPASSNH = 80
    US_NJ_DOWNBEACH_EXPRESS_PASS = 75
    US_NJ_EZPASSNJ = 74
    US_NY_EXPRESSPASS = 76
    US_NY_EZPASSNY = 77
    US_OH_EZPASSOH = 44
    US_PA_EZPASSPA = 45
    US_RI_EZPASSRI = 46
    US_SC_PALPASS = 47
    US_TX_BANCPASS = 48
    US_TX_DEL_RIO_PASS = 49
    US_TX_EFAST_PASS = 50
    US_TX_EAGLE_PASS_EXPRESS_CARD = 51
    US_TX_EPTOLL = 52
    US_TX_EZ_CROSS = 53
    US_TX_EZTAG = 54
    US_TX_LAREDO_TRADE_TAG = 55
    US_TX_PLUSPASS = 56
    US_TX_TOLLTAG = 57
    US_TX_TXTAG = 58
    US_TX_XPRESS_CARD = 59
    US_UT_ADAMS_AVE_PARKWAY_EXPRESSCARD = 60
    US_VA_EZPASSVA = 61
    US_WA_BREEZEBY = 17
    US_WA_GOOD_TO_GO = 1
    US_WV_EZPASSWV = 62
    US_WV_MEMORIAL_BRIDGE_TICKETS = 63
    US_WV_NEWELL_TOLL_BRIDGE_TICKET = 64


__all__ = tuple(sorted(__protobuf__.manifest))
